import sys
import os
import unittest
import logging

root_path: str = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, root_path)
test_path = os.path.join(root_path, 'tests')
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logging.debug(f'root path: {root_path}')

from logger import ExtConsoleLogger

class ConfigTestCase(unittest.TestCase):
       
    def setUp(self) -> None:
        return super().setUp()
    
    def test_configure(self) -> None:
        try:
            ExtConsoleLogger('file_not_exist.yaml')
            self.assertTrue(False)
        except Exception as err:
            logging.debug(f'got exepected exception: {err}')

        try:
            ExtConsoleLogger('empty.yaml').get_logger()
            self.assertTrue(False)
        except Exception as err:
            logging.debug(f'got exepected exception: {err}')
        try:
            conf_file = os.path.join(root_path, 'basic.yaml')
            logging.debug(f'using default yaml {conf_file}')
            ext_log = ExtConsoleLogger(conf_file)
            self._logger = ext_log.get_logger('not_exist')            
        except Exception as err:
            logging.debug(f'unexpected error: {err}')
            self.assertTrue(False)
    
    def test_blakcwhite(self) -> None:
        try:
            conf_file = os.path.join(root_path, 'basic.yaml')
            logging.debug(f'using default yaml {conf_file}')     
            ext_log = ExtConsoleLogger(conf_file)       
            self._logger = ext_log.get_logger('Example2')
            self.assertIsNotNone(self._logger)
            self._logger.debug('this is a debug message')
            self._logger.info('this is a info message')
            self._logger.warning('this is a warning message')
            self._logger.error('this is a error message')
        except Exception as err:
            logging.debug(f'unexpected error: {err}')
            self.assertTrue(False)

    def test_colorful(self) -> None:
        try:
            conf_file = os.path.join(root_path, 'basic.yaml')
            logging.debug(f'using default yaml {conf_file}')
            ext_log = ExtConsoleLogger(conf_file)            
            self._logger = ext_log.get_logger('Example1')
            self.assertIsNotNone(self._logger)            
            self._logger.debug('this is a debug message')
            self._logger.info('this is a info message')
            self._logger.warning('this is a warning message')
            self._logger.error('this is a error message')
        except Exception as err:
            logging.debug(f'unexpected error: {err}')
            self.assertTrue(False)
        
if __name__ == '__main__':
    unittest.main()
