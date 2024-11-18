# Important packages/libraries
import ast
from Checkers_Modules import *
import concurrent.futures

# Sample Cases
from Sample_Cases import LinterCases as LC
from Sample_Cases import ChatGPT_binary_search, Claude_binary_search


class Linter:
    def __init__(self, ast_tree: ast.AST):
        """
        Initialize the Linter class.
        :param ast_tree: The Abstract Syntax Tree of the code to lint.
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

        name_checker = NameConventionChecker.NameConventionChecker()
        checker_objs.append(name_checker)
        name_checker.run_check(self.ast_tree)

        unreachable_checker = UnreachableCodeChecker.UnreachableCodeChecker()
        checker_objs.append(unreachable_checker)
        unreachable_checker.run_check(self.ast_tree)

        unused_var_checker = VariableNameChecker.VariableNameChecker()
        checker_objs.append(unused_var_checker)
        unused_var_checker.run_check(self.ast_tree)

        # Moving violations from checkers to main violations
        checker_obj: object
        for checker_obj in checker_objs:
            self.main_violations_set[checker_obj.__class__.__name__] = checker_obj.violations

    def lint_all_multithreaded(self):
        """
        Run all checkers concurrently on the AST tree and collect violations.
        """
        checker_objs = []

        # Init and Run checkers
        div_checker = Divison_By_Zero_Checker.DivisionByZeroChecker()
        checker_objs.append(div_checker)

        dupe_checker = Duplicate_Item_Checker.DuplicateVarChecker()
        checker_objs.append(dupe_checker)

        name_checker = NameConventionChecker.NameConventionChecker()
        checker_objs.append(name_checker)

        unreachable_checker = UnreachableCodeChecker.UnreachableCodeChecker()
        checker_objs.append(unreachable_checker)

        unused_var_checker = VariableNameChecker.VariableNameChecker()
        checker_objs.append(unused_var_checker)

        with concurrent.futures.ThreadPoolExecutor(len(checker_objs)) as executor:
            futures = []
            for checker in checker_objs:
                try:
                    futures.append(executor.submit(checker.run_check, self.ast_tree))
                except Exception as e:
                    print(f"Error submitting checker {checker.__class__.__name__}: {e}")

        # Moving violations from checkers to main violations
        for checker_obj in checker_objs:
            self.main_violations_set[checker_obj.__class__.__name__] = checker_obj.violations

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
    ast_tree = ast.parse(code)
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
