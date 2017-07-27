#
# Handy Dialog Functions
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
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
import os, sys
if float(sys.version[:3]) < 3:
    from builtins import object
    from future import standard_library
    standard_library.install_aliases()

import gi, collections
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

class messageDlg(object):
    def __init__(self, msg, **kwargs):
        self.buttonTypes = { 'OKCANCEL':    Gtk.ButtonsType.OK_CANCEL,
                             'OK':          Gtk.ButtonsType.OK, 
                             'NONE':        Gtk.ButtonsType.NONE,
                             'YESNO':       Gtk.ButtonsType.YES_NO,
                             'CLOSE':       Gtk.ButtonsType.CLOSE,
             }
        self.custom_buttons = None
        mtype='error'
        self.buttons = Gtk.ButtonsType.OK
        self.response_handler = None
        if 'response_handler' in kwargs:
            self.response_handler = kwargs['response_handler']
        if 'mtype' in kwargs:
            mtype = kwargs['mtype']

        if 'parent' in kwargs:
            parent = kwargs['parent']
        else:
            parent = None


        if 'buttons' in kwargs:
          if kwargs['buttons']:
            if kwargs['buttons'] in self.buttonTypes:
                self.buttons = self.buttonTypes[kwargs['buttons']]
            else:
                raise ValueError('Cannot map "{}" to Gtk.ButtonType'.format(kwargs['buttons']))
          else:
            self.buttons = None

        if 'custom_buttons' in kwargs:
          self.custom_buttons = kwargs['custom_buttons']

        estr = ''

        if mtype == 'error':
            mtype=Gtk.MessageType.ERROR
        elif mtype == 'warn':
            mtype=Gtk.MessageType.WARNING
        elif mtype == 'info':
            mtype = Gtk.MessageType.INFO

        if self.buttons:
          self.dlg = Gtk.MessageDialog(parent=parent,
                            flags=Gtk.DialogFlags.MODAL,
                            type=mtype,
                            buttons=self.buttons,
                            message_format=msg)
        else:
          self.dlg = Gtk.MessageDialog(parent=parent,
                            flags=Gtk.DialogFlags.MODAL,
                            type=mtype,
                            message_format=msg)

        if not self.buttons and len(self.custom_buttons):
          for bt,bid in self.custom_buttons:
            self.dlg.add_button(bt,bid)

        if 'title' in kwargs:
          self.dlg.set_secondary_text(kwargs['title'])

        self.dlg.connect("response", self.response_cb)

    def response_cb(self,widget, response):
        if isinstance(self.response_handler, collections.Callable):
            self.response_handler(response)
        widget.destroy()

def error(msg, **kwargs):
    x = messageDlg(msg,**kwargs)
    return x.dlg.run()

def question(msg,responseHandler=None, mtype='warn', buttons='YESNO',**kwargs):
    resp = [None]
    def noResponse(r):
      resp[0] = r
    x = messageDlg(msg,mtype=mtype, buttons=buttons, response_handler=responseHandler or noResponse,**kwargs)
    dlgreturn = x.dlg.run()
    if responseHandler:
      return dlgreturn
    return resp[0]
    
def message(msg,responseHandler=None, mtype='info', buttons='OK',**kwargs):
    x = messageDlg(msg,mtype=mtype, buttons=buttons, response_handler=responseHandler,**kwargs)
    return x.dlg.run()

if __name__ == "__main__":
  def resp(*args):
    print('response',args)

  question("Unsaved changes!", buttons=None, responseHandler=resp,
    custom_buttons = [('Close Without Saving',Gtk.ResponseType.CLOSE),
                      ('Cancel',Gtk.ResponseType.CANCEL),
                      ('Save',42)])
