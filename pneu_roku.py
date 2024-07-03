import gpiozero
import time
import RPI.GPIO as GPIO
from signal import pause

Top_valpin = gpiozero.LED(2) #Valve 1 (for Upper Chamber)
Bot_valpin = gpiozero.LED(3)	#Valve 2 (For Lower Chamber)

Sensor_Top = 8 #set pin for upper sensor
Sensor_Bot = 7 #set pin for bottom sensor
#pull up = false?


Top_valpin.off()
Bot_valpin.off()

#GPIO-Modus festlegen
GPIO.setmode(GPIO.BCM)

#Pins als Eingang (Sensors) und Ausgang (Ventile) festlegen
GPIO.setup(Sensor_Top, GPIO.IN) 
GPIO.setup(Sensor_Bot, GPIO.IN) 
GPIO.setup(Top_valpin, GPIO.OUT) 
GPIO.setup(Bot_valpin, GPIO.OUT) 


try:
	while True:
		#sensoren auslesen
		Sensor_Top_state = GPIO.input(Sensor_Top)
		Sensor_Bot_state = GPIO.input(Sensor_Bot)
		
		#ventilsteuerung aufgrund der sensor auslesung
		
		if Sensor_Top_state == GPIO.HIGH:
			GPIO.output(Bot_valpin, GPIO.HIGH)	#Ventil Bot öffnen
		else:
			GPIO.output(Bot_valpin, GPIO.LOW)	#Ventil Bot schließen
			
		if Sensor_Bot_state == GPIO.HIGH:
			GPIO.output(Top_valpin, GPIO.HIGH)	#Ventil Top öffnen
		else:
			GPIO.output(Top_valpin, GPIO.LOW)	#Ventil Top schließen
		time.sleep(0.01)
	
except KeyboardInterrupt:
	#GPIO-Einstellungen zurücksetzen, wenn das Skript beendet wird
	GPIO.cleanup
	



