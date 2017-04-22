#!/bin/bash

cd ~

echo "**************************************************"
echo "****************  UPDATING   *********************"
echo "**************************************************"
sudo apt-get update -y

echo "**************************************************"
echo "****************  INSTALLING PACKAGES   **********"
echo "**************************************************"
sudo apt-get install build-essential cmake pkg-config -y --force-yes
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev -y --force-yes
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev -y --force-yes
sudo apt-get install libxvidcore-dev libx264-dev -y --force-yes
sudo apt-get install libgtk2.0-dev -y --force-yes


echo "**************************************************"
echo "**********  INSTALLING PYTHON PACKAGE   **********"
echo "**************************************************"
sudo apt-get install python3-numpy -y
sudo apt-get install python3-matplotlib -y
sudo apt-get install python3-scipy -y
sudo apt-get install python3-skimage -y

echo "**************************************************"
echo "****************  GETTING OPENCV   ***************"
echo "**************************************************"
wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.1.0.zip
wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.1.0.zip
unzip opencv.zip
unzip opencv_contrib.zip
cd ~/opencv-3.1.0/
mkdir build
cd build

echo "**************************************************"
echo "****************  BUILDING OPENCV   **************"
echo "**************************************************"
cmake -D CMAKE_BUILD_TYPE=RELEASE \
-D CMAKE_INSTALL_PREFIX=/usr/local \
-D INSTALL_C_EXAMPLES=OFF \
-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.1.0/modules \
-D BUILD_EXAMPLES=ON ..

echo "**************************************************"
echo "****************  MAKING OPENCV   **********"
echo "**************************************************"
make
sudo make install
sudo ldconfig
echo "your cv version is (should be 3.1.0):"
python3 -c 'import cv2; print("Installed OpenCV Version: "); print(cv2.__version__)'
echo "the installer script has completed."
