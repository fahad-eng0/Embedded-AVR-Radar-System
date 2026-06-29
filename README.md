# 📡 Autonomous AVR Radar Scanning System

An embedded radar scanning system that scans a 180° area using an ultrasonic sensor mounted on a servo motor. The system detects obstacles within 15cm and triggers a visual/audible alarm.

## 🛠️ Hardware Features
* **Microcontroller:** ATmega328P (Arduino Uno)
* **Actuator:** SG90 Servo Motor (Controlled via Hardware PWM)
* **Sensor:** HC-SR04 Ultrasonic Sensor
* **Alarm System:** Active Buzzer + Red/Green LEDs

## 🧠 Low-Level Software Architecture (Bare-Metal)
Instead of using standard Arduino libraries (like `<Servo.h>`), this project configures the microcontroller's registers directly:
* **Timer 2 (Fast PWM Mode):** Utilized to generate a precise 50Hz signal on Pin 3 to control the servo motor angles without blocking the CPU.
* **Timer 1:** Used for precise microsecond time-measurement of the ultrasonic echo pulse.
* **Bitwise Operations:** Used `DDRB`, `PORTB`, and `PINB` registers for lightning-fast I/O operations.
