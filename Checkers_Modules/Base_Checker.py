from threading import Event
import ast
import queue

class checker_base:
    '''
    This class will used to extend to our respective checker classes
    
    '''
    def __init__(self):
        self.violations = set()
        # self.sync_write_event = Event()

    def run_check(self, ast_tree: ast.AST):
        pass

    def run_check_threaded(self, ast_tree:ast.AST, sync_write_event: Event = None, finished_queue: queue.Queue = None):
        '''
        Runs thread safe version of checker; producer like 
        Params:
        ast_tree: Input AST_tree
        sync_write_event: To synchronize d
        '''

        # Run linting rule
        self.run_check(ast_tree=ast_tree)
        # print(sync_write_event.is_set())

        # Once Done linting, set the event to show that a linting rule is done and put to finished queue
        # print("Finished linting putting",type(self), "Into queue!")
        finished_queue.put(self)
        # print(len(finished_queue))

        while not sync_write_event.is_set():
            sync_write_event.set()
