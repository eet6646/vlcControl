import requests
import json
import glob
import os
import time
import sys

import logging
logging.basicConfig(filename='vlcControl.log',level=logging.DEBUG,format='%(asctime)s [%(levelname)s]: %(message)s')
logging.getLogger("requests").setLevel(logging.WARNING)

VLC_WEB_PASS = '' # add pass here

class VLCControl():
    def __init__(self, webServ, musicDir, musicFormat):
        self.webServ = webServ
        self.musicDir = musicDir
        self.musicFormat = musicFormat

        self.session = requests.Session()
        self.session.auth = ('', VLC_WEB_PASS)

    def delCurPlaying(self):
        self.getStatus()
        song = self.curStatus['filename']
        artist = self.curStatus['artist']
        search = os.path.join(self.musicDir, self.musicFormat.format(a=artist,st=song))
        foundFile = glob.glob(search)[0]
        logging.info('[Delete] '+foundFile)
        self.nextSong()
        time.sleep(1)
        os.remove(foundFile)

    def getStatus(self):
        r = self.session.get(self.webServ+'/requests/status.json', verify=False)
        data = json.loads(r.text)
        self.curStatus = data['information']['category']['meta']

    def nextSong(self):
        self.session.get(self.webServ+'/requests/status.xml?command=pl_next')


if __name__ == '__main__':
    c_vlc = VLCControl('http://localhost:8080', 'A:\\Music', '{a} - {st}.???') # a=artist, st=song title

    if sys.argv[1] == 'delcur':
        c_vlc.delCurPlaying()