#include <SD.h>
#include <SPI.h>
#include <ADC.h>
#include "RingBuffer.h"


const int chipSelect = BUILTIN_SDCARD;
const int readPin = A0;
const int ledPin = LED_BUILTIN;

ADC *adc = new ADC(); // adc object;
RingBuffer *buffer0 = new RingBuffer; // buffers to store the values
RingBuffer *buffer1 = new RingBuffer;

void setup()
{
  pinMode(readPin, INPUT);
  pinMode(ledPin, OUTPUT); // led blinks every loop

  // Open serial communications and wait for port to open:
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for Leonardo only
  }


  Serial.print("Initializing SD card...");

  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
    // don't do anything more:
    return;
  }
  if (SD.exists("datalog.txt")) {
    Serial.println("datalog.txt exists.");
    Serial.println("Removing datalog.txt...");
    SD.remove("datalog.txt");
  }
  else {
    Serial.println("datalog.txt doesn't exist.");
  }
  Serial.println("card initialized.");
  Serial.println("Begin ADC setup");

  adc->setAveraging(1); // set number of averages
  adc->setResolution(16); // set bits of resolution
  adc->setConversionSpeed(ADC_CONVERSION_SPEED::VERY_LOW_SPEED); // change the conversion speed
  // it can be any of the ADC_MED_SPEED enum: VERY_LOW_SPEED, LOW_SPEED, MED_SPEED, HIGH_SPEED or VERY_HIGH_SPEED
  adc->setSamplingSpeed(ADC_SAMPLING_SPEED::VERY_LOW_SPEED);


  delay(500);

  Serial.println("End setup");
}
uint16_t value;
uint32_t samples;
uint32_t freq = 44100;
String dataString = "";
File dataFile;

void loop()
{
  if (Serial.available()) {

    samples = Serial.parseInt();

    if (samples > 0) {

      adc->enableInterrupts(ADC_0);
      dataFile = SD.open("datalog.txt", FILE_WRITE);

      while (samples > 0) {


        //        value = (uint16_t)buffer0->read() * 3.3 / adc->getMaxValue();
        //        Serial.println(buffer0->read() * 3.3 / adc->getMaxValue());
        dataFile.println(buffer0->read() * 3.3 / adc->getMaxValue());


        samples--;
      }
    }
    adc->disableInterrupts(ADC_0);
    dataFile.close();

    //    if (!buffer1->isEmpty()) { // read the values in the buffer
    //      Serial.print("Read pin 1: ");
    //      Serial.println(buffer1->read() * 3.3 / adc->getMaxValue());
    //      //Serial.println("New value!");
    //    }
  }
}





void adc0_isr() {

  uint8_t pin = ADC::sc1a2channelADC0[ADC0_SC1A & ADC_SC1A_CHANNELS]; // the bits 0-4 of ADC0_SC1A have the channel

  // add value to correct buffer
  if (pin == readPin) {

    digitalWriteFast(ledPin, HIGH);
    buffer0->write(adc->readSingle());
    digitalWriteFast(ledPin, LOW);

  }
  //  if (adc->adc0->isConverting()) {
  //    digitalWriteFast(LED_BUILTIN, 1);
  //  }
  //  else { // clear interrupt anyway
  //    adc->readSingle();
  //  }
  digitalWriteFast(ledPin, LOW);

  // restore ADC config if it was in use before being interrupted by the analog timer
  //  if (adc->adc0->adcWasInUse) {
  //    // restore ADC config, and restart conversion
  //    adc->adc0->loadConfig(&adc->adc0->adc_config);
  //    // avoid a conversion started by this isr to repeat itself
  //    adc->adc0->adcWasInUse = false;
  //  }
}
