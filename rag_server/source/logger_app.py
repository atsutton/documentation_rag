from logger_debug import logger
from logger_rag import RagLogger

class AppLogger():

    def __init__(self):
        self._debugger = logger
        self._raglog = RagLogger()

    def user_input(self, val):
        self._raglog.record.UserInput = val
        self._debugger.debug('USER INPUT: ' + val)

    def subqueries_response(self, val):
        self._raglog.record.SubqueriesResponse = val
        self._debugger.debug(f'Subqueries Text: {val}')

    def embeddings_scored(self, val):
        self._raglog.record.EmbeddingsScored = str(val)
        self._debugger.debug(f'Embeddings Scored: {val}')

    def embeddings_top(self, val):
        self._raglog.record.EmbeddingsTop = str(val)
        self._debugger.debug(f'Embeddings Top: {val}')
    
    def main_response(self, val):
        self._raglog.record.MainResponse = val
        self._debugger.debug(f'RES MAIN TEXT: {val}')

    def success(self):
        self._raglog.record.IsSuccess = True
        self._debugger.debug('SUCCESS')

    def error(self, ex):
        self._raglog.record.IsSuccess = False
        self._raglog.record.ErrorMessage = ex
        self._debugger.debug(f'ERROR: {ex}')

    def commit(self):
        self._raglog.commit()
