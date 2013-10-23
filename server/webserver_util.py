# System
from time import gmtime, strftime
import calendar, datetime
import cgi
import json
import time
import os
import re
_supported_file_type = {
  'css': 'text/css',
  'gif': 'image/gif',
  'html': 'text/html',
  'ico': 'image/vnd.microsoft.icon',
  'jpg': 'image/jpg',
  'js': 'application/javascript',
  'png': 'image/png',
  'woff': 'application/x-font-woff',
  'ttf': 'application/octet-stream',
  'svg': 'image/svg+xml',
  'ogg': 'audio/ogg',
}

_text_cache = {}

def read_text(path, text_cache = None) :
  key = '_%s_%s' % (path , str(os.path.getmtime(path)))
  if key in _text_cache:
    return _text_cache[key]

  try :
    f = open(path)
    content = f.read()
    f.close()
    _text_cache[key] = content
    return content
  except Exception as e :
    error('Unable to read file', path)
    raise e


def get_request_file_type(path):
  idx = path.find('?')
  if idx > -1:
    path = path[0:idx]
  idx = path.rfind('.')
  if idx > -1:
    path = path[idx + 1:]
  if path in _supported_file_type:
    return path
  else:
    return None

def handle_get(path, query_params):
  content = ''
  file_type = get_request_file_type(path)
  mime = 'text/plain'
  if file_type:
    mime = _supported_file_type.get(file_type)
  else:
    mine = 'text/plain'
  
  if mime and os.path.isfile('.' + path):
    content = read_text('.' + path)
  else:
    content = '"%s" not found' % path
    mime = 'text/plain'
  
  return {
    'mime': mime,
    'content': content
  }
