import sys
import os
import socket
import yaml # type: ignore
import json
import logging
import logging.config
from logging import FileHandler, Handler, StreamHandler, Formatter
from typing import Optional, Dict, Any
from colorama import Fore, Back, Style, init # type: ignore


class ExtConsoleLogger(object):
    def __init__(self, conf: str) -> None:
        super().__init__()        
        if not os.path.exists(conf):
            raise RuntimeError(f'Given configuration file {conf} does not exist.')
        with open(conf) as fd:
            configs = yaml.load(fd, Loader=yaml.SafeLoader)
                        
        if configs is None:
            raise RuntimeError('Empty configuration files.')
        self._conf : Dict[str, Any]
        self._gen_logging_config(configs)

        try:
            logging.config.dictConfig(self._conf)        
        except Exception as err:
            print(f'Loading config for logging failed: {err}')
    
    def get_logger(self, name: str) -> Optional['logging.Logger']:
        if 'loggers' in  self._conf and name in self._conf['loggers']:
            return logging.getLogger(name)        
        return None

    def _gen_logging_config(self, configs: dict) -> None:
        self._conf = {'version': 1}
        formatters = {}
        handlers = {}
        
        if 'settings' not in configs or 'formatters' not in configs:
            raise RuntimeError('Missing settings or formatters.')
        
        for fmt, setting in configs['formatters'].items():
            if 'format' not in setting:
                raise RuntimeError('Missing format in {setting}')
            if setting['format'] not in configs['settings']:
                raise RuntimeError(f"Given formatter {fmt}: {setting['format']} not in formats section")
            formatters.update({fmt: {'format': configs['settings'][setting['format']]['log'], 'datefmt': configs['settings'][setting['format']]['date']}})
            handlers.update({fmt: {'class': setting['class'], 'formatter': fmt, 'settings': configs['settings'][setting['settings']]}})
        
        self._conf['formatters'] = formatters
        self._conf['handlers'] = handlers
        self._conf['loggers'] = configs['loggers']
        self._conf['root'] = configs['root']
    
    def print_logging_config(self) -> None:
        print('config for logging:', '\n', json.dumps(self._conf, indent=4))
        print('yaml:', '\n', yaml.dump(self._conf, Dumper=yaml.SafeDumper))
        
          
class ExtConsoleHandler(Handler):
    '''
    Extending StreamHandler with color schema.
    '''  
    def __init__(self, settings: dict) -> None:
        super().__init__()        
        self.settings = settings
        init()
    
    def emit(self, record: 'logging.LogRecord'):        
        try:            
            msg = self.format(record)            
            color=''
            ln_lower = record.levelname.lower()           
            if ln_lower in self.settings:
                if isinstance(self.settings[ln_lower], dict):
                    color=f"{getattr(Back, self.settings[ln_lower]['bg'].upper())}{getattr(Fore, self.settings[ln_lower]['fore'].upper())}"
                elif isinstance(self.settings[ln_lower], str):          
                    color=f'{getattr(Style, self.settings[ln_lower].upper())}'                
                else:
                    raise RuntimeError('Unexpected format.')
                print(f'{color}{msg}{Style.RESET_ALL}')
            else:
                print(msg)
        except Exception:
            self.handleError(record)