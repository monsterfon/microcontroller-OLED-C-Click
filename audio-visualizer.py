import time, random
import numpy as np
import sounddevice as sd
import board, busio, digitalio
from PIL import Image, ImageDraw
import adafruit_rgb_display.ssd1351 as ssd1351

# --------- Config ---------
WIDTH, HEIGHT = 128, 128   # Full SSD1351 resolution
BAR_WIDTH     = 4          # pixel width of each bar
FPS           = 30
BG_COLOR      = (0, 0, 0)  # black
BAR_AREA      = 96         # bar drawing height (bottom of screen)
RUN_TIME      = 10         # seconds to run

# --------- SPI / Display setup ---------
spi = busio.SPI(clock=board.SCK, MOSI=board.MOSI)
cs  = digitalio.DigitalInOut(board.D17)
dc  = digitalio.DigitalInOut(board.D25)
rst = digitalio.DigitalInOut(board.D24)
display = ssd1351.SSD1351(spi, cs=cs, dc=dc, rst=rst)

# --------- Drawing buffer ---------
image = Image.new("RGB", (WIDTH, HEIGHT))
draw  = ImageDraw.Draw(image)

# --------- Audio setup ---------
SAMPLE_RATE = 44100
BLOCK_SIZE  = 1024
VU_values = []   # history of loudness

def audio_callback(indata, outdata, frames, time_info, status):
    if status:
        print(status)

    # loopback: mic -> speakers
    outdata[:] = indata

    # compute loudness (RMS of current block)
    volume_norm = np.linalg.norm(indata) / np.sqrt(len(indata))
    # scale to [0..BAR_AREA]
    loudness = int(min(volume_norm * 10, 1.0) * BAR_AREA)

    # append to history
    VU_values.append(loudness)
    # keep enough bars to fill screen
    max_bars = WIDTH // BAR_WIDTH
    if len(VU_values) > max_bars:
        VU_values.pop(0)

# --------- Main loop ---------
try:
    frame_time = 1.0 / FPS
    start = time.time()

    with sd.Stream(channels=1,
                   samplerate=SAMPLE_RATE,
                   blocksize=BLOCK_SIZE,
                   callback=audio_callback):

        while time.time() - start < RUN_TIME:
            # Clear frame
            draw.rectangle((0, 0, WIDTH, HEIGHT), fill=BG_COLOR)

            # Draw history bars (left to right)
            for i, h in enumerate(VU_values):
                x0 = i * BAR_WIDTH
                y0 = HEIGHT - h
                color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                draw.rectangle((x0, y0, x0 + BAR_WIDTH - 1, HEIGHT - 1), fill=color)

            display.image(image)
            time.sleep(frame_time)

finally:
    # Clear display
    draw.rectangle((0, 0, WIDTH, HEIGHT), fill=BG_COLOR)
    display.image(image)

    # Release GPIOs
    cs.deinit()
    dc.deinit()
    rst.deinit()
    if spi.try_lock():
        spi.unlock()
