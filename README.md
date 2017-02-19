# sound-level-detector

## Setup

* [ ] `sudo apt-get install screen`

* [ ] Apply screenrc

    ```
    cd /etc/
    sudo rm screenrc
    sudo wget https://raw.githubusercontent.com/testCloud/sound-level-detector/master/screenrc
    ```
* [ ] `sudo apt-get install ruby`

* [ ] `sudo apt-get install ruby-dev`

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

### Activate I2C pins

* execute `i2cdetect -y 1`

    Unless you see this:

    ```         0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- 27 -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
    ```

    do:

    `sudo usermod -aG i2c pi`

    then edit:

    uncomment the line `dtparam=i2c_arm=on` in /boot/config.txt

    ```sudo su
    echo i2c-dev >> /etc/modules
    ```

    `sudo reboot`

    `sudo apt-get install python3-smbus`

    `ls /dev/` and check if you see "i2c-1"

### Almost done!

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