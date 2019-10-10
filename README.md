# RadarPi Procedures

## Set-Up

The instructions followed in this section serves as a tutorial or a guide to assemble the Audio Radar in its entirety. It will follow initial setup of test equipment used, assembly of the transmitting and receiving hardware and finally the software component of the project will be addressed.

### Raspberry Pi Setup

Complete setup instructions exist in many forms online however, this guide will serve the setup requirements needed only for the Audio Radar. Other functionality of the Raspberry Pi are ignored but it should be noted that it is not limited to only the functions that are used here. 

It is assumed that the following is available to the user:

- Raspberry Pi 3 or newer (Models older than the Raspberry Pi 3 will also work but a USB WiFi dongle will be required.) with Raspbian with Desktop already installed and SSH enabled (Numerous online resources exist to achieve this such as https://hackernoon.com/raspberry-pi-headless-install-462ccabd75d0)
- A computer with keyboard, mouse, monitor and SD card slot
- An ethernet cable
- A local area network with ethernet communication and WiFi.

The setup of the Raspberry Pi is covered extensively on the internet. (https://www.instructables.com/id/Ultimate-Raspberry-Pi-Configuration-Guide/) is a guide to set up the Raspberry Pi.

### Package Installation and Setup
The following packages need to be installed:

- Flask (http://mattrichardson.com/Raspberry-Pi-Flask/)
- PyGame (https://www.pygame.org/wiki/GettingStarted)
- $I^2S$ DAC Driver (https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/overview)
- RaspAP (https://raspberry-valley.azurewebsites.net/RaspAP-Wifi-Hotspot/)
- If the radar is implemented using something other than the Raspberry Pi, additional packages need to be installed: 
  - Numpy (https://scipy.org/install.html)
  - Scipy (https://scipy.org/install.html)
  - Matplotlib (https://scipy.org/install.html)

### Hardware Setup
The following links would help with setting up all the hardware needed for the radar.
- Microphone setup https://learn.adafruit.com/adafruit-agc-electret-microphone-amplifier-max9814/wiring-and-test)
- Speaker setup (https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/overview)

### Procedure
Clone repository that is linked in repository and copy contents to ' /home/pi/Documents/ '
Set up script to run \verb webapp.py  at start up of Raspberry Pi (https://www.instructables.com/id/Raspberry-Pi-Launch-Python-script-on-startup/)


## Usage Tutorial
The radar was designed to be as simple as possible to use. Therefore, after initial set-up, the only instructions on how to use the radar are as follows:

1. Power the Raspberry Pi with a minimum 1.5A power supply.
2. Wait for 10 seconds until the Wi-Fi network 'RadarPi' is registered. 
3. Scan the QR-code with your device or connect to the Wi-Fi manually.
4. Scan the other QR-code to visit the web page or enter the web address manually.
5. Select a mode that you want to use i.e. Continuous Wave or Pulsed-Doppler. Both have a technical and non-technical option. The technical version is intended only for advanced users.
6. Enter the parameters requested by the webpage.
7. Click 'submit' and wait for the resulting figure to appear. The Pulsed-Doppler has significant operations and may take longer than 8s.
8. Click on the 'Home' button to return to the landing page or select another mode from the navigation bar.
9. When done using the RadarPi, simply disconnect the power cable from the Raspberry Pi.


