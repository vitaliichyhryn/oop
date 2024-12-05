import gi
import json

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

from gi.repository import Adw, GObject, Gtk, Gio

@Gtk.Template(resource_path="/com/chyhryn/Object2/gtk/table.ui")
class Table(Gtk.ScrolledWindow):
    __gtype_name__: str = "Table"
    
    column_view: Gtk.ColumnView = Gtk.Template.Child()

    def __init__(self, table: list[dict[str, str]], **kwargs):
        super().__init__(**kwargs)
        
        self.table = table
        
        self.keys: list[str] = list(table[0].keys())
        
        list_store = Gio.ListStore(item_type=Entry)
        if self.table[1:]:
            for entry in self.table[1:]:
                list_store.append(
                    Entry(
                        keys=self.keys,
                        values=list(entry.values())
                    )
                )
        
        for key in self.keys:
            column = Gtk.ColumnViewColumn(
                title=key,
                factory=Gtk.SignalListItemFactory()
            )
            column.get_factory().connect("setup", self.on_factory_setup)
            column.get_factory().connect("bind", self.on_factory_bind, key)
            self.column_view.append_column(column)
        
        self.single_selection = Gtk.SingleSelection(
            autoselect=False,
            model=list_store,
        )
        self.column_view.set_model(model=self.single_selection)
            
    def on_factory_setup(self, factory, list_item):
        label = Gtk.Label()
        label.set_margin_top(8)
        label.set_margin_start(8)
        label.set_margin_end(8)
        label.set_margin_bottom(8)
        list_item.set_child(label)
    
    def on_factory_bind(self, factory, list_item, key):
        label = list_item.get_child()
        entry = list_item.get_item()
        label.set_label(str(getattr(entry, key)))
    
    
class Entry(GObject.Object):
    def __init__(self, keys: list[str], values: list[str]):
        super().__init__()
        
        for key, value in zip(keys, values):
            setattr(self, key, value)
