#!/usr/bin/env python
# -*- coding: UTF8 -*-
""" A script for working with dotenv files locally. """
import re
import os
import dotenv


def dotenv_to_dict(dotenv_file) -> dict:
  """ Convert dotenv to dict. """
  with open(dotenv_file, 'r') as f:
    content = f.readlines()

  content_list = [x.strip().split('#')[0].split('=', 1) for x in content if '=' in x.split('#')[0]]
  for i, x in enumerate(content_list):
    for index, num in enumerate(x):
      if index % 2 != 0:
        try:
          content_list[i][index] = num.split("'")[1]
        except IndexError:
          content_list[i][index] = num.split('"')[1]

  content_dict = dict(content_list)
  for k, v in content_list:
    for i, x in enumerate(v.split('$')[1:]):
      key = re.findall(r'\w+', x)[0]
      v = v.replace('$' + key, content_dict[key])
    content_dict[k] = v

  return content_dict


def get_dotenv_path():
  """ Load dotenv file. """
  dotenv_file = dotenv.find_dotenv()
  dotenv.load_dotenv(dotenv_file)
  return dotenv_file


def update_dotenv(new_dotenv: dict):
  """ Update dotenv. """
  dotenv_file = get_dotenv_path()

  for key, value in new_dotenv.items():
    os.environ[key] = str(value)
    # Write changes to .env file.
    dotenv.set_key(dotenv_file, key, os.environ[key])


def check_change(new_dotenv: dict) -> bool:
  """ Check if was dotenv updated. """
  dotenv_file = get_dotenv_path()
  current_dotenv = dotenv_to_dict(dotenv_file)
  for key, value in new_dotenv.items():
    if not (key, value) in new_dotenv.items():
      return False
    
  return True