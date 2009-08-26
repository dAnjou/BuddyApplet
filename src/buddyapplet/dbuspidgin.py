import dbus

class DbusPidgin:
    def __init__(self):
        pass

    def connect(self):
        try:
            self.bus = dbus.SessionBus()
            self.obj = self.bus.get_object("im.pidgin.purple.PurpleService",
                                 "/im/pidgin/purple/PurpleObject")
            self.purple = dbus.Interface(self.obj, "im.pidgin.purple.PurpleInterface")
            return True
        except:
            print "dbus error - maybe pidgin is not running"
            return False

    def get_status_icon(self, buddy):
        try:
            pres = self.purple.PurpleBuddyGetPresence(buddy)
            status = self.purple.PurplePresenceGetActiveStatus(pres)
            statusname = self.purple.PurpleStatusGetId(status)
            if statusname == "available":
                return "/usr/share/pixmaps/pidgin/status/16/available.png"
            elif statusname == "away" or statusname == "extended_away":
                return "/usr/share/pixmaps/pidgin/status/16/away.png"
            elif statusname == "dnd" or statusname == "occupied":
                return "/usr/share/pixmaps/pidgin/status/16/busy.png"
            elif statusname == "offline":
                return "/usr/share/pixmaps/pidgin/status/16/offline.png"
            else:
                return None
        except:
            return None

    def __is_in_list(self, arg, list):
        for entry in list:
            if entry == arg:
                return True
        return False

    def get_buddies_by_status(self, status=["all"]):
        buddyArray = []
        try:
            for account in self.purple.PurpleAccountsGetAllActive():
                for buddy in self.purple.PurpleFindBuddies(int(account), ""):
                    iconpath = self.get_status_icon(buddy)
                    name = self.purple.PurpleBuddyGetAlias(buddy)
                    pres = self.purple.PurpleBuddyGetPresence(buddy)
                    statusid = self.purple.PurplePresenceGetActiveStatus(pres)
                    statusname = self.purple.PurpleStatusGetId(statusid)
                    if self.__is_in_list(statusname, status):
                        buddyArray.append([buddy, name, iconpath])
            return buddyArray
        except:
            return buddyArray

    def get_buddies_by_account(self, username):
        for account in self.purple.PurpleAccountsGetAllActive():
            if username == PurpleAccountGetUsername(account):
                return self.purple.PurpleFindBuddies(account, "")

    def start_IM(self, buddy):
        try:
            account = self.purple.PurpleBuddyGetAccount(buddy)
            self.purple.PurpleConversationNew(1, account, self.purple.PurpleBuddyGetName(buddy))
            return True
        except:
            return False

if __name__ == "__main__":
    print "\timport me :P";