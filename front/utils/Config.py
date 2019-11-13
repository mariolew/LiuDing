#coding=utf-8

import configparser
import sys
import json
import os

__all__ = ['init_config', 'get_config']

__CR__ = None


class ConfigRead(object):
    def __init__(self, filename):
        if os.path.exists(filename):
            self._is_init = True
        else:
            self._is_init = False
        self._cp = configparser.ConfigParser()
        self._cp.read(filename)
        self._config = {}
        self._generate()

    def _get(self, key, section=None):
        if section == None:
            section = self._section
        if self._cp.has_option(section, key):
            res = self._cp.get(section, key)
            try:
                if res.find('#') < 0:
                    res = res.strip()
                else:
                    symbol_index = res.index('#')
                    if res[symbol_index - 1] == '\\':
                        res = res.replace('\\', '')
                        res = res.strip()
                    else:
                        res = res[:res.index("#")].strip()
                # verify boolean
                bool_res = res.upper()
                if bool_res == "FALSE":
                    return False
                elif bool_res == "TRUE":
                    return True
                try:
                    res = int(res)
                except:
                    try:
                        res = float(res)
                    except:
                        return res
                return res
            except:
                return res
        else:
            return False


    def _generate(self):
        for section in self._cp.sections():
            if section not in self._config:
                self._config[section] = {}
            for key in self._cp.options(section):
                self._config[section][key] = self._get(key, section)

    def get_config(self):
        if self._is_init:
            return self._config
        else:
            return False

    def output_config(self):
        sections = sorted(self._config.keys())
        for section in sections:
            print('[{0}]'.format(section))
            keys = sorted(self._config[section])
            for key in keys:
                print('{0} = {1}'.format(key, self._config[section][key]))


def get_config():
    global __CR__
    return __CR__

def init_config(config_path):
    global __CR__
    reader = ConfigRead(config_path)
    __CR__ = reader.get_config()
    if not __CR__:
        return False
    else:
        return True



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: Config.py conf")
        exit(1)
    conf_file = sys.argv[1]
    CR = ConfigRead(conf_file)
    CR.output_config()
