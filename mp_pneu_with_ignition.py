import gpiozero
import time
from signal import pause
import multiprocessing as mp
from functools import partial
import atexit
import signal





purge_event = mp.Event()
purge_done_event = mp.Event()
start_event = mp.Event()
termination_event = mp.Event()









def valve_process_bot(purge_event, purge_done_event, start_event, termination_event):
	
	valv_lower = gpiozero.LED(3)	#Valve 2 (For Lower Chamber)
	chamber_upper = gpiozero.LED(10)
	in_upper = gpiozero.Button(8, pull_up = False) #Upper Limit Switch
	valv_lower.off()
	
	def vent_lower(valv_lower, chamber_upper):
		print("Upper Rising Trigger")
		time.sleep(0.02)
		#Cutter reached top
		valv_lower.on()
		time.sleep(0.9) #delay for upper chamber after reaching TDC
		chamber_upper.on()	#fire chamber
		time.sleep(10)	#firing duration
		chamber_upper.off()
			
	def close_lower(valv_lower):
		print("Upper Falling Trigger")
		time.sleep(0.005)
		valv_lower.off()
		
	def cleanup(valv_lower, chamber_upper):
		print("Cleaning Up bottom Process")
		valv_lower.off()
		chamber_upper.off()
	
	print("starting lower process")

	
	in_upper.when_pressed = partial(vent_lower, valv_lower, chamber_upper)
	in_upper.when_released = partial(close_lower, valv_lower)
	
	while not termination_event.is_set():
		if purge_event.is_set():
			valv_lower.on()
			purge_event.clear()
			
		elif purge_done_event.is_set():
			valv_lower.on()
			purge_done_event.clear()
			
		elif start_event.is_set():
			vent_lower(valv_lower, chamber_upper)
			start_event.clear()
			
	print("Exiting lower Process")
	cleanup(valv_lower, chamber_upper)
	print("Cleanup Done")



def valve_process_top(purge_event, purge_done_event, termination_event):
	
	valv_upper = gpiozero.LED(2) #Valve 1 (for Upper Chamber)
	chamber_lower = gpiozero.LED(9)
	in_lower = gpiozero.Button(7, pull_up = False) #Lower Limit Switch
	valv_upper.off()
	
	def vent_upper(valv_upper, chamber_lower):
		print("Lower Rising Trigger")
		time.sleep(0.005)
		valv_upper.on()
		time.sleep(0.2) #delay for lower chamber after reaching BDC
		chamber_lower.on()	#fire chamber
		time.sleep(0.06)	#firing duration
		chamber_lower.off()
			
	def close_upper(valv_upper):
		print("Lower Falling Trigger")
		time.sleep(0.4)
		valv_upper.off()
		
	def cleanup(valv_upper, chamber_lower):
		print("Cleaning Up top Process")
		valv_upper.off()
		chamber_lower.off()
	
	print("starting upper process")
	in_lower.when_pressed = partial(vent_upper, valv_upper, chamber_lower)
	in_lower.when_released = partial(close_upper, valv_upper)
	print("wait for purge")
	while not termination_event.is_set():
		if purge_event.is_set():
			valv_upper.on()
			purge_event.clear()
			
		elif purge_done_event.is_set():
			valv_upper.off()
			purge_done_event.clear()
			
	print("Exiting lower Process")
	cleanup(valv_upper, chamber_lower)
	print("Cleanup Done")

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

def handle_signal(signum, frame, termination_event):
	print("recived Exit Signal....")
	termination_event.set()
	time.sleep(1)
	


	
	
signal.signal(signal.SIGTERM, termination_event.set)
signal.signal(signal.SIGINT, termination_event.set)
signal.signal(signal.SIGHUP, termination_event.set)

process_bot = mp.Process(target=valve_process_bot, args=(purge_event, purge_done_event, start_event, termination_event))
process_top = mp.Process(target=valve_process_top, args=(purge_event, purge_done_event, termination_event))

process_bot.start()
process_top.start()



time.sleep(2)

match input("Do you want to Purge ? (Y/N), M for Manual Control"):

	case "Y":
		purge(purge_event, purge_done_event)
		start_event.set()
	
	case "N":
		start_event.set()
		
	case "M":
		manual_mode()

input("Press a Key to exit")
termination_event.set()

process_bot.join()
process_top.join()
