from gi.repository import Gtk

def find_icon_path(icon_name):
    if icon_name:
        theme = Gtk.IconTheme.get_default()
        for res in range(0, 512, 2):
            icon = theme.lookup_icon(icon_name, res, 0)
            if icon:
                return icon.get_filename()