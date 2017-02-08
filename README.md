# sound-level-detector

## Setup

* [ ] `sudo apt-get install ruby`

* [ ] `sudo gem install god`

* [ ] install [pigpio](http://abyz.co.uk/rpi/pigpio/download.html)

    ```
    wget abyz.co.uk/rpi/pigpio/pigpio.zip
    unzip pigpio.zip
    cd PIGPIO
    make -j4
    sudo make install
    ```
* [ ] install [RPi.GPIO](https://pypi.python.org/pypi/RPi.GPIO)

* [ ] `sudo apt-get install python3-rpi.gpio`

* [ ] `sudo pip3 install requests-futures`

* [ ] `sudo pip3 install alsaaudio`

* [ ] put detect_sound_level.py into ~/sound

    ```
    mkdir ~/sound
    cd ~/sound
    wget https://raw.githubusercontent.com/testCloud/sound-level-detector/master/detect_sound_level.py
    ```
* [ ] start pigpiod

    ``sudo pigpiod``

* [ ] make sure the microphone is plugged in

* [ ] start detect_sound_level.py

    ```
    cd ~/sound
    python3 detect_sound_level.py
    ```
