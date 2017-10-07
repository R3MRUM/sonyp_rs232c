# SonyHWXXES
A Python3 class used for controlling a Sony VPL-HWXXES projector via serial connection. This has only been tested on a Sony VPL-HW40ES projector but should work for similar models (VPL-HW58ES, VPL-HW55ES, VPL-HW50ES, VPL-HW40ES, VPL-HW35ES). Since this has been tested in extremely limited capacity, use at your own risk!

# Installation
```
> pip install sonyp_rs232c
```

# My Setup
* Sony VPL-HW40ES Projector
* Windows 10 HTPC
* <a href="https://www.amazon.com/gp/product/B002TLT95K/">Syba PCI-Express x1 4 Port RS232 Serial Card</a>
* 2x <a href="https://www.monoprice.com/product?p_id=1153">DB9F/RJ-45 Modular Adapter</a>
* 50' Cat5e Ethernet Cable

# Files
* **SonyHWXXES.py** - the class that you will need to import into your python script (ie. toggle_power.py) to enable communication with your Sony projector.
* **toggle_power.py** - an example script that leverages the SonyHWXXES.py class to turn your projector on an off. You should just need to modify the port specified in the script to match whatever port is correct for your setup.

# Execution
```
C:\SonyHWXXES>python toggle_power.py
Initiating Serial Object
Serial Object Initiated
Turning Power On
Phase: Standby
Phase: Start Up
Phase: Startup Lamp
Phase: Power On

C:\SonyHWXXES>python toggle_power.py
Initiating Serial Object
Serial Object Initiated
Turning Power Off
Phase: Cooling1
Phase: Cooling2
Phase: Standby
Phase: Power Off
```

Note that shutting down the projector takes ~30 seconds due to the cool down.
