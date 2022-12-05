from dataglove import *
import serial
from time import sleep

THUMB = 0
INDEX = 1
MIDDLE = 2
RING = 3
PINKY = 4
PALM = 5

ser = serial.Serial('COM4', 115200)
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
	pass
	# if (len(normalizedPressureData) == 5):

	# 	Forte_SendHaptic(datagloveIO, THUMB, 0, normalizedPressureData[0])
	# 	Forte_SendHaptic(datagloveIO, INDEX, 0, normalizedPressureData[1])
	# 	Forte_SendHaptic(datagloveIO, MIDDLE, 0, normalizedPressureData[2])
	# 	Forte_SendHaptic(datagloveIO, RING, 0, normalizedPressureData[3])
	# 	Forte_SendHaptic(datagloveIO, PINKY, 0, normalizedPressureData[4])

def send_sensors():
	# [0, -16, 16, 23, 104, 115, 127, 86, 63, 116]
	try:
		# leftHand = Forte_CreateDataGloveIO(1, "")
		# sleep(0.1)

		sensors = Forte_GetFullReport(leftHand)
		sleep(0.05)
		thumb = sensors[4] + sensors[5]
		index = sensors[6] + sensors[7]
		middle = sensors[8] + sensors[9]
		
		print(sensors)

		# Forte_DestroyDataGloveIO(leftHand)
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

	leftHand = Forte_CreateDataGloveIO(1, "")

	while True:
		try:
			send_sensors()
			update_haptics(leftHand, get_pressure_data())
		except(KeyboardInterrupt):
			Forte_SilenceHaptics(leftHand)
			Forte_DestroyDataGloveIO(leftHand)
			ser.close()
			exit()
		i += 1
		sleep(0.05)
