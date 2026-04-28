from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence


SIGN_CONTINUE = "OBLIGATORIO-CONTINUAR-RECTO"
SIGN_TURN_RIGHT = "OBLIGATORIO-GIRAR-DERECHA"
SIGN_TURN_LEFT = "OBLIGATORIO-GIRAR-IZQUIERDA"
SIGN_NO_ENTRY = "PROHIBIDO"
SIGN_STOP = "STOP"
SIGN_SPEED_30 = "VELOCIDAD-MAX-30"
SIGN_SPEED_90 = "VELOCIDAD-MAX-90"

KNOWN_SIGNS = {
    SIGN_CONTINUE,
    SIGN_TURN_RIGHT,
    SIGN_TURN_LEFT,
    SIGN_NO_ENTRY,
    SIGN_STOP,
    SIGN_SPEED_30,
    SIGN_SPEED_90,
}

SAFETY_SIGNS = {SIGN_STOP, SIGN_NO_ENTRY}
TURN_SIGNS = {SIGN_TURN_LEFT, SIGN_TURN_RIGHT}
SPEED_SIGNS = {SIGN_SPEED_30, SIGN_SPEED_90}


@dataclass(frozen=True)
class AutonomousConfig:
    min_confidence: float = 0.35
    stale_prediction_sec: float = 1.25
    max_frame_age_sec: float = 1.0
    min_area_ratio: float = 0.004
    near_area_ratio: float = 0.045
    center_left: float = 0.40
    center_right: float = 0.60
    neutral_steering: float = 0.25
    neutral_throttle: float = 0.0
    crawl_throttle: float = 0.12
    slow_throttle: float = 0.18
    turn_throttle: float = 0.22
    cruise_throttle: float = 0.34
    fast_throttle: float = 0.48
    left_steering: float = 0.84
    right_steering: float = -0.84


@dataclass(frozen=True)
class SignObservation:
    label: str
    confidence: float
    x: float
    y: float
    width: float
    height: float
    center_x: float
    center_y: float
    area_ratio: float
    zone: str
    distance: str
    score: float

    def to_status(self) -> dict[str, Any]:
        return {
            "class": self.label,
            "confidence": round(self.confidence, 4),
            "x": round(self.x, 2),
            "y": round(self.y, 2),
            "width": round(self.width, 2),
            "height": round(self.height, 2),
            "center_x": round(self.center_x, 4),
            "center_y": round(self.center_y, 4),
            "area_ratio": round(self.area_ratio, 5),
            "zone": self.zone,
            "distance": self.distance,
            "score": round(self.score, 4),
        }


@dataclass(frozen=True)
class AutonomousDecision:
    active: bool
    steering: float
    throttle: float
    action: str
    reason: str
    target: SignObservation | None
    candidates: tuple[SignObservation, ...]

    def control(self) -> tuple[float, float]:
        return self.steering, self.throttle

    def to_status(self) -> dict[str, Any]:
        return {
            "active": self.active,
            "steering": round(self.steering, 3),
            "throttle": round(self.throttle, 3),
            "action": self.action,
            "reason": self.reason,
            "target": None if self.target is None else self.target.to_status(),
            "candidates": [candidate.to_status() for candidate in self.candidates[:6]],
        }


def decide_autonomous_control(
    predictions: list[dict[str, Any]],
    *,
    frame_shape: Sequence[int] | None,
    now: float,
    frame_time: float | None,
    predictions_time: float | None,
    config: AutonomousConfig,
) -> AutonomousDecision:
    if frame_time is None or now - frame_time > config.max_frame_age_sec:
        return _neutral(config, "safe-neutral", "no-fresh-frame")

    if predictions_time is None:
        return _neutral(config, "safe-neutral", "no-inference-yet")

    if now - predictions_time > config.stale_prediction_sec:
        return _neutral(config, "safe-neutral", "stale-inference")

    observations = build_observations(predictions, frame_shape=frame_shape, config=config)
    if not observations:
        return AutonomousDecision(
            active=True,
            steering=round(config.neutral_steering, 3),
            throttle=round(config.cruise_throttle, 3),
            action="continue",
            reason="no-relevant-sign",
            target=None,
            candidates=(),
        )

    target = observations[0]
    steering, throttle, action, reason = command_for_observation(target, config)
    return AutonomousDecision(
        active=True,
        steering=round(steering, 3),
        throttle=round(throttle, 3),
        action=action,
        reason=reason,
        target=target,
        candidates=tuple(observations),
    )


def build_observations(
    predictions: list[dict[str, Any]],
    *,
    frame_shape: Sequence[int] | None,
    config: AutonomousConfig,
) -> list[SignObservation]:
    frame_h, frame_w = _frame_size(frame_shape)
    if frame_w <= 0 or frame_h <= 0:
        return []

    observations: list[SignObservation] = []
    for prediction in predictions:
        observation = observation_from_prediction(prediction, frame_w, frame_h, config)
        if observation is not None:
            observations.append(observation)

    observations.sort(key=lambda item: item.score, reverse=True)
    return observations


def observation_from_prediction(
    prediction: dict[str, Any],
    frame_w: int,
    frame_h: int,
    config: AutonomousConfig,
) -> SignObservation | None:
    label = str(prediction.get("class") or prediction.get("class_name") or "").strip()
    if label not in KNOWN_SIGNS:
        return None

    confidence = _float_or_none(prediction.get("confidence"))
    if confidence is None or confidence < config.min_confidence:
        return None

    x = _float_or_none(prediction.get("x"))
    y = _float_or_none(prediction.get("y"))
    width = _float_or_none(prediction.get("width"))
    height = _float_or_none(prediction.get("height"))
    if x is None or y is None or width is None or height is None:
        return None
    if width <= 0 or height <= 0:
        return None

    center_x = _clamp(x / frame_w, 0.0, 1.0)
    center_y = _clamp(y / frame_h, 0.0, 1.0)
    area_ratio = _clamp((width * height) / float(frame_w * frame_h), 0.0, 1.0)
    if area_ratio < config.min_area_ratio:
        return None

    zone = _zone(center_x, config)
    distance = _distance(area_ratio, config)
    class_weight = {
        SIGN_STOP: 1.70,
        SIGN_NO_ENTRY: 1.65,
        SIGN_TURN_LEFT: 1.28,
        SIGN_TURN_RIGHT: 1.28,
        SIGN_SPEED_30: 1.08,
        SIGN_SPEED_90: 1.02,
        SIGN_CONTINUE: 0.96,
    }[label]
    zone_weight = 1.0 if zone == "center" else 0.82
    distance_weight = min(2.4, max(0.18, (area_ratio / max(config.near_area_ratio, 0.0001)) * 2.4))
    score = confidence * class_weight * zone_weight * distance_weight

    return SignObservation(
        label=label,
        confidence=confidence,
        x=x,
        y=y,
        width=width,
        height=height,
        center_x=center_x,
        center_y=center_y,
        area_ratio=area_ratio,
        zone=zone,
        distance=distance,
        score=score,
    )


def command_for_observation(
    observation: SignObservation,
    config: AutonomousConfig,
) -> tuple[float, float, str, str]:
    label = observation.label

    if label in SAFETY_SIGNS:
        if observation.distance == "far":
            return (
                _steer_towards_zone(observation, config, strength=0.12),
                config.crawl_throttle,
                "approach-stop",
                f"{label}:far-{observation.zone}",
            )
        return (
            config.neutral_steering,
            config.neutral_throttle,
            "stop",
            f"{label}:{observation.distance}-{observation.zone}",
        )

    if label == SIGN_TURN_LEFT:
        strength = _turn_strength(observation)
        steering = _blend(config.neutral_steering, config.left_steering, strength)
        throttle = config.turn_throttle if observation.distance != "far" else config.slow_throttle
        action = "turn-left" if observation.distance != "far" else "prepare-left"
        return steering, throttle, action, f"{label}:{observation.distance}-{observation.zone}"

    if label == SIGN_TURN_RIGHT:
        strength = _turn_strength(observation)
        steering = _blend(config.neutral_steering, config.right_steering, strength)
        throttle = config.turn_throttle if observation.distance != "far" else config.slow_throttle
        action = "turn-right" if observation.distance != "far" else "prepare-right"
        return steering, throttle, action, f"{label}:{observation.distance}-{observation.zone}"

    if label == SIGN_SPEED_30:
        return (
            _steer_towards_zone(observation, config, strength=0.08),
            config.slow_throttle,
            "speed-30",
            f"{label}:{observation.distance}-{observation.zone}",
        )

    if label == SIGN_SPEED_90:
        return (
            _steer_towards_zone(observation, config, strength=0.04),
            config.fast_throttle,
            "speed-90",
            f"{label}:{observation.distance}-{observation.zone}",
        )

    return (
        _steer_towards_zone(observation, config, strength=0.08),
        config.cruise_throttle,
        "continue",
        f"{label}:{observation.distance}-{observation.zone}",
    )


def _neutral(config: AutonomousConfig, action: str, reason: str) -> AutonomousDecision:
    return AutonomousDecision(
        active=False,
        steering=round(config.neutral_steering, 3),
        throttle=round(config.neutral_throttle, 3),
        action=action,
        reason=reason,
        target=None,
        candidates=(),
    )


def _frame_size(frame_shape: Sequence[int] | None) -> tuple[int, int]:
    if frame_shape is None or len(frame_shape) < 2:
        return 0, 0
    try:
        return int(frame_shape[0]), int(frame_shape[1])
    except (TypeError, ValueError):
        return 0, 0


def _float_or_none(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def _zone(center_x: float, config: AutonomousConfig) -> str:
    if center_x < config.center_left:
        return "left"
    if center_x > config.center_right:
        return "right"
    return "center"


def _distance(area_ratio: float, config: AutonomousConfig) -> str:
    if area_ratio >= config.near_area_ratio:
        return "near"
    if area_ratio >= config.near_area_ratio * 0.40:
        return "mid"
    return "far"


def _turn_strength(observation: SignObservation) -> float:
    if observation.distance == "near":
        return 1.0
    if observation.distance == "mid":
        return 0.72
    return 0.36


def _steer_towards_zone(
    observation: SignObservation,
    config: AutonomousConfig,
    *,
    strength: float,
) -> float:
    if observation.zone == "left":
        return _blend(config.neutral_steering, config.left_steering, strength)
    if observation.zone == "right":
        return _blend(config.neutral_steering, config.right_steering, strength)
    return config.neutral_steering


def _blend(start: float, end: float, factor: float) -> float:
    return start + (end - start) * _clamp(factor, 0.0, 1.0)
