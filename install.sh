#!/bin/bash

IS_RASPBERRY=`cat /etc/os-release | grep "ID=raspbian" | wc -l`
ABS_PATH=`pwd`
echo $ABS_PATH

print () {
  if [ $IS_RASPBERRY -eq 1 ]
  then
    echo "\033[32m$1\e[0m"
  else
    echo -e "\033[32m$1\e[0m"
  fi
}

print "========================"
print "Raspberry PI OS version:"
cat /etc/os-release
print "========================"

# Activate Python virtual environment
print "Install and Activate Python VENV..."
if [ ! -d "venv" ]; then
  python -m venv venv
fi

# Use Python virtual environment
. venv/bin/activate

# Upgrade PIP
print "Install/Upgrade PIP..."
python -m pip install --upgrade pip

# Install all dependencies
print "Install dependencies..."
pip install pyyaml
pip install RPi.GPIO
pip install gpiozero

# Set test roboscope server as executable
print "Make server script executable..."
chmod +x start.sh
chmod +x server.py

# Set systemd service
if [ $IS_RASPBERRY -eq 1 ]
then
  print "Create service..."
  rm -f script/allsky-options.service
  cp script/allsky-options.service.example script/allsky-options.service
  sed -i "s@WORKING_DIR@${ABS_PATH}@g" script/allsky-options.service
  sudo systemctl link ./script/allsky-options.service
  print "Enable service..."
  sudo systemctl enable allsky-options
  print "Start service..."
  sudo systemctl start allsky-options
else
  print "You can install the service only on a Raspberry device!"
fi


