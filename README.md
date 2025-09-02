# Audio Visualizer with OLED C Click on Raspberry Pi

This project creates a real-time audio visualizer on a Raspberry Pi 3B using an OLED C Click display (96x96 px) and a USB microphone. It captures audio, plays it back through speakers, and shows a dynamic bar visualization of recent audio loudness.

## Features

- Initializes and controls the SSD1351 OLED display via SPI
- Real-time bar visualization of microphone audio
- Each bar shows the loudness of a previous audio interval
- Bars use random colors
- Audio loopback: microphone input is played through speakers

## Components

- **OLED C Click:** PSP27801, 25x25 mm, 96x96 px, SSD1351 driver
- **Raspberry Pi 3B:** running Raspberry Pi OS Lite (32-bit, headless)
- **Rode NT USB microphone**
- **Speakers**
- **SSH connection** from development machine to Raspberry Pi



## Wiring

Connect the OLED C Click display to the Raspberry Pi using SPI:

- **SPI Pins:**
    - `SCK` (Clock): Connect to Raspberry Pi SCK (GPIO 11)
    - `MOSI`: Connect to Raspberry Pi MOSI (GPIO 10)
- **Control Pins:**
    - `CS` (Chip Select): Connect to GPIO 17
    - `DC` (Data/Command): Connect to GPIO 25
    - `RST` (Reset): Connect to GPIO 24
- **Enable Pin:** Connect to 3.3V to power the display
- **Power:** Connect VCC to 3.3V
- **Ground:** Connect GND to Raspberry Pi GND



## Installation

**Update your Raspberry Pi:**
```sh
sudo apt update
sudo apt upgrade -y
```

**Install Python dependencies:**
```sh
sudo apt install python3-pip python3-pil python3-numpy python3-smbus git -y
pip3 install adafruit-circuitpython-ssd1351 sounddevice
```

**Clone this repository:**
```sh
git clone https://github.com/yourusername/audio-visualizer-oled.git
cd audio-visualizer-oled
```

**Run the program:**
```sh
python3 audio-visualizer.py
```

## Notes


- The display is 96x96 px, but the SSD1351 uses a 128x128 buffer, requiring custom memory mapping.
- Designed for headless Raspberry Pi OS Lite (no GUI).
