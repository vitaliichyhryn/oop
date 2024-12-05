from gi.repository import Adw
from gi.repository import Gtk

@Gtk.Template(resource_path='/com/chyhryn/Project/gtk/sign-up-dialog.ui')
class SignUpDialog(Adw.Dialog):
    __gtype_name__ = 'SignUpDialog'
    
    view = Gtk.Template.Child()
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.pages = []
        self.conf = {
            "Contact": ["Email"],
            "Delivery": ["First name", "Last name", "Country", "City"],
            "Payment": ["Card number", "Expiration date", "Security code"],
        }
        for page_title in self.conf:
            page = SignUpPage(
                self,
                page_title,
                self.conf[page_title]
            )
            self.pages.append(page)
            self.view.add(page)
        
        self.view.connect("notify::visible-page", self.on_page_changed)
    
    def on_prev_page(self, *_):
        self.view.pop()
    
    def on_next_page(self, *_):
        page = self.view.get_visible_page()
        index = self.pages.index(page)
        self.view.push(self.pages[index + 1])
    
    def on_submit(self, *_):
        user_data = {}
        for page, page_title in zip(self.pages, self.conf):
            user_data[page_title] = {}
            for field_name in self.conf[page_title]:
                entered_text = page.entry_rows[field_name].get_text()
                user_data[page_title][field_name] = entered_text
                
        print(user_data)
    
    def on_page_changed(self, *_):
        visible_page = self.view.get_visible_page()
        visible_page.prev_button.set_visible(visible_page is not self.pages[0])
        visible_page.next_button.set_visible(visible_page is not self.pages[-1])
        visible_page.submit_button.set_visible(visible_page is self.pages[-1])


@Gtk.Template(resource_path='/com/chyhryn/Project/gtk/sign-up-page.ui')
class SignUpPage(Adw.NavigationPage):
    __gtype_name__ = "SignUpPage"
    
    entry_row_group = Gtk.Template.Child()
    prev_button = Gtk.Template.Child()
    next_button = Gtk.Template.Child()
    submit_button = Gtk.Template.Child()
    
    def __init__(self, dialog, title, entry_fields, **kwargs):
        super().__init__(title=title, **kwargs)
        
        self.dialog = dialog
        
        self.prev_button.connect("clicked", dialog.on_prev_page)
        self.next_button.connect("clicked", dialog.on_next_page)
        self.submit_button.connect("clicked", dialog.on_submit)
        
        self.entry_rows = {}
        for field_name in entry_fields:
            entry_row = Adw.EntryRow(title=field_name)
            self.entry_rows[field_name] = entry_row
            self.entry_row_group.add(entry_row)
        
