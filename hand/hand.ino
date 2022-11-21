#include <Servo.h>

Servo thumb;
Servo pointer;
Servo middle;
Servo ring;
Servo pinky;

int fsrPin = 0;     // the FSR and 10K pulldown are connected to A0
int fsrReading;     // the analog reading from the FSR resistor divider
int fsrVoltage;     // the analog reading converted to voltage
unsigned long fsrResistance;  // The voltage converted to resistance, can be very big so make "long"
unsigned long fsrConductance; 
long fsrForce;       // Finally, the resistance converted to force
 
void setup(void) {
	Serial.begin(9600);   // We'll send debugging information via the Serial monitor

	thumb.attach(6);
	pointer.attach(5);
	middle.attach(4);
	ring.attach(3);
	pinky.attach(2);
}

void loop(void) {
	fsrReading = analogRead(fsrPin);  
	// analog voltage reading ranges from about 0 to 1023 which maps to 0V to 5V (= 5000mV)
	fsrVoltage = map(fsrReading, 0, 1023, 0, 5000);
	// The voltage = Vcc * R / (R + FSR) where R = 10K and Vcc = 5V
	// so FSR = ((Vcc - V) * R) / V        yay math!
	fsrResistance = 5000 - fsrVoltage;     // fsrVoltage is in millivolts so 5V = 5000mV
	fsrResistance *= 10000;                // 10K resistor
	fsrResistance /= fsrVoltage;
	Serial.print("FSR resistance in ohms = ");
	Serial.println(fsrResistance);

	fsrConductance = 1000000;           // we measure in micromhos so 
	fsrConductance /= fsrResistance;

	// Use the two FSR guide graphs to approximate the force
	if (fsrConductance <= 1000) {
	fsrForce = fsrConductance / 80;
	Serial.print("Force in Newtons: ");
	Serial.println(fsrForce);
	} else {
	fsrForce = fsrConductance - 1000;
	fsrForce /= 30;
	Serial.print("Force in Newtons: ");
	Serial.println(fsrForce);
	}

	thumb.write(map(fsrForce, 0, 50, 50, 120));
	pointer.write(map(fsrForce, 0, 50, 130, 80));
	middle.write(map(fsrForce, 0, 50, 60, 120));
	ring.write(map(fsrForce, 0, 50, 40, 100));
	pinky.write(map(fsrForce, 0, 50, 130, 80));
	
	delay(10);
}