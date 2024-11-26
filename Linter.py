# AST functionality
import ast
from Checkers_Modules import *

# Miscellanous 
import sys

# Multiprocessing
import concurrent.futures
from threading import Event
import queue

# Sample Cases
from Sample_Cases import LinterCases as LC
# from Sample_Cases import Claude_Pig_Dice_Game, ChatGPT_Pig_Dice_Game


class Linter:
    def __init__(self, ast_tree: ast.AST):
        """
        Initialize the Linter class.
        param ast_tree: The Abstract Syntax Tree of the code to lint.
        """
        self.ast_tree = ast_tree
        self.main_violations_set = {}  # Store violations in a dictionary of each respective checker

        # {<linting_rule_1>: set(),
        # for key_value_pair of this dictionary key = a_linting_checker, value = set_of_all violations from checker
        # }

    

    def lint_all_non_threaded(self):
        """
        Run all checkers sequentially on the AST tree and collect violations.
        """
        # Store checker objects in a list for later reference
        checker_objs = []

        # CHECKER OBJECT STANDARDIZATIONS
        # 1. violations set attribute must be named 'violations'!
        # 2. violations set attribute must be datatype of 'set' and initialized as empty upon init!
        # 3. checker object must have class method of 'run_check'!
        #    'run_check' must accept ast_tree argument as datatype 'ast.AST'
        #    'run_check' must run linting rule on ast_tree and store violations in 'violations'
        # 4. 'run_check' & 'violations' must be accessible under the same class

        # Init and Run checkers
        div_checker = Divison_By_Zero_Checker.DivisionByZeroChecker()
        checker_objs.append(div_checker)
        div_checker.run_check(self.ast_tree)

        dupe_checker = Duplicate_Item_Checker.DuplicateVarChecker()
        checker_objs.append(dupe_checker)
        dupe_checker.run_check(self.ast_tree)

        name_checker = NameConventionChecker()
        checker_objs.append(name_checker)
        name_checker.run_check(self.ast_tree)

        unreachable_checker = UnreachableCodeChecker()
        checker_objs.append(unreachable_checker)
        unreachable_checker.run_check(self.ast_tree)

        unused_var_checker = VariableNameChecker()
        checker_objs.append(unused_var_checker)
        unused_var_checker.run_check(self.ast_tree)

        # Moving violations from checkers to main violations
        checker_obj: checker_base
        for checker_obj in checker_objs:
            self.main_violations_set[checker_obj.__class__.__name__] = checker_obj.violations

    def main_set_violations_writer(self, finished_checkers: queue.Queue, if_linting_rule_done: Event, total_checkers: int):
        '''
        For making writing to self.main_violations_set concurrent and thread safe

        Params:
        finished_checkers: a queue where finished checker objs are stored
        if_linting_rule_done: event is there is atleast one linting rule done
        total_checkers: for safety; ensures that all checkers have finished

        '''

        checker_obj: checker_base
        current_num_checkers = 0 

        # Run thread until queue is empty and all checkers have completed
        while (not finished_checkers.empty()) and current_num_checkers < total_checkers:
            
            # Run 
            while if_linting_rule_done.is_set():
                # Get the checker_obj from the finished queue
                checker_obj = finished_checkers.get()
                # print(type(checker_obj))
                self.main_violations_set[checker_obj.__class__.__name__] = checker_obj.violations
                current_num_checkers += 1
                # print(self.main_violations_set)
                # If the queue is empty, clear the event
                # print("Is the queue empty? ",finished_checkers.empty())
                # print("Have all checkers ran?", current_num_checkers)

                if (not finished_checkers) or (current_num_checkers == total_checkers):
                    if_linting_rule_done.clear()
            # print(current_num_checkers)


        
        return True
        
        

    def lint_all_multithreaded(self):
        """
        Run all checkers concurrently on the AST tree and collect violations on separate threads
        """
        checker_objs = []

        # Init and Run checkers
        div_checker = DivisionByZeroChecker()
        checker_objs.append(div_checker)

        dupe_checker = DuplicateVarChecker()
        checker_objs.append(dupe_checker)

        name_checker = NameConventionChecker()
        checker_objs.append(name_checker)

        unreachable_checker = UnreachableCodeChecker()
        checker_objs.append(unreachable_checker)

        unused_var_checker = VariableNameChecker()
        checker_objs.append(unused_var_checker)
        
        # Queue for finished 
        total_checkers = len(checker_objs)
        finished_checkers = queue.Queue(maxsize=total_checkers)
        sync_write_event = Event()

        checker: checker_base
        # Run checkers into Thread pool
        with concurrent.futures.ThreadPoolExecutor(total_checkers) as executor:
            checker_obj_futures: list[concurrent.futures._base.Future]
            checker_obj_futures = []
            try:
                for checker in checker_objs:
                    '''
                    Required args for checker
                    
                    ast_tree:ast.AST 
                    sync_write_event: Event = None
                    finished_queue: queue.Queue = None
                    '''
                    
                    checker_obj_futures.append(executor.submit(checker.run_check_threaded, self.ast_tree, sync_write_event, finished_checkers))
            except Exception as e:
                print(f"Error submitting checker {checker.__class__.__name__}: {e}")
            # Run writer thread to store violations
            executor.submit(self.main_set_violations_writer,finished_checkers, sync_write_event, total_checkers)
        # print([concurrent.futures.wait(checker_obj_futures, return_when='FIRST_COMPLETED')])

        # Moving violations from checkers to main violations
        # while not concurrent.futures.wait(fs=futures):
        #     pass
        # for checker_obj in checker_objs:
        #     self.main_violations_set[checker_obj.__class__.__name__] = checker_obj.violations

    def __str__(self):
        """
        Returns str upon print method being called upon this class object.
        """
        no_violations_response = 'NO VIOLATIONS'
        string = 'All violations:\n'
        for checker in self.main_violations_set:
            string += f'\t{checker}:\n'
            string += f'\tDetected: {len(self.main_violations_set[checker])}\n'
            if self.main_violations_set[checker]:
                for violation in self.main_violations_set[checker]:
                    string += f'\t\t{violation}\n'
            else:
                string += f'\t\t{no_violations_response}\n'
        return string


def main():
    """
    Main function to demonstrate the functionality of the Linter class.
    """
    code = """
def exampleFunction():
    x = 5
    if x > 10:
        return x
        print("Unreachable")  # Unreachable code
    camelCaseVar = 20  # Not snake_case
    y = 10  # Unused variable
"""
    print("Linting", sys.argv[1])
    
    python_module = open(sys.argv[1]).read()

    # ast_tree = ast.parse(inspect.getsource(LC))
    ast_tree = ast.parse(python_module)

    mylinter = Linter(ast_tree=ast_tree)

    # Test both linting modes
    print("Running Non-Threaded Linter:")
    mylinter.lint_all_non_threaded()
    print(mylinter)

    print("\nRunning Multi-Threaded Linter:")
    mylinter.lint_all_multithreaded()
    print(mylinter)


if __name__ == "__main__":
    main()
