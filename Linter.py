
# Important packages/libraries
import ast
from Checkers_Modules import *

# Sample Cases
from Sample_Cases import LinterCases as LC


class Linter:
    def __init__(self,ast_tree:ast.AST):
        self.ast_tree = ast_tree
        self.main_violations_set = {} #Store violations in a dictionary of each respective checker

        # {<linting_rule_1>: set(),
        # for key_value_pair of this dictionary key = a_linting_checker, value = set_of_all violations from checker

        # }

    

    def run_all_linting_rule_non_threaded(self):
        # Store checkers objs in list for later reference
        checker_objs = []
        
        #CHECKER OBJ STANDARDIZATIONS
        # 1. violations set attribute must be named 'violations'!
        # 2. violations set attribute must be datatype of 'set' and initialized as empty upon init!
        # 3. checker object must have class method of 'run_check'!
            # 'run_check' must accept ast_tree argument as datatype 'ast.AST'
            # 'run_check' must run linting rule on ast_tree and store violations in 'violations'
        # 4. 'run_check' & 'violations' must be accessible under same class

        # Init and Run checkers
        div_checker = Divison_By_Zero_Checker.DivisionByZeroChecker()
        div_checker.run_check(self.ast_tree)
        checker_objs.append(div_checker)
        

        dupe_checker = Duplicate_Item_Checker.DuplicateVarChecker()
        dupe_checker.run_check(self.ast_tree)
        checker_objs.append(dupe_checker)

        # Moving violations to main violations
        checker_obj: object
        
        for checker_obj in checker_objs:
            self.main_violations_set[checker_obj.__class__.__name__] = checker_obj.violations
        pass

    def __str__(self):
        '''
        returns str upon print method being called upon this class object
        '''
        no_violations_response = 'NO VIOLATIONS'
        string = 'All violations:\n'
        for checker in self.main_violations_set:
            string += '\t'+checker + ':' + '\n'
            string += f'\tDetected: {len(self.main_violations_set[checker])} \n'
            if self.main_violations_set[checker]:
                for violation in self.main_violations_set[checker]:
                    string += '\t\t'+violation + '\n'
            else:
                string += f'\t\t{no_violations_response}\n'
                
        return string
        

    

def main():
    
    string = inspect.getsource(LC.divide_by_constant)
    ast_tree = ast.parse(string)
    mylinter = Linter(ast_tree=ast_tree)
    mylinter.run_all_linting_rule_non_threaded()
    print(mylinter)
    pass

if __name__ == '__main__':
    main()