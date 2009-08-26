#!/bin/sh

echo "    Copy icon in '/usr/share/pixmaps/'"
cp ./buddyapplet-icon.png /usr/share/pixmaps/
echo "    Copy logo in '/usr/share/pixmaps/'"
cp ./buddyapplet-logo.png /usr/share/pixmaps/
echo "    Copy bonobo activation file in '/usr/lib/bonobo/servers/'"
cp ./buddyapplet.server /usr/lib/bonobo/servers/
echo "    Create directory '/usr/lib/gnome-applets/buddyapplet/'"
mkdir -p /usr/lib/gnome-applets/buddyapplet/
echo "    Copy modules in '/usr/lib/gnome-applets/buddyapplet/'"
cp ./src/buddyapplet/main.py /usr/lib/gnome-applets/buddyapplet/main
cp ./src/buddyapplet/dbuspidgin.py /usr/lib/gnome-applets/buddyapplet/
cp ./src/buddyapplet/app.py /usr/lib/gnome-applets/buddyapplet/
echo "    Set rights for the executable"
chmod +x /usr/lib/gnome-applets/buddyapplet/main
echo "    Ready"

exit 0