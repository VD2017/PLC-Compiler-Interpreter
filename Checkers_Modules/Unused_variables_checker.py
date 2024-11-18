import ast

class VariableNameChecker:
    def __init__(self):
        self.violations = set()  # Standardized violations attribute as a set

    def run_check(self, ast_tree: ast.AST):
        """
        Runs the linting rule on the provided AST tree to detect unused variables.
        Populates the 'violations' set with messages about detected issues.
        """
        class VariableVisitor(ast.NodeVisitor):
            def __init__(self):
                self.assigned_vars = set()
                self.used_vars = set()

            def visit_Assign(self, node):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.assigned_vars.add(target.id)
                self.generic_visit(node)

            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Load):
                    self.used_vars.add(node.id)
                self.generic_visit(node)

        # Visit the tree and collect variables
        visitor = VariableVisitor()
        visitor.visit(ast_tree)

        # Find unused variables
        unused_vars = visitor.assigned_vars - visitor.used_vars
        for var in unused_vars:
            self.violations.add(f"Variable '{var}' is assigned but never used.")

    def __str__(self):
        """
        Returns a string representation of the violations for this checker.
        """
        if not self.violations:
            return f"{self.__class__.__name__}: No violations detected."
        return f"{self.__class__.__name__} Violations:\n" + "\n".join(self.violations)


# Example of how this would be used with the main Linter class
if __name__ == "__main__":
    test_code = """
x = 5
y = 10
z = x + y
print(x)
a = 3
b = 5
for i in range(10):
    print(i)
    e = 8

"""

    # Parse the code into an AST
    tree = ast.parse(test_code)

    # Create and run the checker
    checker = VariableNameChecker()
    checker.run_check(tree)

    # Print the violations
    print(checker)
