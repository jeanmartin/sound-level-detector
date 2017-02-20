# sound-level-detector

## Files and their purpose

### `app.py`

This is the main file running the event listener: It initializes all the other classes and then
listens to all inputs from buttons & rotary encoders.

You run it with: `python3 app.py`

### `event_publisher.py`

Waits for events and publishes them to [kraken](https://github.com/testCloud/kraken).

### `screen_controller.py`

Waits for messages to display on the screen.

Imports `LCD1602.py`

### `sound_listener.py`

Opens the mic and listens to the volume. Triggers stuff once the threshold is reached.

### `led_controller.py`

Controls the LED strip. Provides methods to switch it on and off.

### The `experiments` folder

... is for ... well, experiments!


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

    ```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
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

    then edit `/boot/config.txt`: uncomment the line `dtparam=i2c_arm=on`

    ```
    sudo su
    echo i2c-dev >> /etc/modules
    ```

    `sudo reboot`

    `sudo apt-get install python3-smbus`

    `ls /dev/` and check if you see "i2c-1"

### Almost done!

* [ ] clone the repo into ~/SLD

    ```
    cd ~
    git clone https://github.com/testCloud/sound-level-detector.git SLD
    ```

* [ ] start pigpiod

    `sudo pigpiod`

* [ ] make sure the microphone is plugged in

* [ ] start the app

    ```
    cd ~/SLD
    python3 app.py
    ```

    If you get something about "recource busy" try unplugging and plugging in the mic.
