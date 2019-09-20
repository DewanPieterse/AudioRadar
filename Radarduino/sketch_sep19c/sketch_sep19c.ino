#include <IntervalTimer.h>
#include <ADC.h>
#include <RingBuffer.h>    // normally use this line
//  #include "RingBuffer.h"     // I have RingBuffer in local directory
#include <math.h>

// The following from ADC_Module.h
// Other things to measure with the ADC that don't use external pins
// In my Teensy I read 1.22 V for the ADC_VREF_OUT (doesn't exist in Teensy LC), random values for ADC_BANDGAP,
// 3.3 V for ADC_VREFH and 0.0 V for ADC_VREFL.
#define ADC_TEMP_SENSOR     38 // 0.719 V at 25\BAC and slope of 1.715 mV/\BAC for Teensy 3.x and 0.716 V, 1.62 mV/\BAC for Teensy LC
#define ADC_VREF_OUT        39
#define ADC_BANDGAP         41
#define ADC_VREFH           42
#define ADC_VREFL           43

#define LED_POWER   13

// adc variables
ADC *adc = new ADC();  // adc object
ADC::Sync_result adcValues;
ADC_Module::ADC_Config ADCtemperatureConfig;
void setADCdifferential(), setADCsingle(); // setup ADC
bool startADC;


RingBuffer *temperatureRingBuffer1 = new RingBuffer(), *temperatureRingBuffer2 = new RingBuffer();

const float Fs = 128;                        // force integer sampling rate and a multiple of Fw (assuming Fw <= 3 decimal places

// Timer setup and variables to call interrupt for ADC initialization
IntervalTimer samplingTimer; // interrupt timer for sampling
int timerReturnValue, timerPriorityReturnValue;  // timer return values for testing


elapsedMicros ISRtime = 0;
uint32_t ISRtime01;

uint32_t temperature1Raw, temperature2Raw;

void setup() {
  // initialize the light & pins
  pinMode(LED_POWER, OUTPUT);
  pinMode(A2, INPUT);
  pinMode(A3, INPUT);
  pinMode(A4, INPUT);
  pinMode(A5, INPUT);
  pinMode(A10, INPUT);
  pinMode(A12, INPUT);
  pinMode(38, INPUT);


  Serial.begin(9600);  // for debugging or datalogging
  delay(2000);
  Serial.println("Starting Serial Port");

  // set ADC parameters

  Serial.print("ISR Frequency  ");
  Serial.println(Fs);

  // set interrupt timer with sampling time in microseconds
  timerReturnValue = samplingTimer.begin(sampleBeginISR, 1e6 / Fs);

  // enable adc interrupts just before the main loop
  adc->enableInterrupts();  // call interrupt to read value upon completion of ADC
}


void sampleBeginISR(void) {
  noInterrupts();
  // Start ADC
  setADCsingle1();           // set ADC for single-ended measurement
  Serial.print("StartADC0 a - Successful - ");
  attachInterruptVector(IRQ_ADC0, singleReadADC0_isr1);
  startADC = adc->startSingleRead(38, 0);
  Serial.println(startADC);
  interrupts();
}

void sample2isr() {
  noInterrupts();
  setADCsingle2();           // set ADC for single-ended measurement
  Serial.print("\tStartADC0 b - Successful - ");
  attachInterruptVector(IRQ_ADC0, singleReadADC0_isr2);
  startADC = adc->startSingleRead(38, 0);
  Serial.println(startADC);
  interrupts();
}


// Single-ended read data and reset for differential measurement
void singleReadADC0_isr1() {
  // put single-ended values into a ring buffer
  noInterrupts();
  Serial.print("\tStartADC0 b - Successful - ");
  temperatureRingBuffer1->write(adc->readSingle());
  attachInterruptVector(IRQ_ADC0, singleReadADC0_isr2);
  startADC = adc->startSingleRead(38, 0);
  Serial.println(startADC);
  Serial.println("Read temperature 1 ADC subroutine executed");
  interrupts();
}

// Single-ended read data and reset for differential measurement
void singleReadADC0_isr2() {
  // put single-ended values into a ring buffer
  noInterrupts();
  temperatureRingBuffer2->write(adc->readSingle());
  interrupts();
  Serial.println("Read Temperature 2 ADC subroutine executed");
}

void setADCsingle1() {
  Serial.println("setADCsingle 1 subroutine executed");
  // ADC 0
  // one of ADC_REF_3V3, ADC_REF_1V2, ADC_REF_EXT.
  //adc->setReference(ADC_REF_1V2, ADC_0); // change all 3.3 to 1.2 if you change the reference to 1V2

  adc->setReference(ADC_REF_1V2, ADC_0);  //ADC_REF_3V3, ADC_REF_1V2, ADC_REF_EXT
  //  adc->enablePGA(1, ADC_0); // options are 1, 2, 4, 8, 16, 32 or 64
  adc->setAveraging(64, ADC_0);
  adc->setResolution(ADC_MED_SPEED, ADC_0); // see ADC.h
  // one of ADC_VERY_LOW_SPEED, ADC_LOW_SPEED, ADC_MED_SPEED, ADC_HIGH_SPEED_16BITS, ADC_HIGH_SPEED, ADC_VERY_HIGH_SPEED
  adc->setConversionSpeed(ADC_MED_SPEED, ADC_0); // see ADC.h for options
  // one of ADC_VERY_LOW_SPEED, ADC_LOW_SPEED, ADC_MED_SPEED, ADC_HIGH_SPEED, ADC_VERY_HIGH_SPEED
  adc->setSamplingSpeed(ADC_MED_SPEED, ADC_0); // see ADC.h for options

  // save configuration
  // ADC_Module::saveConfig(*ADCtemperatureConfig);
}

void setADCsingle2() {
  Serial.println("setADCsingle 2 subroutine executed");
  // ADC 0
  // one of ADC_REF_3V3, ADC_REF_1V2, ADC_REF_EXT.
  //adc->setReference(ADC_REF_1V2, ADC_0); // change all 3.3 to 1.2 if you change the reference to 1V2

  adc->setReference(ADC_REF_1V2, ADC_0);  //ADC_REF_3V3, ADC_REF_1V2, ADC_REF_EXT
  //  adc->enablePGA(1, ADC_0); // options are 1, 2, 4, 8, 16, 32 or 64
  adc->setAveraging(1, ADC_0);
  adc->setResolution(ADC_VERY_HIGH_SPEED, ADC_0); // see ADC.h
  // one of ADC_VERY_LOW_SPEED, ADC_LOW_SPEED, ADC_MED_SPEED, ADC_HIGH_SPEED_16BITS, ADC_HIGH_SPEED, ADC_VERY_HIGH_SPEED
  adc->setConversionSpeed(ADC_VERY_HIGH_SPEED, ADC_0); // see ADC.h for options
  // one of ADC_VERY_LOW_SPEED, ADC_LOW_SPEED, ADC_MED_SPEED, ADC_HIGH_SPEED, ADC_VERY_HIGH_SPEED
  adc->setSamplingSpeed(ADC_MED_SPEED, ADC_0); // see ADC.h for options

  // save configuration
  // ADC_Module::saveConfig(*ADCtemperatureConfig);
}



void loop() {


  // check temperature only if the temperature ring buffer is not empty
  if (!temperatureRingBuffer2->isEmpty()) {

    // read data from ringBuffer
    noInterrupts();
    temperature1Raw = temperatureRingBuffer1->read();
    temperature2Raw = temperatureRingBuffer2->read();
    interrupts();

    Serial.print("Read Ring Buffer");
    Serial.print("\t");
    Serial.print(temperatureRingBuffer1->isEmpty());
    Serial.print("\t");
    Serial.print(temperature1Raw);
    Serial.print("\t");
    Serial.println(temperature2Raw);

  }
}
