#!/bin/bash
set -e

# display the hello message
echo "#########################################################################"
echo "WELCOME TO THE HANDTOP PATCHER V1.0!"
echo "#########################################################################"
echo "It will try to patch the handtop image to make it run on other Anbernic's"
echo "Allwinner H700 based handhelds. It may not work properly."
echo "#########################################################################"

echo ""
echo "1. Unpacking the system image:"
xz -d -v *.img.xz

echo ""
echo "2. Mounting the system image:"
sudo losetup -Pf *.img
sudo mount -v /dev/loop0p1 mnt/boot
sudo mount -v /dev/loop0p2 mnt/root

echo ""
echo "3. Patching the boot partition:"
sudo rm -fv mnt/boot/device_trees/*
sudo cp -v dtb/* mnt/boot/device_trees
cd mnt/boot
sudo rm -fv dtb.img dtb-rocknix.img dtb-rev6.img dtb-regular.img panel.txt rg35xxh-input.conf
sudo cp -v device_trees/*40xx-h-v2-panel.dtb dtb.img # i'll implement choosing later
cd ../..

echo ""
echo "4. Patching the rootfs:"
sudo mkdir mnt/root/home/rg/.config/joystick-leds
sudo cp -v service/settings.conf mnt/root/home/rg/.config/joystick-leds
sudo cp -v service/joystick-leds.py mnt/root/usr/local/bin
sudo cp -v service/joystick-leds.service mnt/root/etc/systemd/system
sudo mkdir mnt/root/home/rg/.config/Thunar
sudo cp -v patches/uca.xml mnt/root/home/rg/.config/Thunar
cd mnt/root
sudo ln -sv etc/systemd/system/joystick-leds.service etc/systemd/system/multi-user.target.wants/joystick-leds.service
sudo rm -fv etc/systemd/system/multi-user.target.wants/rg35xxh-panel.service
sudo chmod -v 755 usr/local/bin/joystick-leds.py
sudo chmod -v 666 home/rg/.config/joystick-leds/settings.conf
sudo chmod -v 644 etc/systemd/system/joystick-leds.service
sudo chmod -v 666 home/rg/.config/Thunar/uca.xml
cd ../..

echo ""
echo "5. Unmounting the system image:"
sync
sudo umount -v mnt/*
sudo losetup -d /dev/loop0

echo ""
echo "6. Repacking the system image (disabled, enable for smaller file):"
#xz -T0 -9 -v *.img

echo ""
echo "#########################################################################"
echo "THE PATCHER PATCHED THE PATCHES!"
echo "#########################################################################"
echo "So, here's what to do now:"
echo " 1. flash the image.img.xz to your microSD card."
echo " 2. mount the boot partition from the microSD card. Choose the dtb"
echo "    file for your device (default is rg40xxhv2), rename it to"
echo "    dtb.img and place it in the boot partition's root folder."
echo " 3. Enjoy! And please let me know, if anything is broken."
echo "#########################################################################"
echo "kernel: rocknix, userspace: junsulee119, patcher: us3r_d0e5nt_3x1st"
echo "#########################################################################"
