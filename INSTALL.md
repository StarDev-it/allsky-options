## INSTALL REQUIREMENTS
* Raspberry PI device
* Keyestudio KS0212 RPi Relay Shield (https://wiki.keyestudio.com/KS0212_keyestudio_RPI_4-channel_Relay_Shield)
* access to bash and sudo (or root) permissions
* Python version 3.9 or above

## INSTALL SERVICE
To full install the service run the script `sh install.sh`

## INSTALL ENVIRONMENT

The venv module provides support for creating lightweight “virtual environments” with their own site directories, optionally isolated from system site directories. Each virtual environment has its own Python binary (which matches the version of the binary that was used to create this environment) and can have its own independent set of installed Python packages in its site directories.   
To create a Python virtual environment run this command:
```
python -m venv venv
```

After the virtual environment installation, run the installation script:

```
sh install.sh
```

start virtual env
```
. venv/bin/activate
```

## 