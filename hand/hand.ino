#include <Servo.h>

Servo thumb;
Servo pointer;
Servo middle;
Servo ring;
Servo pinky;

int finger_pins[] = {9, 10, 11, 12, 13};

int readFinger(int index) {
	digitalWrite(finger_pins[index], HIGH);
	int reading = analogRead(0);
	digitalWrite(finger_pins[index], LOW);
	return reading;
}

long getForce(int fsrReading) {
	// analog voltage reading ranges from about 0 to 1023 which maps to 0V to 5V (= 5000mV)
	int fsrVoltage = map(fsrReading, 0, 1023, 0, 5000);
	// The voltage = Vcc * R / (R + FSR) where R = 10K and Vcc = 5V
	// so FSR = ((Vcc - V) * R) / V        yay math!
	unsigned long fsrResistance = 5000 - fsrVoltage;     // fsrVoltage is in millivolts so 5V = 5000mV
	fsrResistance *= 10000;                // 10K resistor
	fsrResistance /= fsrVoltage;

	unsigned long fsrConductance = 1000000;           // we measure in micromhos so 
	fsrConductance /= fsrResistance;

	// Use the two FSR guide graphs to approximate the force
	long fsrForce;
	if (fsrConductance <= 1000) {
		fsrForce = fsrConductance / 80;
	} else {
		fsrForce = fsrConductance - 1000;
		fsrForce /= 30;
	}

	return fsrForce;
}

void setup(void) {
	Serial.begin(9600);   // We'll send debugging information via the Serial monitor

	for (int i = 0; i < 5; i++) {
		pinMode(finger_pins[i], OUTPUT);
	}

	thumb.attach(6);
	pointer.attach(5);
	middle.attach(4);
	ring.attach(3);
	pinky.attach(2);
}

void loop(void) {
	for (int i = 0; i < 5; i++) {
		Serial.print(readFinger(i));
		if (i < 4) {
			Serial.print(',');
		}
	}
	Serial.println();

	// thumb.write(map(fsrForce, 0, 50, 50, 120));
	// pointer.write(map(fsrForce, 0, 50, 130, 80));
	// middle.write(map(fsrForce, 0, 50, 60, 120));
	// ring.write(map(fsrForce, 0, 50, 40, 100));
	// pinky.write(map(fsrForce, 0, 50, 130, 80));
	
	delay(100);
}
