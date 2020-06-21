sudo apt-get update
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.6
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 1
sudo apt-get install python3-apt
sudo apt-get install -y python3.6-distutils
python3.6 -m pip install --upgrade pip