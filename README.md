# Scripts de control (DeepRacer)

Descripcion corta de cada script:

- `car1_manual_control_server.py`: servidor UDP para el coche 1; recibe imagen/LIDAR, muestra la camara y mapa LIDAR, y envia control manual desde teclado.
- `car3_manual_control_server.py`: servidor UDP para el coche 3; recibe imagen/LIDAR, muestra la camara y mapa LIDAR, y envia control manual desde teclado.
- `car1_cloud_control_server.py`: servidor UDP para el coche 1; recibe imagen/LIDAR/bateria y calcula control autonomo con `artemis_autonomous_car`.
- `car3_cloud_control_server.py`: servidor UDP para el coche 3; recibe imagen/LIDAR/bateria y calcula control autonomo con `artemis_autonomous_car`.
- `car1_cloud_control_server_real_time_control.py`: como `car1_cloud_control_server.py` pero permite cambiar el modo de control en tiempo real con teclado.
- `car3_cloud_control_server_real_time_control.py`: como `car3_cloud_control_server.py` pero permite cambiar el modo de control en tiempo real con teclado.
- `artemis_autonomous_car.py`: logica local de autonomia (procesamiento de imagen/LIDAR y decisiones de control).
