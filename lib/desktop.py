import os, sys, gi, debug
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Gio

def setBackground(desktopEnv,imageFile):
    '''
        Change desktop background image to 'imageFile' in Gnome, Cinnamon, Unity or Mate
    '''

    if desktopEnv in ["gnome", "unity", "cinnamon"]:
        uri = 'file://{}'.format(imageFile)
        SCHEMA = "org.gnome.desktop.background"
        KEY = "picture-uri"
        if desktopEnv == "cinnamon":
            SCHEMA = "org.cinnamon.desktop.background"
        try:
            gsettings = Gio.Settings(schema=SCHEMA)
            gsettings.set_string(KEY, uri)
        except:
            args = ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri]
            subprocess.Popen(args)
    elif desktop_env=="mate":
        try: # MATE >= 1.6
            # info from http://wiki.mate-desktop.org/docs:gsettings
            args = ["gsettings", "set", "org.mate.background", "picture-filename", "'{}'".format(imageFile)]
            subprocess.Popen(args)
        except: # MATE < 1.6
            # From https://bugs.launchpad.net/variety/+bug/1033918
            args = ["mateconftool-2","-t","string","--set","/desktop/mate/background/picture_filename", "'{}'".format(imageFile)]
            subprocess.Popen(args)    
