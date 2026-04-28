from __future__ import annotations

import unittest

from autonomous_driver import (
    AutonomousConfig,
    SIGN_CONTINUE,
    SIGN_SPEED_30,
    SIGN_SPEED_90,
    SIGN_STOP,
    SIGN_TURN_LEFT,
    SIGN_TURN_RIGHT,
    decide_autonomous_control,
)


FRAME_SHAPE = (480, 640, 3)
NOW = 10.0


def prediction(label: str, *, x: float, y: float = 240, width: float = 110, height: float = 110):
    return {
        "class": label,
        "confidence": 0.91,
        "x": x,
        "y": y,
        "width": width,
        "height": height,
    }


class AutonomousDriverTest(unittest.TestCase):
    def setUp(self) -> None:
        self.config = AutonomousConfig()

    def decide(self, predictions):
        return decide_autonomous_control(
            predictions,
            frame_shape=FRAME_SHAPE,
            now=NOW,
            frame_time=NOW - 0.1,
            predictions_time=NOW - 0.1,
            config=self.config,
        )

    def test_stop_near_central_holds_neutral(self):
        decision = self.decide([prediction(SIGN_STOP, x=320, width=180, height=180)])
        self.assertEqual(decision.action, "stop")
        self.assertEqual(decision.throttle, self.config.neutral_throttle)
        self.assertEqual(decision.steering, self.config.neutral_steering)

    def test_turn_direction_uses_model_class(self):
        left = self.decide([prediction(SIGN_TURN_LEFT, x=160, width=180, height=180)])
        right = self.decide([prediction(SIGN_TURN_RIGHT, x=480, width=180, height=180)])
        self.assertEqual(left.action, "turn-left")
        self.assertEqual(right.action, "turn-right")
        self.assertGreater(left.steering, self.config.neutral_steering)
        self.assertLess(right.steering, self.config.neutral_steering)

    def test_closer_sign_wins_over_far_side_sign(self):
        decision = self.decide(
            [
                prediction(SIGN_TURN_LEFT, x=150, width=55, height=55),
                prediction(SIGN_TURN_RIGHT, x=500, width=180, height=180),
            ]
        )
        self.assertEqual(decision.action, "turn-right")
        self.assertEqual(decision.target.zone, "right")

    def test_speed_signs_change_throttle(self):
        slow = self.decide([prediction(SIGN_SPEED_30, x=320, width=150, height=150)])
        fast = self.decide([prediction(SIGN_SPEED_90, x=320, width=150, height=150)])
        self.assertEqual(slow.action, "speed-30")
        self.assertEqual(fast.action, "speed-90")
        self.assertLess(slow.throttle, fast.throttle)

    def test_far_stop_approaches_instead_of_full_stop(self):
        decision = self.decide([prediction(SIGN_STOP, x=320, width=50, height=50)])
        self.assertEqual(decision.action, "approach-stop")
        self.assertGreater(decision.throttle, self.config.neutral_throttle)

    def test_no_relevant_sign_continues(self):
        decision = self.decide(
            [
                {"class": SIGN_CONTINUE, "confidence": 0.1, "x": 320, "y": 240, "width": 140, "height": 140}
            ]
        )
        self.assertEqual(decision.action, "continue")
        self.assertGreater(decision.throttle, self.config.neutral_throttle)


if __name__ == "__main__":
    unittest.main()
