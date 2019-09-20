#include "ADC.h"
#include "RingBuffer.h"

const int readPin = A0;

ADC *adc = new ADC(); // adc object

RingBuffer *buffer = new RingBuffer;


void setup() {

  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(readPin, INPUT); //pin 23 single ended

  Serial.begin(9600);

  // reference can be ADC_REFERENCE::REF_3V3, ADC_REFERENCE::REF_1V2 (not for Teensy LC) or ADC_REF_EXT.
  //adc->setReference(ADC_REFERENCE::REF_1V2, ADC_0); // change all 3.3 to 1.2 if you change the reference to 1V2

  adc->setAveraging(1); // set number of averages
  adc->setResolution(16); // set bits of resolution
  adc->setConversionSpeed(ADC_CONVERSION_SPEED::HIGH_SPEED); // change the conversion speed
  //VERY_LOW_SPEED, LOW_SPEED, MED_SPEED, HIGH_SPEED or VERY_HIGH_SPEED
  adc->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_HIGH_SPEED);

  // always call the compare functions after changing the resolution!
  //adc->enableCompare(1.0/3.3*adc->getMaxValue(ADC_0), 0, ADC_0); // measurement will be ready if value < 1.0V
  //adc->enableCompareRange(1.0*adc->getMaxValue(ADC_1)/3.3, 2.0*adc->getMaxValue(ADC_1)/3.3, 0, 1, ADC_1); // ready if value lies out of [1.0,2.0] V

  //adc->enableInterrupts(ADC_0);
}
uint32_t samples;
uint16_t value = 0;

void loop() {
  if (Serial.available()) {
    samples = Serial.parseInt();
    while (samples > 0) {
      //      value = adc->analogRead(readPin);

      //    buffer->write(value);
      //
      //    Serial.print("Buffer read:");
      Serial.println(adc->analogRead(readPin) * 3.3 / adc->getMaxValue(ADC_0),DEC);
      samples--;
      //    delay(100);}
    }
  }
}
