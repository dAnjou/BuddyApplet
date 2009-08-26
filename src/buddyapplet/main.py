#!/usr/bin/python

import sys
import gtk
import applet

def factory(applet, iid):
    return True

for arg in sys.argv:
    if arg == "run-in-window":
        mainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
        mainWindow.set_title("BuddyApplet")
        mainWindow.connect("destroy", gtk.main_quit)
        applet = applet.Applet()
        factory(applet, None)
        applet.reparent(mainWindow)
        mainWindow.show_all()
        gtk.main()
        sys.exit()

if __name__ == '__main__':
    print "Starting factory"
    gnomeapplet.bonobo_factory("OAFIID:BuddyApplet_Factory", buddyapplet.Applet.__gtype__, "Applet, that displays a Pidgin buddy list", "0.2", factory)