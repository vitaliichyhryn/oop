import json

from gi.repository import Adw, Gtk, Gio
from .drawing_area import DrawingArea
from .shape_picker import ShapePicker
from .table import Table

@Gtk.Template(resource_path="/com/chyhryn/Lab5/gtk/window.ui")
class Window(Adw.ApplicationWindow):
    __gtype_name__: str = "Window"
    
    overlay: Gtk.Overlay = Gtk.Template.Child()
    table: Table | None = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.drawing_area = DrawingArea()
        self.overlay.set_child(self.drawing_area)
        
        # check if singleton
        print((new_drawing_area := DrawingArea()) is self.drawing_area)

        pick_shape = Gio.PropertyAction(
            name="pick_shape",
            object=self.drawing_area,
            property_name="picked_shape_name",
        )
        self.add_action(pick_shape)
        
        self.create_action("open_file", self.open_file)
        self.create_action("save_file", self.save_file)
        
        self.drawing_area.stroked.connect(self.on_stroked)
    
    def create_action(self, name, callback):
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        
    @Gtk.Template.Callback()
    def show_table(self, button: Gtk.Button) -> None:
        if self.table:
            self.table.present()
            return
        self.table: Table = Table(self.drawing_area.table)
        self.table.entry_removed.connect(self.on_entry_removed)
        self.table.single_selection.connect("selection-changed", self.on_selection_changed)
        self.table.connect("close-request", self.on_table_closed)
        self.table.present()
        
    def on_stroked(self, drawing_area) -> None:
        if self.table is not None:
            self.table.update_table(self.drawing_area.table)
    
    def on_entry_removed(self, table) -> None:
        self.drawing_area.selected_shape = None
        self.drawing_area.table = self.table.table
        
    def on_selection_changed(self, single_selection, *_) -> None:
        pos = single_selection.get_selected()
        self.drawing_area.selected_shape = self.drawing_area.shapes[pos]
        self.drawing_area.queue_draw()
    
    def on_table_closed(self, table) -> None:
        self.table = None
        self.drawing_area.selected_shape = None
        self.drawing_area.queue_draw()
        
    def open_file(self, *_):
        dialog = Gtk.FileDialog()
        dialog.open(self, None, self.on_file_opened)
    
    def on_file_opened(self, file_dialog, result):
        file = file_dialog.open_finish(result)
        contents = file.load_contents()[1].decode('utf-8')
        self.drawing_area.table = json.loads(contents)
    
    def save_file(self, *_):
        dialog = Gtk.FileDialog(initial_name="untitled")
        dialog.save(self, None, self.on_file_saved)
    
    def on_file_saved(self, file_dialog, result):
        file = file_dialog.save_finish(result)
        contents = (
            json.dumps(self.drawing_area.table, ensure_ascii = False)
            .encode("UTF-8")
        )
        file.replace_contents_async(
            contents,
            etag=None,
            make_backup=False,
            flags=Gio.FileCreateFlags.NONE,
            cancellable=None,
            callback=self.on_replace_contents,
        )
    
    def on_replace_contents(self, file, result):
        file.replace_contents_finish(result)
    
