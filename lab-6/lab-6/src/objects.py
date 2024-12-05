from gi.repository import Gdk, GLib, Gio

class Object():
    def __init__(
        self,
        name: str,
        object_path: str,
        interface_name: str,
        connection: Gio.DBusConnection,
    ) -> None:
        self.name = name
        self.object_path = object_path
        self.interface_name = interface_name
        self.connection = connection
        
    def call_method(
        self,
        method_name: str,
        parameters: GLib.Variant | None = None,
        interface_name: str | None = None,
    ) -> None:
        if not interface_name:
            interface_name = self.interface_name
        
        proxy = Gio.DBusProxy.new_sync(
            connection=self.connection,
            flags=Gio.DBusProxyFlags.NONE,
            info=None,
            name=self.name,
            object_path=self.object_path,
            interface_name=interface_name,
            cancellable=None
        )
        
        proxy.call_sync(
            method_name=method_name,
            parameters=parameters,
            flags=Gio.DBusCallFlags.NONE,
            timeout_msec=-1,
        )
    
    def activate(self) -> None:
        platform_data = GLib.Variant.new_tuple(
            GLib.Variant(
                "a{sv}",
                {"desktop-startup-id": GLib.Variant("s", self.name)},
            )
        )
    
        self.call_method(
            "Activate",
            platform_data,
            "org.freedesktop.Application",
        )
    
    def ping(self) -> None:
        self.call_method("Ping")
    
    @property
    def is_active(self) -> bool:
        try:
            self.ping()
        except Exception as e:
            print(str(e))
            return False
        return True
    
    def shutdown(self) -> None:
        self.call_method("Shutdown")
