import ast
import re

class NameConventionChecker:
    def __init__(self):
        self.violations = set()  # Store violations in a set

    def run_check(self, ast_tree: ast.AST):
        """
        Processes the AST tree to check for name convention violations.
        Populates the `violations` set with messages about detected issues.
        """
        class NameConventionVisitor(ast.NodeVisitor):
            def __init__(self):
                self.all_names = set()        # All names (variables, functions, etc.)
                self.snake_case_names = set()
                self.camel_case_names = set()
                self.other_case_names = set()

            def visit_FunctionDef(self, node):
                self.all_names.add(node.name)
                self._check_name_convention(node.name)
                self.generic_visit(node)

            def visit_Name(self, node):
                # Collect all variable names
                self.all_names.add(node.id)
                self._check_name_convention(node.id)
                self.generic_visit(node)

            def _check_name_convention(self, name):
                snake_case_pattern = r'^[a-z]+(_[a-z0-9]+)*$'
                camel_case_pattern = r'^[a-z]+([A-Z][a-z0-9]+)+$'

                if re.match(snake_case_pattern, name):
                    self.snake_case_names.add(name)
                elif re.match(camel_case_pattern, name):
                    self.camel_case_names.add(name)
                else:
                    self.other_case_names.add(name)

        # Visit the AST tree and collect names
        visitor = NameConventionVisitor()
        visitor.visit(ast_tree)

        # Check names in camelCase or other formats that should follow snake_case
        for name in visitor.camel_case_names:
            self.violations.add(f"Violation: '{name}' is in camelCase, expected snake_case.")
        for name in visitor.other_case_names:
            self.violations.add(f"Violation: '{name}' does not follow snake_case or camelCase.")

    def __str__(self):
        """
        Returns a string representation of the violations for this checker.
        """
        if not self.violations:
            return f"{self.__class__.__name__}: No violations detected."
        return f"{self.__class__.__name__} Violations:\n" + "\n".join(self.violations)


# Example of integration with the main Linter class
if __name__ == "__main__":
    code = """
def exampleFunction():
    snake_case_var = 10
    camelCaseVar = 20
    iPhone_ = 12
    AnotherVar = 30
"""

    # Parse the code into an AST
    tree = ast.parse(code)

    # Create and run the checker
    name_checker = NameConventionChecker()
    name_checker.run_check(tree)

    # Print the violations
    print(name_checker)
