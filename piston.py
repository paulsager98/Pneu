import gpiozero
import time
from signal import pause
import multiprocessing as mp




chamber_upper = gpiozero.LED(10)
chamber_lower = gpiozero.LED(9)

valv_upper = gpiozero.LED(2) #Valve 1 (for Upper Chamber)
valv_lower = gpiozero.LED(3)	#Valve 2 (For Lower Chamber)


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
	
	#time.sleep(0.01)
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
	
	#time.sleep(0.01)
	valv_lower.on()
	
def close_upper():
	'''
	To be executed when lower Limit Switch is released
	'''
	print("Lower Falling Trigger")
	time.sleep(0.6)
	valv_upper.off()
	
def close_lower():
	'''
	To be executed when upper Limit Switch is released
	'''
	print("Upper Falling Trigger")
	time.sleep(0.15)
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




try:
	
	while True:
		time.sleep(0.03)
		#Cutter reached top
		valv_lower.on()
		time.sleep(0.5) #delay for upper chamber after reaching TDC
		valv_upper.off()
		time.sleep(0.04)
		chamber_upper.on()	#fire chamber
		time.sleep(0.045)	#firing duration
		chamber_upper.off()
		time.sleep(0.05)
		valv_upper.on()
		
		
		
		
		time.sleep(0.1) #delay for lower chamber after reaching BDC
		valv_lower.off()
		time.sleep(0.04)
		chamber_lower.on()	#fire chamber
		time.sleep(0.045)	#firing duration
		chamber_lower.off()

except KeyboardInterrupt:
	chamber_upper.off()
	chamber_lower.off()
	valv_upper.on()
	valv_lower.on()
	time.sleep(3)
	valv_lower.off()
	valv_upper.off()
	time.sleep(1)
	
	


