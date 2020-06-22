# Install Python3.7 in a virtual environment
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:jonathonf/python-3.7
sudo apt update
sudo apt install -y python3.7
sudo apt install -y python3.7-dev
sudo apt install -y python3-pip
sudo apt install -y python3.7-venv
sudo apt install -y -y python3-opencv

# Install Face Recognition libraries
pip3 install numpy
pip3 install pillow
pip3 install dlib
sudo apt-get -y install cmake
pip3 install face_recognition
pip3 install opencv-contrib-python==4.1.0.25

# Install RPi support in Virtual Environment
pip3 install RPi.GPIO

# Install Support Libraries
sudo apt-get install -y git libgtk2.0-dev pkg-config libavcodec-dev
sudo apt-get install -y libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
sudo apt-get install -y libatlas-base-dev
sudo apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev -y
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev -y
sudo apt-get install -y libgtk2.0-dev libgtk-3-dev -y
sudo apt-get install -y libavformat-dev libswscale-dev openexr libopenexr-dev
sudo apt-get install -y libqt4-dev
sudo apt-get install -y libgstreamer0.10-0-dbg libgstreamer0.10-0 libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev
sudo apt-get install -y qt5-default pyqt5-dev pyqt5-dev-tools