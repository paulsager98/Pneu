import gpiozero
import time
from signal import pause
import multiprocessing as mp
from functools import partial





purge_event = mp.Event()
purge_done_event = mp.Event()








def valve_process_bot(purge_event, purge_done_event):
	
	valv_lower = gpiozero.LED(3)	#Valve 2 (For Lower Chamber)
	in_upper = gpiozero.Button(8, pull_up = False) #Upper Limit Switch
	valv_lower.off()
	
	def vent_lower(valv_lower):
		print("Upper Rising Trigger")
		time.sleep(0.02)
		valv_lower.on()
			
	def close_lower(valv_lower):
		print("Upper Falling Trigger")
		time.sleep(0.005)
		valv_lower.off()
		
	print("starting lower process")
	in_upper.when_pressed = partial(vent_lower, valv_lower)
	in_upper.when_released = partial(close_lower, valv_lower)
	
	while True:
		if purge_event.is_set():
			valv_lower.on()
			purge_event.clear()
			
		elif purge_done_event.is_set():
			valv_lower.on()
			purge_done_event.clear()


def valve_process_top(purge_event, purge_done_event):
	
	valv_upper = gpiozero.LED(2) #Valve 1 (for Upper Chamber)
	in_lower = gpiozero.Button(7, pull_up = False) #Lower Limit Switch
	valv_upper.off()
	
	def vent_upper(valv_upper):
		print("Lower Rising Trigger")
		time.sleep(0.005)
		valv_upper.on()
			
	def close_upper(valv_upper):
		print("Lower Falling Trigger")
		time.sleep(1.55)
		valv_upper.off()
	
	print("starting upper process")
	in_lower.when_pressed = partial(vent_upper, valv_upper)
	in_lower.when_released = partial(close_upper, valv_upper)
	print("wait for purge")
	while True:
		if purge_event.is_set():
			valv_upper.on()
			purge_event.clear()
			
		elif purge_done_event.is_set():
			valv_upper.off()
			purge_done_event.clear()

def purge(purge_event, purge_done_event):
	purge_event.set()
	
	input("Press Enter to Stop Purging!")
	
	time.sleep(1)
	purge_done_event.set()
	
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

process_bot = mp.Process(target=valve_process_bot, args=(purge_event, purge_done_event))
process_top = mp.Process(target=valve_process_top, args=(purge_event, purge_done_event))

process_bot.start()
process_top.start()



time.sleep(2)

match input("Do you want to Purge ? (Y/N), M for Manual Control"):

	case "Y":
		purge(purge_event, purge_done_event)
	
	case "N":
		pass
		
	case "M":
		manual_mode()



process_bot.join()
process_top.join()
