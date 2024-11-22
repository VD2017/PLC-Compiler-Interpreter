import ast

class UnreachableCodeChecker:
    def __init__(self):
        # Initializes a set to store violations of unreachable code
        self.violations = set()

    def run_check(self, ast_tree: ast.AST):
        # Define a nested visitor class to traverse the AST
        class UnreachableCodeVisitor(ast.NodeVisitor):
            def __init__(self):
                # List to store unreachable code nodes
                self.unreachable_nodes = []
                # Stack to keep track of the current function or scope
                self.scope_stack = []
                # Boolean flag to track whether code is reachable
                self.reachable = True

            def record_unreachable(self, node):
                # Record unreachable nodes, ensuring the node has a line number
                if hasattr(node, 'lineno') and self.scope_stack:
                    self.unreachable_nodes.append((self.scope_stack[-1], node.lineno))

            def process_body(self, body):
                # Processes a list of statements and checks their reachability
                for stmt in body:
                    if not self.reachable:
                        # Record unreachable statements
                        self.record_unreachable(stmt)
                    else:
                        # Visit the statement if reachable
                        self.visit(stmt)
            
            
            def visit_FunctionDef(self, node):
                # Handle function definitions by updating the scope stack
                self.scope_stack.append(node.name)
                self.reachable = True  # Reset reachability for the function body
                self.process_body(node.body[:-1])
                self.generic_visit(node.body[-1])
                self.scope_stack.pop()

            def visit_Return(self, node):
                # Visiting a return statement makes subsequent code unreachable
                self.generic_visit(node)
                self.reachable = False

            def visit_Break(self, node):
                # Visiting a break statement makes subsequent code unreachable in the loop
                self.generic_visit(node)
                self.reachable = False

            def visit_Continue(self, node):
                # Visiting a continue statement makes subsequent code unreachable in the loop
                self.generic_visit(node)
                self.reachable = False

            def visit_If(self, node):
                # Handles if-else blocks and tracks reachability of both branches
                self.visit(node.test)
                current_reachable = self.reachable

                # Process the 'if' body
                self.reachable = current_reachable
                self.process_body(node.body)
                if_reachable = self.reachable

                # Process the 'else' body
                self.reachable = current_reachable
                self.process_body(node.orelse)
                else_reachable = self.reachable

                # After the if-else block, reachable if either branch is reachable
                self.reachable = if_reachable or else_reachable

            def visit_For(self, node):
                # Handles for loops, checking the body and the optional else block
                self.visit(node.target)
                self.visit(node.iter)
                self.process_body(node.body)
                self.process_body(node.orelse)

            def visit_While(self, node):
                # Handles while loops, checking the body and the optional else block
                self.visit(node.test)
                self.process_body(node.body)
                self.process_body(node.orelse)

            def visit(self, node):
                # Generalized visit function that tracks reachability
                if not self.reachable:
                    # Record unreachable nodes if they exist
                    self.record_unreachable(node)
                else:
                    super().visit(node)

        # Create a visitor instance and traverse the AST
        visitor = UnreachableCodeVisitor()
        visitor.visit(ast_tree)

        # Collect all violations found during traversal
        for scope, lineno in visitor.unreachable_nodes:
            self.violations.add(f"Unreachable code detected in '{scope}' at line {lineno}.")

    def __str__(self):
        # Generate a readable string representation of all violations
        string = f"{self.__class__.__name__} All Violations:\n"
        for violation in sorted(self.violations):
            string += violation + "\n"
        return string

def main():
    # Define test cases as tuples of name and code snippet
    test_cases = [
        ("Test Case 1", """
def test_case_1():
    x = 5
    return x
    y = 10  # Unreachable
"""),
        ("Test Case 2", """
def test_case_2():
    for i in range(5):
        if i == 2:
            break
        print(i)
    print("End of loop")  # Should be reachable
"""),
        ("Test Case 3", """
def test_case_3():
    for i in range(5):
        if i % 2 == 0:
            continue
            print("Skipped number")  # Unreachable
        print(i)
"""),
        ("Test Case 4", """
def test_case_4():
    x = 5
    if x > 0:
        return x
    print("This won't print")  # Unreachable
"""),
        ("Test Case 5", """
def test_case_5():
    for i in range(3):
        for j in range(3):
            if j == 1:
                continue
                print("Unreachable inner loop")  # Unreachable
            if j == 2:
                break
                print("Unreachable break")  # Unreachable
        print("Outer loop")
"""),
        ("Test Case 6", """
def test_case_6():
    x = 5
    if x > 10:
        return x
    return 0
    print("Unreachable after return")  # Unreachable
"""),
        ("Test Case 7", """
def test_case_7():
    x = 5
    y = 10
    print(x + y)
    return x
"""),
        ("Test Case 8", """
def test_case_8():
    for i in range(3):
        print(i)
    return
    print("Unreachable after return")  # Unreachable
"""),
        ("Test Case 9", """
def test_case_9():
    while True:
        break
        print("Unreachable in infinite loop")  # Unreachable
"""),
        ("Test Case 10", """
def test_case_10():
    x = 10
    for i in range(x):
        if i > 5:
            return i
            print("Unreachable in loop")  # Unreachable
    print("End of function")
""")
    ]

    # Execute the unreachable code checker for each test case
    for name, code in test_cases:
        print(f"\n{name}:")
        tree = ast.parse(code)  # Parse the code into an AST
        checker = UnreachableCodeChecker()  # Create the checker instance
        checker.run_check(tree)  # Run the check on the AST
        print(checker)  # Print the results

if __name__ == "__main__":
    main()
