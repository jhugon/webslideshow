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
import yaml
import threading
import time
import sys
import argparse

# Use threads                                       
GLib.threads_init()

class App(object):
    def __init__(self,argv):
        self.timeout_index = None
        self.parse_args(argv)
        self.parse_config()
        window = Gtk.Window()
        window.connect("delete-event",self.quit)
        window.connect("key-press-event",self.on_key_press)

        webView = WebKit.WebView()
        window.add(webView)
        window.show_all()

        self.window = window
        self.webView = webView

        if self.is_fullscreen:
            self.window.fullscreen()

    def parse_args(self,argv):
        parser = argparse.ArgumentParser(description="Cycles through webpages.")
        parser.add_argument('config_file', 
                           help='Configuration file path')
        parser.add_argument('--fullscreen','-f', action='store_true',
                           default=False,
                           help='Start in fullscreen mode')
        args = parser.parse_args()
    
        self.is_fullscreen = args.fullscreen
        self.config_filename = args.config_file

    def parse_config(self):
        with open(self.config_filename) as config_file:
          config = yaml.load(config_file)
          #print(config)
          try:
            self.default_page_time = float(config['default_page_time'])
          except TypeError:
            raise Exception("In configuration, default_page_time '{0}' can not be cast to float".format(config['default_page_time']))
          self.profiles = config['profiles']
          self.set_profile_name(config['default_profile'])
          self.next_page_index = 0

    def set_profile_name(self,name):
        if not 'page_list' in self.profiles[name]:
            raise Exception("Profile: '{0}' does not have a 'page_list'".format(name))
        if type(self.profiles[name]['page_list']) != list:
            raise Exception("Profile: '{0}' page_list is not type list".format(name))
        if len(self.profiles[name]['page_list']) == 0:
            raise Exception("Profile: '{0}' page_list is empty".format(name))
        self.profile_name = name
        wait_time = self.default_page_time
        try:
            wait_time = float(self.profiles[name]['page_time'])
        except KeyError:
            pass
        except TypeError:
            raise Exception("In configuration, page_time '{0}' for profile '{1}' can not be cast to float".format(self.profiles[name]['page_time']))
        if self.timeout_index != None:
          Gobject.source_remove(self.timeout_index)
        self.timeout_index = GObject.timeout_add(wait_time*1000,self.on_timeout)

    def get_page(self):
        name = self.profile_name
        page = self.profiles[name]['page_list'][self.next_page_index]

        self.next_page_index += 1
        if self.next_page_index >= len(self.profiles[name]['page_list']):
            self.next_page_index = 0

        return page

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
        self.show_html()
        Gtk.main()

    def on_timeout(self,*args):
        self.show_html()
        return True

    def show_html(self):
        print("starting show html")
        print("  iURL: ",self.next_page_index)
        url = self.get_page()
        print("  URL:       ",url)
        GLib.idle_add(self.webView.load_uri, url)
        

if __name__ == "__main__":
  app = App(sys.argv)
  
  app.run()
  Gtk.main()


