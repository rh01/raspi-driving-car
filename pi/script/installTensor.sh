# sudo apt-get install python3-dev -y
# wget https://github.com/samjabrahams/tensorflow-on-raspberry-pi/releases/download/v1.0.0/tensorflow-1.0.0-cp34-cp34m-linux_armv7l.whl
# sudo pip3 install tensorflow-1.0.0-cp34-cp34m-linux_armv7l.whl


sudo apt-get update

# For Python 2.7
sudo apt-get install python-pip python-dev -y

# For Python 2.7
wget https://github.com/samjabrahams/tensorflow-on-raspberry-pi/releases/download/v1.0.1/tensorflow-1.0.1-cp27-none-linux_armv7l.whl

sudo pip install tensorflow-1.0.1-cp27-none-linux_armv7l.whl -y

# For Python 2.7
sudo pip uninstall mock -y
sudo pip install mock -y

# # for python3.4
# sudo apt-get install python3-pip python3-dev


# # For Python 3.4
# wget https://github.com/samjabrahams/tensorflow-on-raspberry-pi/releases/download/v1.0.1/tensorflow-1.0.1-cp34-cp34m-linux_armv7l.whl
# sudo pip3 install tensorflow-1.0.1-cp34-cp34m-linux_armv7l.whl

# # For Python 3.3+
# sudo pip3 uninstall mock
# sudo pip3 install mock