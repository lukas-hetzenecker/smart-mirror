import dbus

class GeocluePositionProvider(object):
    pass

    def __init__ (self, filename):
        self.interfaces = "org.freedesktop.Geoclue.Position"

    def get_proxy(self):
        self.bus = dbus.SessionBus()
        return self.bus.get_object("org.freedesktop.Geoclue.Providers.Static", "/org/freedesktop/Geoclue/Providers/Static")
