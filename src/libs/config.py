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
        # Scan for default locations if no path is provided
        # else attempt to load config file directly
        if cfgpath == '':
            self.__scan_default_paths()
        else:
            self.__load_config(cfgpath)

    def __load_config(self, file) -> None:
        # Attempt to blindly load YAML file...
        try:
            with open(file, 'r') as f:
                self.conf = yaml.safe_load(f)
        except Exception:
            print("Cannot read YAML file!")

    def __scan_default_paths(self) -> None:
        # Scan default path for potential config file.
        for file in default_paths:
            if os.path.exists(os.path.expanduser(file)):
                print(f"Config found in {file}. Loading...")
                self.__load_config(file)

                return
                
        print("Cannot locate flow.yaml in default locations!")

    def get_blueprints_location(self) -> str:
        pass
