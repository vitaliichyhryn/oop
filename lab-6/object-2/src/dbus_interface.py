import re, random, subprocess, json

from gi.repository import Gio, GLib, Gtk, Gdk

class DBusInterface(Gio.DBusInterfaceSkeleton):
    """
    <node name="/com/chyhryn/Object2">
        <interface name="com.chyhryn.Object2Interface">
            <method name="Initialize">
                <arg name="point_num" type="i" direction="in"/>
                <arg name="x_low" type="i" direction="in"/>
                <arg name="x_up" type="i" direction="in"/>
                <arg name="y_low" type="i" direction="in"/>
                <arg name="y_up" type="i" direction="in"/>
            </method>
            <method name="Ping">
            </method>
            <method name="Shutdown">
            </method>
        </interface>
    </node>
    """
    
    def __init__(self, application):
        self.app = application
        self.win = self.app.get_active_window()
    
        connection = Gio.bus_get_sync(Gio.BusType.SESSION)
        node_info = Gio.DBusNodeInfo.new_for_xml(self.__doc__)
        
        for interface in node_info.interfaces:
            connection.register_object(
                object_path="/com/chyhryn/Object2",
                interface_info=interface,
                method_call_closure=self.on_method_call,
                get_property_closure=None,
                set_property_closure=None,
            )
        
    def on_method_call(
        self,
        connection: Gio.DBusConnection,
        sender: str,
        object_path: str,
        interface_name: str,
        method_name: str,
        parameters: GLib.Variant,
        invocation: Gio.DBusMethodInvocation,
    ) -> None:
        args = list(parameters.unpack())
        method_snake_name = DBusInterface.camelcase_to_snake_case(method_name)
        try:
            result = getattr(self, method_snake_name)(*args)
        except ValueError as e:
            invocation.return_dbus_error(interface_name, str(e))
        invocation.return_value(None)
        
    @staticmethod
    def camelcase_to_snake_case(name: str) -> str:
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
        
    def initialize(self, point_num, x_low, x_up, y_low, y_up):
        points = [(random.randint(x_low, x_up), random.randint(y_low, y_up)) for _ in range(point_num)]
        points.sort(key=lambda point: point[0])
        self.win.show_points(points)
        process = subprocess.run(["wl-copy"], input=json.dumps(points).encode("utf-8"))
            
    def ping(self):
        return
    
    def shutdown(self):
        self.app.quit()
