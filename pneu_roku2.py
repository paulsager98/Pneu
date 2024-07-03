from gpiozero import DigitalInputDevice, OutputDevice
from time import sleep

# GPIO-Pins für die Sensoren und Ventile festlegen (Beispiel-Pins)
pin_sensor_top = 8
pin_sensor_bottom = 7
pin_valve_top = 2
pin_valve_bottom = 3

# Sensoren als DigitalInputDevice konfigurieren
sensor_top = DigitalInputDevice(pin=pin_sensor_top)
sensor_bottom = DigitalInputDevice(pin=pin_sensor_bottom)

# Ventile als OutputDevice konfigurieren
valve_top = OutputDevice(pin=pin_valve_top, initial_value=False)
valve_bottom = OutputDevice(pin=pin_valve_bottom, initial_value=False)

try:
    while True:
        # Überprüfen der Sensorwerte und Steuerung der Ventile
        if sensor_bottom.is_active:
            valve_top.on()
        else:
            valve_top.off()

        if sensor_top.is_active:
            valve_bottom.on()
        else:
            valve_bottom.off()

        # Kurze Pause, bevor die Schleife erneut durchlaufen wird
        sleep(0.1)

except KeyboardInterrupt:
    print("Programm wurde beendet.")

finally:
    # Ventile ausschalten und GPIO-Pins freigeben
    valve_top.off()
    valve_bottom.off()
    sensor_top.close()
    sensor_bottom.close()

