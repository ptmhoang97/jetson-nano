# Setup Jetson Nano

**1. Flash and boot:**
- Dowload JetPack 4.5:
https://developer.nvidia.com/jetson-nano-sd-card-image-45
- And follow tutorial:
https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit

**2. Install NoMachine on Jetson Nano:**
```
sudo apt-get update
wget https://download.nomachine.com/download/7.6/Arm/nomachine_7.6.2_3_arm64.deb
sudo dpkg -i nomachine_7.6.2_3_arm64.deb
```

**3. Enable automatic login (fix black screen when remote):**
```
sudo vim /etc/gdm3/custom.conf
```
- Remove character # at line AutomaticLoginEnable and AutomaticLogin. Change user1 to your user name.\
![image](https://user-images.githubusercontent.com/53186326/135458006-f24f78a6-7888-453f-aa33-82cbdc0f95a0.png)
- Edit with vim:
  - Press 'i' to enable edit mode.
  - Press 'Esc' to disable edit mode.
  - Press ':wq' to save and quit.
  - Press ':q' to quit without modify.
  - Press ':q!' to quit with modify but don't want to save.

**4. Change resolution (fix small screen):**
```
sudo vim /etc/X11/xorg.conf
```
- Add these lines at the end of file:
```
# Modify "Modes" and "Virtual" based on your monitor's resolution.
Section "Screen"
Identifier "Screen0"
Monitor    "Monitor0"
    SubSection "Display"
    Viewport   0 0
    Modes "1366x768"
    Depth   24 
    Virtual 1366 768
EndSubSection
EndSection
```
```
sudo reboot
```

**5. Install NoMachine on Window PC:**
- Dowload NoMachine from https://www.nomachine.com/
- Remote to Jetson Nano.

**6. Save RAM:**
```
# Check RAM before
free -h

# Switch to lightdm
sudo dpkg-reconfigure lightdm

# Reboot
sudo reboot

# Check RAM after
free -h
```

**7. Install pip3:**
```
sudo apt-get -y install python3-pip
```

**8. Install Jetson Stats:**
```
sudo -H pip3 install -U jetson-stats
sudo jtop
```

**9. Add swap memory:**\
![image](https://user-images.githubusercontent.com/53186326/135964552-8cd2d618-e49d-412f-b8b3-cc00ccbb1ce9.png)

**10. Boost clock:**\
![image](https://user-images.githubusercontent.com/53186326/135964578-93d3cc25-a118-49d4-aa53-bb19c828f758.png)

**11. Create shortcut key for LXTerminal:**
- Use vim to open lxde-rc.xml:
<!---->
    sudo vim cd ~/.config/openbox/lxde-rc.xml  
- Type "/keyboard" and press "Enter" for searching tag \<keyboard\>  .
- Press "i" for edit, copy below code to position which inside tag \<keyboard\>:  
<!-- Launch LXTerminal with Ctrl+Alt+t-->
    <keybind key="C-A-t">
      <action name="Execute">
        <command>lxterminal</command>
      </action>
    </keybind>
- Press "Esc" for stopping edit.
- Type ":wq" for quit and save file.
- sudo reboot ( After login, use command "Ctrl+Atl+t" to open LXTerminal).

