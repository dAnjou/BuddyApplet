#!/bin/sh

echo "    Copy icon in '/usr/share/pixmaps/'"
cp ./buddyapplet-icon.png /usr/share/pixmaps/
echo "    Copy logo in '/usr/share/pixmaps/'"
cp ./buddyapplet-logo.png /usr/share/pixmaps/
echo "    Copy bonobo activation file in '/usr/lib/bonobo/servers/'"
cp ./buddyapplet.server /usr/lib/bonobo/servers/
echo "    Copy executable in '/usr/lib/gnome-applets/'"
cp ./src/buddyapplet.py /usr/lib/gnome-applets/buddyapplet
echo "    Set rights for the executable"
chmod +x /usr/lib/gnome-applets/buddyapplet
echo "    Ready"

exit 0