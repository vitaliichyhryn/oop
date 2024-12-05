import numpy, subprocess, json

from matplotlib.backends.backend_gtk4agg import \
    FigureCanvasGTK4Agg as FigureCanvas
from matplotlib.figure import Figure
from gi.repository import Adw, Gtk, Gdk

@Gtk.Template(resource_path='/com/chyhryn/Object3/gtk/window.ui')
class Window(Adw.ApplicationWindow):
    __gtype_name__ = 'Window'
    
    toolbar_view = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    @property
    def points(self):
        process = subprocess.run(["wl-paste"], capture_output=True, text=True)
        clipboard_text = process.stdout
        points = json.loads(clipboard_text)
        return points
        
    def show_plot(self):
        figure = Figure()
        axes = figure.add_subplot()
        xs = [point[0] for point in self.points]
        ys = [point[1] for point in self.points]
        
        axes.spines[["left", "bottom"]].set_position('zero')
        axes.spines[["top", "right"]].set_visible(False)
        
        axes.set(aspect="equal")
        
        axes.set_xlabel('x', size=14, labelpad=-24, x=1.03)
        axes.set_ylabel('y', size=14, labelpad=-28, rotation=0, y=1.02)
        
        axes.plot(1, 0, ">k", transform=axes.get_yaxis_transform(), clip_on=False)
        axes.plot(0, 1, "^k", transform=axes.get_xaxis_transform(), clip_on=False)
        
        axes.plot(xs, ys, marker='o', linestyle='-')

        canvas = FigureCanvas(figure)
        canvas.set_size_request(1200, 1200)
        self.toolbar_view.set_content(canvas)
        
