install-deps:
	chmod a+x install_python37_venv.sh
	./install_python37_venv.sh
	install-pyqt5-rpi

# Correct way to install PyQt5 on RPi (a little painful)
install-pyqt5-rpi:
	# Install SIP
	wget https://www.riverbankcomputing.com/static/Downloads/sip/4.19/sip-4.19.tar.gz
	tar -xzvf sip-4.19.1.tar.gz
	cd sip-4.19/
	python3 configure.py
	make 
	sudo make install
    cd ../

	# Install PyQt5
	pip3 install PyQt-builder
	pip3 install PyQt5-sip
	wget https://files.pythonhosted.org/packages/8c/90/82c62bbbadcca98e8c6fa84f1a638de1ed1c89e85368241e9cc43fcbc320/PyQt5-5.15.0.tar.gz
	tar -xzvf PyQt5-5.15.0.tar.gz
	cd PyQt5-5.15.0/
	python3 configure.py
	make 
	sudo make install

run:
	@python3 src/face_recognizer.py