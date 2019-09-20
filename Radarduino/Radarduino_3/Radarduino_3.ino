/* Example for analogRead
   You can change the number of averages, bits of resolution and also the comparison value or range.
*/

#include <ADC.h>
#include "RingBuffer.h"

const int readPin = A0; // ADC0

ADC *adc = new ADC(); // adc object;
RingBuffer *buffer = new RingBuffer;

void setup() {

  //  pinMode(LED_BUILTIN, OUTPUT);
  //  pinMode(readPin, INPUT);

  Serial.begin(500000);

  //  Serial.println("Begin setup");

  ///// ADC0 ////
  // reference can be ADC_REFERENCE::REF_3V3, ADC_REFERENCE::REF_1V2 (not for Teensy LC) or ADC_REFERENCE::REF_EXT.
  //adc->setReference(ADC_REFERENCE::REF_1V2, ADC_0); // change all 3.3 to 1.2 if you change the reference to 1V2

  adc->setAveraging(1); // set number of averages
  adc->setResolution(16); // set bits of resolution

  // it can be any of the ADC_CONVERSION_SPEED enum: VERY_LOW_SPEED, LOW_SPEED, MED_SPEED, HIGH_SPEED_16BITS, HIGH_SPEED or VERY_HIGH_SPEED
  // see the documentation for more information
  // additionally the conversion speed can also be ADACK_2_4, ADACK_4_0, ADACK_5_2 and ADACK_6_2,
  // where the numbers are the frequency of the ADC clock in MHz and are independent on the bus speed.
  adc->setConversionSpeed(ADC_CONVERSION_SPEED::VERY_HIGH_SPEED); // change the conversion speed
  // it can be any of the ADC_MED_SPEED enum: VERY_LOW_SPEED, LOW_SPEED, MED_SPEED, HIGH_SPEED or VERY_HIGH_SPEED
  adc->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_HIGH_SPEED); // change the sampling speed

  // always call the compare functions after changing the resolution!
  //adc->enableCompare(1.0/3.3*adc->getMaxValue(ADC_0), 0, ADC_0); // measurement will be ready if value < 1.0V
  //adc->enableCompareRange(1.0*adc->getMaxValue(ADC_0)/3.3, 2.0*adc->getMaxValue(ADC_0)/3.3, 0, 1, ADC_0); // ready if value lies out of [1.0,2.0] V

  //  Serial.println("End setup");

}

uint16_t value;
int samples;
char tic, toc;
char t;
uint32_t freq = 44100;
char on = 0;
int c;

void loop() {

  if (Serial.available()) {

    samples = Serial.parseInt();
    if (samples > 0) {
      //      adc->adc0->stopPDB();
      //      adc->adc0->startSingleRead(readPin); // call this to setup everything before the pdb starts,
      adc->enableInterrupts(ADC_0);
      //      adc->adc0->startPDB(freq); //frequency in Hz

      //    while(audio < samples){
      //      value = adc->readSingle(ADC_0); // the unsigned is necessary for 16 bits,
      //      audio.append = (value * 3.3 / adc->getMaxValue(ADC_0), DEC);
      //    }
      //
      //      for (int i = 0; i < samples; i++) {
      //        value = (uint16_t)adc->readSingle(ADC_0); // the unsigned is necessary for 16 bits, otherwise values larger than 3.3/2 V are negative!
      //        //        buffer->write(value);
      //        //        audio[i] = (buffer->read() * 3.3 / adc->getMaxValue(), DEC);
      //        //        Serial.println(buffer->read() * 3.3 / adc->getMaxValue(), DEC);
      //        Serial.println(value * 3.3 / adc->getMaxValue(), DEC);
    }
    adc->disableInterrupts(ADC_0);

    //    else if (c == 'r') {
    //      Serial.println(adc->adc0->getPDBFrequency());
    //      for (char j; j < samples; j++) {
    //        Serial.println(audio[j]);
    //      }
    //    }
  }
}


// If you enable interrupts make sure to call readSingle() to clear the interrupt.
void adc0_isr() {
  if (samples > 0) {
    value = adc->readSingle();
    Serial.println(value * 3.3 / adc->getMaxValue());
//    digitalWriteFast(LED_BUILTIN, !digitalReadFast(LED_BUILTIN) );
    samples--;
  }
}

// pdb interrupt is enabled in case you need it.
void pdb_isr(void) {
  PDB0_SC &= ~PDB_SC_PDBIF; // clear interrupt
  //digitalWriteFast(LED_BUILTIN, !digitalReadFast(LED_BUILTIN) );
}
