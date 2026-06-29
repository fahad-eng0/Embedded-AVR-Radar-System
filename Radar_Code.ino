void setup() {
  DDRB |= (1 << 0);  
  DDRB |= (1 << 1); 
  DDRB |= (1 << 2);  
  DDRB |= (1 << 3);  
  DDRB &= ~(1 << 4); 

  DDRD |= (1 << 3);  

  TCCR1A = 0; 

  TCCR2A = (1 << COM2B1) | (1 << WGM21) | (1 << WGM20); 
  TCCR2B = (1 << WGM22) | (1 << CS22) | (1 << CS21) | (1 << CS20); // Prescaler 1024
  OCR2A = 156; 
}

void setServoAngle(int angle) {
  int ocrValue = 8 + (angle * 16 / 180);
  OCR2B = ocrValue;
  delay(15); 
}

unsigned int readDistance() {
  PORTB &= ~(1 << 3); 
  delayMicroseconds(2);
  PORTB |= (1 << 3);  
  delayMicroseconds(10);
  PORTB &= ~(1 << 3); 

  while (!(PINB & (1 << 4))); 
  TCNT1 = 0; 
  TCCR1B = (1 << CS10); 
  while (PINB & (1 << 4));
  TCCR1B = 0; 

  return (TCNT1 / 16) / 58;
}

void loop() {
  for (int angle = 15; angle <= 165; angle += 15) {
    setServoAngle(angle);
    unsigned int distance = readDistance();

    if (distance < 15) { 
      PORTB |= (1 << 1);  
      PORTB |= (1 << 2);  
      PORTB &= ~(1 << 0); 
      delay(300);         
    } else { 
      PORTB |= (1 << 0);  
      PORTB &= ~(1 << 1); 
      PORTB &= ~(1 << 2); 
    }
    delay(100);
  }

  for (int angle = 165; angle >= 15; angle -= 15) {
    setServoAngle(angle);
    unsigned int distance = readDistance();

    if (distance < 15) { 
      PORTB |= (1 << 1);  
      PORTB |= (1 << 2);  
      PORTB &= ~(1 << 0); 
      delay(300);
    } else { 
      PORTB |= (1 << 0);  
      PORTB &= ~(1 << 1); 
      PORTB &= ~(1 << 2); 
    }
    delay(100);
  }
}
