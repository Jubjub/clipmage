import os
import sys
import xchat 
import pycurl
import cStringIO
from PythonMagick import Image

__module_name__ = 'clipmage' 
__module_version__ = '0.2' 
__module_description__ = 'Uploads an image on the clipboard to imgur.com and post the url.' 

def screenshot(word, word_eol, userdata):
    try:
        Image("clipboard:").write("PNG32:clipmage.png")
    except RuntimeError:
        xchat.prnt('no image in the clipboard')
        return xchat.EAT_ALL
    response = cStringIO.StringIO()
    c = pycurl.Curl()
    values = [
              ("key", "37c8847d8ce46eb4bb4175ad4573441b"),
              ("image", (c.FORM_FILE, "clipmage.png"))]
    c.setopt(c.URL, "http://api.imgur.com/2/upload.xml")
    c.setopt(c.HTTPPOST, values)
    c.setopt(c.WRITEFUNCTION, response.write)
    c.perform()
    c.close()
    os.remove('clipmage.png')
    xchat.command('say %s' % response.getvalue().split('<original>')[1].split('</original>')[0])
    return xchat.EAT_ALL



xchat.prnt('plugin "clipmage" loaded')
xchat.hook_command('clipmage', screenshot, userdata=None, priority=xchat.PRI_NORM, help=None)

