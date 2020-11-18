# PiPlateBrewery
Brewery controller software for a Raspberry Pi coupled with a DAQC2 and THERMOplate from Pi-Plates.  The interface is designed for a screen resolution of 1280x800.

# Setup
1. Update your Raspberry Pi `sudo apt-get update -y` followed by `sudo apt-get upgrade -y`
2. Enable SPI on the Raspberry Pi.  This can be done either via the GUI or `sudo raspi-config`
3. Install the Pi-Plates python module `sudo pip install Pi-Plates`
4. Install Apache and PHP `sudo apt-get install apache2 php libapache2-mod-php -y`
5. Configure Apache to run as pi: 
    - `sudo nano /etc/apache2/envars`  
    - Change `export APACHE_RUN_USER=www-data` to `export APACHE_RUN_USER=pi`
    - Change `export APACHE_RUN_GROUP=www-data` to `export APACHE_RUN_GROUP=pi`
6. Configure the 'pi' user to not require a password for sudo
    - `sudo visudo`
    - Change the `pi ALL=(ALL:ALL) ALL` to `pi ALL=(ALL) NOPASSWD:ALL`
7. Copy project files to /var/www/html
8. Configure the Raspberry pi to boot into chromium in fullscreen and open UI
    - `sudo nano /home/pi/.config/lxsession/LXDE-pi/autostart`
    - Create the file with the following lines:
    ```@unclutter
    @xset s off
    @xset s noblank
    @xset -dpms

    @/usr/bin/chromium-browser --start-fullscreen http://localhost```
9. Reboot `sudo restart now`
The Raspberry Pi should reboot, Chromium should open fullscreen and you should see the brewery interface.


# Configuration
You will need to create a conf.json or rename conf_template.json to conf.json file in the py folder on your device to utilize the Azure logging function.  Format of the file should be:
```
{	
    "WorkspaceId": "",	
    "WorkspaceKey": "",	
    "LogName": ""	
}
```
- WorkspaceId can be found in the Advanced Settings of your Log Analytics instance.  
- Workspace Key can be found in the same location and can be either the Primary or Secondary key.  
- Log Name is the name that entries will appear as once ingested into Log Analytics.  Log Analytics will automatically append '\_CL' to the end of the log name.
