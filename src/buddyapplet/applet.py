import pygtk
pygtk.require('2.0')
import gnomeapplet
import gtk
import dbuspidgin

class Applet(gnomeapplet.Applet):
    def __init__(self):
        gnomeapplet.Applet.__init__(self)

        self.dbus = dbuspidgin.DbusPidgin()
        self.dbus.connect()

        # applet icon (what you will see in the panel)
        eventbox = gtk.EventBox()
        eventbox.connect("button-press-event", self.__on_applet_clicked)
        eventbox.show()
        image = gtk.Image()
        image.set_from_file("/usr/share/pixmaps/buddyapplet-icon.png")
        eventbox.add(image)
        image.show()

        # adding "applet icon" to the applet
        self.add(eventbox)

        self.show_all()

        # adding "About" entry to the right click menu
        propxml = """
                <popup name="button3">
                <menuitem name="Item 3" verb="About" label="_About" pixtype="stock" pixname="gtk-about"/>
                </popup>"""
        verbs = [("About", self.__on_about_clicked)]
        self.setup_menu(propxml, verbs, None)

    def __on_applet_clicked(self, eventbox, event):
        if event.button == 1:
            menu = gtk.Menu()
            offmenu = gtk.Menu()
            offitem = gtk.ImageMenuItem("Offline")
            offitem.set_submenu(offmenu)
            offitem.show()
            self.__fill_list(menu, self.dbus.get_buddies_by_status(["available", "away", "dnd", "extended_away", "occupied"]))
            self.__fill_list(offmenu, self.dbus.get_buddies_by_status(["offline"]))
            menu.append(offitem)
            menu.attach_to_widget(eventbox, None)
            menu.popup(None, None, self.__set_menu_position, event.button, event.time, eventbox)
            return True
        return False

    def __set_menu_position(self, menu, eventbox):
        if menu.get_attach_widget() is None:
            # Prevent null exception in weird cases
            return (0, 0, True)
        x,y = eventbox.window.get_origin()
    #    x += eventbox.allocation.x;
        width,height = menu.size_request()
        screen_h = eventbox.get_screen().get_height()
        if (y + height) >= screen_h:
            y -= height;
        else:
            y += eventbox.allocation.height;
        return (x,y,True)

    def __show_alert(self, msg):
        pass

    def __get_menu_entry(self, buddy, name, iconpath):
        caption = name
        item = gtk.ImageMenuItem(caption)
        img = gtk.Image()
        img.set_from_file(iconpath)
        item.set_image(img)
        item.connect("activate", self.__on_item_clicked, buddy)
        item.show()
        return item

    def __fill_list(self, menu, list):
        for buddy, name, iconpath in list:
            item = self.__get_menu_entry(buddy, name, iconpath)
            item.show()
            menu.append(item)

    def __on_item_clicked(self, item, buddy):
        self.dbus.start_IM(buddy)

    def __on_about_close(self, dialog, response):
        if response == gtk.RESPONSE_CANCEL:
            dialog.hide()

    def __on_about_clicked(self, event, data):
        logo = gtk.Image()
        logo.set_from_file("/usr/share/pixmaps/buddyapplet-logo.png")
        about = gtk.AboutDialog()
        about.set_name("BuddyApplet")
        about.set_version("0.2")
        about.set_comments("GNOME panel applet, that displays a Pidgin buddy list")
        about.set_website("http://maximiert.endoftheinternet.org/dokuwiki/")
        about.set_website_label("Website")
        about.set_logo(logo.get_pixbuf())
        about.set_artists(["Mauricio Duque <http://www.snap2objects.com/2008/11/12/15-free-high-resolution-web-stock-icons/>"])
        license = """
Copyright (c) 2009, Max Ludwig
All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the documentation
      and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
        about.set_license(license)
        about.set_authors(["Max Ludwig <maxe.ludwig@googlemail.com>"])
        about.connect("response", self.__on_about_close)
        about.show()

if __name__ == "__main__":
    print "\timport me :P";