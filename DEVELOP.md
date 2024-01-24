## Use Python Virtual Environment

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

## Manage remote service
To install the software on your Raspberry PI, you must run the executable script: `install.sh`.   
The script create a new systemd service called `allsky-options`.  
If you develop in a remote client and if you want change the service `allsky-options` status, I suggest you use this workflow:
* copy the modified code from remote client to your Raspberry PI   
(You can use FTP. SFTP. Rsync, etc...)
* copy your remote host SSH key to your Raspberry PI  
`ssh-copy-id -i ~/.ssh/id_rsa.pub skycam@skycam-hostname-or-ip-address`
* try to execute a `allsky-options` service status check from remote host to your Raspberry PI:  
`ssh 'skycam@skycam-hostname-or-ip-address' sudo systemctl status allsky-options`