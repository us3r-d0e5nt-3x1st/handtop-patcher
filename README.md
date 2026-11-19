# 0. Handtop Patcher :
Handtop Patcher aims to be a port of the Handtop project by junsulee119 to the whole family of Allwinner H700 based Anbernic retro consoles.

<img width="772" height="432" alt="image" src="https://github.com/user-attachments/assets/95ce9099-9e3e-4ff5-99ae-3836d6af56b7" />

# 1. How to download the project :
You can either download prebuilt images or patch it yourself, go to the releases tab and download necessary files. Pay attention to the version you need for your console (DDR3/DDR4).

# 2. Patching it yourself :
You will need the patcher program and an image of the original Handtop downloaded from the junsulee119's repository. You just unpack the patcher archive, place the .img.xz file in the root directory of it (next to the patcher.sh), open a terminal there and run ./patcher.sh, or you could just run it from GUI. The program was poorly written on Debian, and i tested it by running it through su (as superuser), so try that if something doesn't work.

# 3. Flashing the image :
You will need an image (.img or .img.xz) and some kind of a program to flash it to the SD card (i recommend raspberry pi imager, it's included in the patcher archive if you want to use it). Please skip the image verification as quickly as possible, it's a modified image and it will fail it, and possibly break the installation in the process (it did for me).

# 4. Choosing the DTB file :
! If you have RG40XX-H with the V2 panel, you don't need to do that, it's the default one choosen !
After installation, you will need to mount the flashed SD card in your PC and go to the Boot partition and replace the dtb.img file with one available in the /device_trees folder, you need to place the one matching your device in the main directory of the boot partition and rename it to dtb.img . 

# 5. What is exactly being patched here :
It unpacks the image and mounts it as a loop0 to make it possible to write to it, then replaces DTB files in the boot partition for all the files taken from the Rocknix image, cleanes up some unnecessary files there and replaces the dtb.img for the one matching my device (RG40XX-H V2), then it moves on to the rootfs partition, where it disables the rx35xxh-panel service that's not needed here, it originally replaced the DTB file with the one matching the device because of the LCD panel version, but it won't work here because there's too many devices. It also installs and enables the joystick-leds service, and a "Open terminal here" patch, because it didn't work in the original Handtop project and it was annoying. Then it just unmounts the image, and repacks it as it was (it's disabled by default to make patching quicker, but you can just uncomment the line below 6.*** to enable it and make it easier to send the file somewhere etc).

# 6. About the joystick-leds service :
It's a custom system service made by me to support the RGB LEDs around the joysticks, it runs once when booting and once every waking up from a suspend and sends a command through uart to the MCU controlling the LEDs to set the color. You can change the color in the /home/rg/.config/joystick-leds/settings.conf file, save it and it will update the color with the next service activation (reboot for sure, maybe suspend/sleep if you're lucky idk). 

# 7. Huge thanks to these amazing projects :
ROCKNIX - For making a mainline kernel and u-boot for these devices - 
junsulee119 - For making the whole Debian based OS for RG35XX-H - 
Raspberry Pi Foundation - For making the rpi-imager that can actually flash the f*cked up image file - 
