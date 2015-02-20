#!/usr/bin/env python3

"""
An application that cycles through webpages

WebKit-GTK-python code started from http://stackoverflow.com/a/11070455/3242539
"""

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import WebKit
import threading
import time
import sys

# Use threads                                       
GLib.threads_init()

class App(object):
    def __init__(self):
        window = Gtk.Window()
        window.connect("delete-event",self.quit)
        window.connect("key-press-event",self.on_key_press)

        webView = WebKit.WebView()
        window.add(webView)
        window.show_all()

        self.window = window
        self.webView = webView

        self.is_fullscreen = False

    def on_key_press(self,widget,event):
        keyname = Gdk.keyval_name(event.keyval)
        #print("key pressed",keyname)
        if keyname == "q" or keyname == "Escape":
          self.quit()
        if keyname == "f":
          if self.is_fullscreen:
            self.window.unfullscreen()
            self.is_fullscreen = False
          else:
            self.window.fullscreen()
            self.is_fullscreen = True

    def quit(self,*args,**kargs):
        #print("Quiting webslideshow...")
        Gtk.main_quit()
        sys.exit()

    def run(self):
        Gtk.main()

    def show_html(self):
        #print("show html")

        #time.sleep(1)
        #print("after sleep")

        #GLib.idle_add(self.webView.load_uri, "http://www.google.com")
        #GLib.idle_add(self.webView.load_uri, "http://radar.weather.gov/ridge/Conus/RadarImg/southeast.gif")
        GLib.idle_add(self.webView.load_uri, "http://radar.weather.gov/ridge/Conus/southeast_loop.php")

if __name__ == "__main__":
  app = App()
  
  thread = threading.Thread(target=app.show_html)
  thread.start()
  
  app.run()
  Gtk.main()


