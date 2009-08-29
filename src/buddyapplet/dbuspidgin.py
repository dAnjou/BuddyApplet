import dbus

class DbusPidgin:
    def __init__(self):
        self.icondict = {"available"     : "/usr/share/pixmaps/pidgin/status/16/available.png",
                         "away"          : "/usr/share/pixmaps/pidgin/status/16/away.png",
                         "extended_away" : "/usr/share/pixmaps/pidgin/status/16/away.png",
                         "dnd"           : "/usr/share/pixmaps/pidgin/status/16/busy.png",
                         "occupied"      : "/usr/share/pixmaps/pidgin/status/16/busy.png",
                         "offline"       : "/usr/share/pixmaps/pidgin/status/16/offline.png"}

    def connect(self):
        try:
            self.bus = dbus.SessionBus()
            self.obj = self.bus.get_object("im.pidgin.purple.PurpleService",
                                 "/im/pidgin/purple/PurpleObject")
            self.purple = dbus.Interface(self.obj, "im.pidgin.purple.PurpleInterface")
            return True
        except:
            return False

    def get_status_icon(self, buddy):
        try:
            pres = self.purple.PurpleBuddyGetPresence(buddy)
            status = self.purple.PurplePresenceGetActiveStatus(pres)
            statusname = self.purple.PurpleStatusGetId(status)
            iconpath = self.icondict[statusname]
            return iconpath
        except:
            return None

    def get_buddies_by_status(self, statusliste=["all"]):
        buddyArray = []
        try:
            for account in self.purple.PurpleAccountsGetAllActive():
                for buddy in self.purple.PurpleFindBuddies(int(account), ""):
                    iconpath = self.get_status_icon(buddy)
                    name = self.purple.PurpleBuddyGetAlias(buddy)
                    pres = self.purple.PurpleBuddyGetPresence(buddy)
                    statusid = self.purple.PurplePresenceGetActiveStatus(pres)
                    status = self.purple.PurpleStatusGetId(statusid)
                    if status in statusliste:
                        buddyArray.append([buddy, name, iconpath])
            return buddyArray
        except:
            return buddyArray

    def get_buddies_by_account(self, username):
        buddyArray = []
        try:
            for account in self.purple.PurpleAccountsGetAllActive():
                if username == self.purple.PurpleAccountGetUsername(account):
                    for buddy in self.purple.PurpleFindBuddies(account, ""):
                        iconpath = self.get_status_icon(buddy)
                        name = self.purple.PurpleBuddyGetAlias(buddy)
                        buddyArray.append([buddy, name, iconpath])
            return buddyArray
        except:
            return buddyArray

    def get_buddy_details(self, buddy):
        try:
            address = self.purple.PurpleBuddyGetName(buddy)
            account = self.purple.PurpleBuddyGetAccount(buddy)
            accountname = self.purple.PurpleAccountGetUsername(account)
            protocol = self.purple.PurpleAccountGetProtocolName(account)
            if not self.purple.PurpleBuddyGetIcon(buddy) == 0:
                icon = self.purple.PurpleBuddyGetIcon(buddy)
                iconpath = self.purple.PurpleBuddyIconGetFullPath(icon)
            else:
                iconpath = None
            pres = self.purple.PurpleBuddyGetPresence(buddy)
            statusid = self.purple.PurplePresenceGetActiveStatus(pres)
            message = self.purple.PurpleStatusGetAttrString(statusid, "message")
            return (address, accountname, protocol, message, iconpath)
        except:
            return ("", "", "", "", None)

    def start_IM(self, buddy):
        try:
            account = self.purple.PurpleBuddyGetAccount(buddy)
            self.purple.PurpleConversationNew(1, account, self.purple.PurpleBuddyGetName(buddy))
            return True
        except:
            return False

if __name__ == "__main__":
    print "\timport me :P";