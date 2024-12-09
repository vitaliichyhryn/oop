import json
from gi.repository import Adw, Gtk, GLib, Gio

@Gtk.Template(resource_path='/com/chyhryn/Project/gtk/sign-up-window.ui')
class SignUpWindow(Adw.Window):
    __gtype_name__ = 'SignUpWindow'
    
    view = Gtk.Template.Child()
    
    def __init__(self, win, **kwargs):
        super().__init__(**kwargs)
        
        self.win = win
        self.conf = self.get_conf()
        self.load_conf(self.conf)
        self.view.connect("notify::visible-page", self.on_page_changed)

    def get_conf(self):
        conf_file = Gio.File.new_build_filenamev(
            [
                GLib.get_user_config_dir(),
                "project_conf.json"
            ]
        )
        contents = conf_file.load_contents()[1].decode("utf-8")
        conf = json.loads(contents)
        return conf

    def load_conf(self, conf):
        self.pages = []
        for page_title in conf:
            page = SignUpPage(
                self,
                page_title,
                conf[page_title]
            )
            self.pages.append(page)
            self.view.add(page)

    def on_prev_page(self, *_):
        self.view.pop()
    
    def on_next_page(self, *_):
        page = self.view.get_visible_page()
        index = self.pages.index(page)
        self.view.push(self.pages[index + 1])
    
    def on_submit(self, *_):
        user_data = self.get_user_data()
        self.save_user_data(user_data)
        self.display_user_data(user_data)
        self.close()

    def on_page_changed(self, *_):
        visible_page = self.view.get_visible_page()
        visible_page.prev_button.set_visible(visible_page is not self.pages[0])
        visible_page.next_button.set_visible(visible_page is not self.pages[-1])
        visible_page.submit_button.set_visible(visible_page is self.pages[-1])

    def get_user_data(self):
        user_data = {}
        for page, page_title in zip(self.pages, self.conf):
            user_data[page_title] = {}
            for field_name in self.conf[page_title]:
                entered_text = page.entry_rows[field_name].get_text()
                user_data[page_title][field_name] = entered_text
        return user_data
    
    def save_user_data(self, user_data):
        user_data = json.dumps(user_data, indent=4)
        home_dir = GLib.get_home_dir()
        file = Gio.File.new_for_path(home_dir + "/user_data.json")
        output_stream = file.replace(
            etag=None,
            make_backup=False,
            flags=Gio.FileCreateFlags.NONE,
            cancellable=None,
        )
        output_stream.write(user_data.encode('utf-8'))
        output_stream.close()

    def display_user_data(self, user_data):
        if self.win.user_data_box:
            self.win.box.remove(self.win.user_data_box)

        box = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL,
            halign=Gtk.Align.CENTER,
            valign=Gtk.Align.CENTER,
            spacing=18,
        )

        for page in user_data:
            preferences_group = Adw.PreferencesGroup(title=page)
            for field in user_data[page]:
                row = Adw.ActionRow(title=user_data[page][field], subtitle=field)
                preferences_group.add(row)
            box.append(preferences_group)

        self.win.user_data_box = box
        self.win.box.prepend(box)

@Gtk.Template(resource_path='/com/chyhryn/Project/gtk/sign-up-page.ui')
class SignUpPage(Adw.NavigationPage):
    __gtype_name__ = "SignUpPage"
    
    entry_row_group = Gtk.Template.Child()
    prev_button = Gtk.Template.Child()
    next_button = Gtk.Template.Child()
    submit_button = Gtk.Template.Child()
    
    def __init__(self, sign_up_win, title, entry_fields, **kwargs):
        super().__init__(title=title, **kwargs)
        
        self.sign_up_win = sign_up_win
        
        self.prev_button.connect("clicked", sign_up_win.on_prev_page)
        self.next_button.connect("clicked", sign_up_win.on_next_page)
        self.submit_button.connect("clicked", sign_up_win.on_submit)
        
        self.entry_rows = {}
        for field_name in entry_fields:
            entry_row = Adw.EntryRow(title=field_name)
            self.entry_rows[field_name] = entry_row
            self.entry_row_group.add(entry_row)
