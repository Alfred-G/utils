# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 12:41:47 2016

@author: Alfred
"""
import os
from ftplib import FTP


class Ftp(FTP):
    """
    1
    """


    def __init__(self, server, oschar):
        super(Ftp, self).__init__()
        #self.server=server
        self.set_debuglevel(2)
        self.connect(server)
        self.oschar = oschar
        self.bufsize = 10240
        
    def download(self, filename):
        """
        1
        """

        file_handler = open(os.path.join(self.oschar, filename), 'wb')
        self.retrbinary('RETR %s' % os.path.basename(filename),
                        file_handler.write, self.bufsize)
        file_handler.close()

    def upload(self, filename):
        """
        1
        """

        file_handler = open(os.path.join(self.oschar, filename), 'rb')
        self.storbinary("STOR %s" % os.path.basename(filename),
                        file_handler, self.bufsize)
        file_handler.close()

    def download_files(self):
        """
        1
        """

        dir_res = []
        self.dir('.', dir_res.append)
        files = [f.split(None, 8)[-1] for f in dir_res if f.startswith('-')]
        dirs = [f.split(None, 8)[-1] for f in dir_res if f.startswith('d')]
        return (files, dirs)

    def walk(self, **kwargs):
        """
        1
        """

        ext = kwargs.get('ext', {})
        for path, dirs, files in os.walk(self.oschar):
            for file_name in files:
                os.remove(os.path.join(path, file_name))
        files, dirs = self.download_files()

        for file_name in files:
            if ext and file_name.split('.')[1] in ext:
                self.download(file_name)
        for dir_name in dirs:
            print('Walking to:', dir_name)
            self.cwd(dir_name)
            self.walk()