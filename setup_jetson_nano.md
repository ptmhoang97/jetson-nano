# Setup Jetson Nano

**1. Flash and boot:**\
https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit

**2. Install NoMachine:**
```
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
Section "Screen"
Identifier "Screen0"
Monitor    "Monitor0"
    SubSection "Display"
    Viewport   0 0
    Modes "1920x1080"
    Depth   24 
    Virtual 1920 1080
EndSubSection
EndSection
```
- Modify "1920" and "1080" based on your monitor's resolution.

**5. Save RAM:**
```
# Check RAM before
free -h

# Switch to lightdm
sudo dpkg-reconfigure lightdm

# Check RAM after
free -h
```

**6. Add swap memory:**
```
# Check swap memory before
free -h

# Create swap memory
sudo fallocate -l 4G /var/swapfile
sudo chmod 600 /var/swapfile
sudo mkswap /var/swapfile
sudo swapon /var/swapfile
sudo bash -c 'echo "/var/swapfile swap swap defaults 0 0" >> /etc/fstab'

# Check swap memory after
free -h
```
