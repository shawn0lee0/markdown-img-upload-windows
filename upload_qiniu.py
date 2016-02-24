# -*- coding: utf-8 -*-

import os
import sys

from qiniu import Auth, put_file
import qiniu.config

from ctypes import *
import time

import ConfigParser


cf = ConfigParser.ConfigParser()
cf.read('config.ini')
access_key = cf.get('qiniu', 'ak') # AK
secret_key = cf.get('qiniu', 'sk') # SK
bucket_name = cf.get('qiniu', 'bucket') # 七牛空间名
url = cf.get('qiniu', 'url') # url

q = Auth(access_key, secret_key)

mime_type = "image/jpeg"
params = {'x:a': 'a'}

def upload_qiniu(path):
    ''' upload file to qiniu '''
    dirname, filename = os.path.split(path)
    key = '%s' % filename # upload to qiniu's dir

    token = q.upload_token(bucket_name, key)
    progress_handler = lambda progress, total: progress
    ret, info = put_file(token, key, path, params, mime_type, progress_handler=progress_handler)
    return ret != None and ret['key'] == key

if __name__ == '__main__':
    path = sys.argv[1]
    ret = upload_qiniu(path)
    if ret:
        # upload success
        name = os.path.split(path)[1]
        markdown_url = "![](%s/%s)" % (url, name)
        # make it to clipboard
        ahk = cdll.AutoHotkey #load AutoHotkey
        ahk.ahktextdll("") #start script in persistent mode (wait for action)
        while not ahk.ahkReady(): #Wait for AutoHotkey.dll to start
            time.sleep(0.01)
        ahk.ahkExec(u"clipboard = %s" % markdown_url)
    else: print "upload_failed"