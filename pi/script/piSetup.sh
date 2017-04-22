
#!/bin/bash

cd ~
echo "**************************************************"
echo "****************   UPDATING   ********************"
echo "**************************************************"
sudo apt-get update -y

echo "**************************************************"
echo "****************  INSTALLING PACKAGES   **********"
echo "**************************************************"
sudo apt-get install libatlas-base-dev gfortran -y --force-yes
sudo apt-get install python2.7-dev python3-dev python3.4-dev -y --force-yes

echo "********************************************************"
echo "****************   INSTALLING PIP   ********************"
echo "********************************************************"
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py

echo "********************************************************************"
echo "****************   INSTALING PYTHON3 PACKAGES   ********************"
echo "********************************************************************"
sudo pip3 install numpy
sudo pip3 install imutils
sudo apt-get install python-tk
#sudo pip3 install scipy

echo "********************************************************************"
echo "****************   INSTALLING PYTHON2 PACKAGES  ********************"
echo "********************************************************************"
sudo apt-get install i2c-tools python-smbus python-opengl python-pygame python-webpy -y

echo "*************************************************************"
echo "****************   INSTALLING VNC SERVER ********************"
echo "*************************************************************"
sudo apt-get install tightvncserver -y


echo "the installer script has completed."
passwd
