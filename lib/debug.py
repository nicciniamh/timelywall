#
# Handy Debug Logger
# Copyright 2017 Nicole Stevens
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys, os, inspect, gi, datetime
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GObject, Gdk, GdkPixbuf
from cStringIO import StringIO

debugFlag = True
logData = None
debugPos = 0
def setdebug(flag):
    global debugFlag
    if(flag):
        debugFlag = True
    else:
        debugFlag = False
def getdebug():
    return debugFlag
def debug(*args):
    global debugFlag, logData
    if debugFlag:
        caller = inspect.getframeinfo(inspect.stack()[1][0])
        fname = str(caller.filename).replace(os.getcwd()+'/','')
        now = datetime.datetime.now()
        timestr = '{:02}:{:02}:{:02}'.format(now.hour,now.minute,now.second)
        idstr = '{}: {}:{}'.format(timestr, fname, caller.lineno)
        x = ['{} - '.format(idstr)]
        for a in args:
            x.append('{}'.format(a))
        output = ' '.join(x)
        #print output
        if not logData:
            try:
                logData = open('./logfile.txt','a+',0)
            except Exception as e:
                sys.stderr.write('{} - Fatal - logfile could not be opened: {}\n'.format(idstr,e))
                sys.exit(1)
            greeting = '{} Welcome to Timely Wallpaper - Logging to {}\n'.format(timestr,os.path.abspath('./logfile.txt'))
            logData.write(greeting)
            sys.stdout.write(greeting)
            debugPos = logData.tell()
        logData.write('{}\n'.format(output))


class debugWindow:
    def __init__(self,iconFile):
        if not getdebug():
            setdebug(True)
            debug("Started Logging")
        self.debugShown = True
        self.iconFile = iconFile
        self.win = Gtk.Window(title="Log View")
        self.win.connect('delete-event',self.hide)
        self.timeout_source = None
        self.win.set_icon_from_file(self.iconFile)
        self.win.set_size_request(640,480)
        self.box = Gtk.VBox(2)
        self.sw = Gtk.ScrolledWindow()
        self.buf = Gtk.TextBuffer(text='')
        self.txt = Gtk.TextView(buffer=self.buf)
        self.txt.connect('size-allocate',self.scrollToBottom)
        self.txt.set_editable(False)
        self.win.add(self.box)
        self.sw.add(self.txt)
        self.box.add(self.sw)

    def show(self):
        self.debugShown = True
        self.win.show_all()
        self.ticker()

    def ticker(self):
        global debugPos
        if not logData:
            return
        tmpPos = logData.tell()
        logData.seek(debugPos,0)
        text = logData.read()
        logData.seek(tmpPos,0)
        debugPos = tmpPos
        end_iter = self.buf.get_end_iter()
        self.buf.insert(end_iter, text)
        self.timeout_source = GObject.timeout_add(1000,self.ticker)

    def scrollToBottom(self,*args):
        adj = self.sw.get_vadjustment()
        adj.set_value(adj.get_upper() - adj.get_page_size())

    def hide(self,*args):
        self.debugShown = False
        if self.timeout_source:
            try:
                GObject.source_remove(self.timeout_source)
            except:
                pass
        self.timeout_source = None
        self.win.hide()  
        return True

    def toggleVisibility(self,*args):
        if self.debugShown:
            self.hide()
        else:
            self.show()

    def getVisibility(self):
        return self.debugShown

