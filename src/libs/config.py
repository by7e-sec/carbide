import os
import yaml

default_paths = [
    '/etc/distflow/flow.yaml',
    '~/.local/distflow/flow.yaml',
    '../cfg/flow.yaml',
    './cfg/flow.yaml',
    './flow.yaml',
]

class Config:
    conf = {}
    def __init__(self, cfgpath='') -> None:
        if cfgpath == '':
            self.__scan_default_paths()
        else:
            self.__load_config(cfgpath)

    def __load_config(self, file):
        try:
            with open(file, 'r') as f:
                self.conf = yaml.safe_load(f)
                print(self.conf)
        except Exception:
            print("Cannot read YAML file!")

    def __scan_default_paths(self):
        for file in default_paths:
            if os.path.exists(file):
                print(f"Config found in {file}. Loading...")
                self.__load_config(file)

                return
                
        print("Cannot locate flow.yaml in default locations!")
