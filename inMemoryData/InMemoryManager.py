# from flask_restful import Resource
from utils.print_enh import print_begin
import logging
import definitions


class InMemoryManager:

    current_logger = definitions.setup_logger(__name__, level=logging.DEBUG)

    def dataframes_load(self, speech_text: str) -> str:

        logtest = f'dataframes_load method with - :{speech_text}'
        print_begin(f'Enter {logtest}')
        self.current_logger.info(f'Entered {logtest}')

        print_begin(f'Exiting {logtest}')
        return speech_text

    def dataframes_search(self, speech_text: str) -> str:
        print_begin(f'Enter dataframes_search method with - :{speech_text}')


        print_begin(f'Exiting dataframes_search method.')
        return speech_text

    def dataframes_add(self, speech_text: str) -> str:
        print_begin(f'Enter dataframes_add method with - :{speech_text}')


        print_begin(f'Exiting dataframes_add method.')
        return speech_text

