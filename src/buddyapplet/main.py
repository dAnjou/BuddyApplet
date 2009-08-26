#!/usr/bin/python

import sys
import gtk
import app
import gnomeapplet


def factory(app, iid):
    return True

for arg in sys.argv:
    if arg == "run-in-window":
        mainWindow = gtk.Window(gtk.WINDOW_TOPLEVEL)
        mainWindow.set_title("BuddyApplet")
        mainWindow.connect("destroy", gtk.main_quit)
        applet = app.Applet()
        factory(applet, None)
        applet.reparent(mainWindow)
        mainWindow.show_all()
        gtk.main()
        sys.exit()

if __name__ == '__main__':
    gnomeapplet.bonobo_factory("OAFIID:BuddyApplet_Factory", app.Applet.__gtype__, "Applet, that displays a Pidgin buddy list", "0.2", factory)