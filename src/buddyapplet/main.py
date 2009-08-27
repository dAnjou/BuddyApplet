#!/usr/bin/python

import sys
import gtk
import app
import gnomeapplet


def factory(applet, iid):
    app.Applet(applet, iid)
    return True

for arg in sys.argv:
    if arg == "run-in-window":
        mainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
        mainWindow.set_title("BuddyApplet")
        mainWindow.connect("destroy", gtk.main_quit)
        gapplet = gnomeapplet.Applet()
        factory(gapplet, None)
        gapplet.reparent(mainWindow)
        mainWindow.show_all()
        gtk.main()
        sys.exit()

if __name__ == '__main__':
    gnomeapplet.bonobo_factory("OAFIID:BuddyApplet_Factory", gnomeapplet.Applet.__gtype__, "Applet, that displays a Pidgin buddy list", "0.2", factory)