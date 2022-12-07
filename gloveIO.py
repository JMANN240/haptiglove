from dataglove import *
import serial
import msvcrt
from time import sleep

THUMB = 0
INDEX = 1
MIDDLE = 2
RING = 3
PINKY = 4
PALM = 5

ser = serial.Serial('COM12', 115200)
ser.flush()

def get_pressure_data():
	# Captures sensor data from pressure sensors 
	try:
		data = ser.readline().decode()
		pressures = [(float(n)/60)**(1/2) for n in data.split(',')]
	except:
		pressures = [0,0,0,0,0]
	print("""
	
	
	
	
	
	
	
	
	
	 """)
	print(pressures)
	print(""" 
	
	
	
	
	
	
	
	""")

	return pressures

def update_haptics(datagloveIO, normalizedPressureData):
	# Sends haptics to glove
	# Forte_SendHaptic(leftHand, 4, 0, 1.0)
	# pass
	try:
		Forte_SendHaptic(datagloveIO, THUMB, 0, normalizedPressureData)
		Forte_SendHaptic(datagloveIO, INDEX, 0, normalizedPressureData)
		Forte_SendHaptic(datagloveIO, MIDDLE, 0, normalizedPressureData)
		Forte_SendHaptic(datagloveIO, RING, 0, normalizedPressureData)
		Forte_SendHaptic(datagloveIO, PINKY, 0, normalizedPressureData)
	except(GloveDisconnectedException):
		print("Glove is Disconnected")
		
def send_sensors():
	# [0, -16, 16, 23, 104, 115, 127, 86, 63, 116]
	try:
		# sleep(0.1)

		sensors = Forte_GetFullReport(leftHand)
		sleep(0.05)
		thumb = sensors[4] + sensors[5]
		index = sensors[6] + sensors[7]
		middle = sensors[8] + sensors[9]
		
		print(sensors)

		sleep(0.05)
		ser.write(f"{str(thumb).rjust(3, '0')},{str(index).rjust(3, '0')},{str(middle).rjust(3, '0')},{str(middle).rjust(3, '0')},{str(middle).rjust(3, '0')}".encode("utf-8"))
	except(KeyboardInterrupt):
		Forte_SilenceHaptics(leftHand)
		Forte_DestroyDataGloveIO(leftHand)
		ser.close()
		exit()
	except:
		print("Glove is Disconnected")

i = 0

if __name__ == '__main__':

	mode = input("Select mode (1 | 2 | 3):\n1. Haptic + Visual\n2. Haptic Only\n3. Visual Only ")
	mode = int(mode)
	file = ['Haptic+Visual', 'HapticOnly', 'VisualOnly']
	
	leftHand = Forte_CreateDataGloveIO(1, "")



	while True:
		try:
			send_sensors()
			pressure_data = get_pressure_data()
			pressure_data = pressure_data[0]
			
			if msvcrt.kbhit():
				print(msvcrt.getch())
				if msvcrt.getch() == b' ':
					outputFile = open(f"Data_{file[mode -1]}.txt", "a")
					outputFile.write(f"{pressure_data}\n")
					outputFile.close()
			if mode != 3:
				update_haptics(leftHand, pressure_data)
		except(KeyboardInterrupt):
			Forte_SilenceHaptics(leftHand)
			Forte_DestroyDataGloveIO(leftHand)
			ser.close()
			exit()
		i += 1
		sleep(0.05)
