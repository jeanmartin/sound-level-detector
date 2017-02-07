# sound-level-detector

## Setup

1. [ ] install [pigpio](http://abyz.co.uk/rpi/pigpio/download.html)

    ```
    wget abyz.co.uk/rpi/pigpio/pigpio.zip
    unzip pigpio.zip
    cd PIGPIO
    make -j4
    sudo make install
    ```
2. [ ] install [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO)

   ``sudo apt-get install python3-rpi.gpio``

3. [ ] put detect_sound_level.py into ~/sound

    ```
    mkdir ~/sound
    cd ~/sound
    wget https://raw.githubusercontent.com/testCloud/sound-level-detector/master/detect_sound_level.py
    ```
4. [ ] start pigpiod

    ``sudo pigpiod``

5. [ ] make sure the microphone is plugged in

6. [ ] start detect_sound_level.py

    ```
    cd ~/sound
    python3 detect_sound_level.py
    ```
