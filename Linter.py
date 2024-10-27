import ast
class violation:
    # *An instance of a violation within in a set of a linting checker/rule class
    node: ast.AST 
    string: str
    linting_rule : str
    violation_num : int
    pass

    def __str__(self):
        # string = 
        pass

class Linter:
    def __init__(self):
        self.violations = {} #Store violations in a dictionary of each respective checker

        # {<linting_rule_1>: set(),
        # for key_value_pair of this dictionary key = a_linting_checker, value = set_of_all violations from checker

        # }

    
    def run_all_linting_rule(self):
        pass

    def __str__(self):
        pass

    


    