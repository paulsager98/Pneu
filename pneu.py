import gpiozero
import time
from signal import pause

valv_upper = gpiozero.LED(2) #Valve 1 (for Upper Chamber)
valv_lower = gpiozero.LED(3)	#Valve 2 (For Lower Chamber)

in_lower = gpiozero.Button(7, pull_up = False) #Lower Limit Switch
in_upper = gpiozero.Button(8, pull_up = False) #Upper Limit Switch


valv_upper.off()
valv_lower.off()


	
def vent_upper():
	
	'''
	To be executed when lower Limit Switch is set
	'''
	
	print("Lower Rising Trigger")
	#valv_lower.off()
	#time.sleep(0.05)			#Limit Switch Delay
	#valv_upper.on()					#Vent
	#time.sleep(0.6)				#Venting Time
	
	#valv_upper.off()					#Close Valve for Firing upper Chamber
	
	time.sleep(0.05)
	valv_upper.on()
	

def vent_lower():
	
	'''
	To be executed when upper Limit Switch is set
	'''
	print("Upper Rising Trigger")
	#time.sleep(0.05)			#Limit Switch Delay
	#valv_lower.on()					#Vent
	#time.sleep(0.75)				#Venting Time
	
	#valv_lower.off()					#Close Valve for Firing lower Chamber
	
	time.sleep(0.05)
	valv_lower.on()
	
def close_upper():
	'''
	To be executed when lower Limit Switch is released
	'''
	print("Lower Falling Trigger")
	time.sleep(0.25)
	valv_upper.off()
	
def close_lower():
	'''
	To be executed when upper Limit Switch is released
	'''
	print("Upper Falling Trigger")
	time.sleep(0.25)
	valv_lower.off()

	
def purge():
	valv_upper.on()
	valv_lower.on()
	
	input("Press Enter to Stop Purging!")
	
	time.sleep(1)
	valv_upper.off()
	time.sleep(1)
	valv_lower.off()
	
def manual_mode():
	while True:
		match input("Choose Valve (U/L), E to Exit"):
			case "U":
				while True:
					match input("Choose Position (O/C), E to Exit"):
					
						case "O":
							
							valv_upper.on()
							
						case "C":
							valv_upper.off()
							
						case "E":
							break
			case "L":
				while True:
					match input("Choose Position (O/C), E to Exit"):
					
						case "O":
							
							valv_lower.on()
							
						case "C":
							valv_lower.off()
							
						case "E":
							break
			case "E":
				break

match input("Do you want to Purge ? (Y/N), M for Manual Control"):

	case "Y": 
		purge()
	
	case "N":
		pass
		
	case "M":
		manual_mode()

	
valv_lower.on()

in_lower.when_pressed = vent_upper
in_lower.when_released = close_upper

in_upper.when_pressed = vent_lower
in_upper.when_released = close_lower

pause()
	


