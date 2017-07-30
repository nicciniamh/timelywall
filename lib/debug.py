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

debugFlag = False
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
