from pathlib import Path
import os

class Util:
    """class Util

    Contains utility functions

    """
    def get_config(self, home='.') -> dict:
        config = {}
        try:
            home = Path(os.path.abspath(home))
            EOF = False
            with open(home / 'instance' / 'config.py', mode='r') as fp:
                while not EOF:
                    line = fp.readline()
                    if len(line) == 0:
                        EOF = True
                        continue
                    key, value = line.split('=',maxsplit=1)
                    config[key] = value.replace('\n','')
            return config
        except FileNotFoundError as fnfe:
            print(f'config file not found')
            return None




