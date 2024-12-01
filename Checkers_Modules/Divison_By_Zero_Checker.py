import ast
import inspect
from collections import deque
# import Sample_Cases.LinterCases.py as LC

if __name__ == "__main__":
    from Base_Checker import checker_base

else:
    from .Base_Checker import checker_base

class DivisionOperatorChecker(ast.NodeVisitor):
    # Visits instances of the division operator being used
    def __init__(self):
        self.div_nodes = []
        # For most recent assignment of variables
        self.var_assignments = {}
        self.program_scope_stack = deque()

    # def visit_Module(self, node):
    #     # To reset scope when entering a python Module
    #     self.div_nodes = []
    #     self.generic_visit(node)


    # Reset scope when visiting class definition
    def visit_ClassDef(self, node):
        self.program_scope_stack.append(node)
        self.var_assignments = {}
        self.generic_visit(node)
        self.program_scope_stack.pop()

    # Reset scope when entering function
    def visit_FunctionDef(self, node):
        self.program_scope_stack.append(node)
        self.var_assignments = {}
        self.generic_visit(node)
        self.program_scope_stack.pop()

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(node.value, ast.Constant):
                self.var_assignments[target.id] = node.value.value
        self.generic_visit(node)

    def visit_BinOp(self, node):
        
        # Check if that instance is div operation and the right operand is a constant
        if type(node.op) == ast.Div:
            # Check if the right constant is 0
            is_Constant = type(node.right) == ast.Constant
            if isinstance(node.right, ast.Constant):
                if node.right.value == 0:
                    self.div_nodes.append(node)
            # Consider check for id of var name
            elif isinstance(node.right, ast.Name):
                # If variable is not assigned in a func body assume it's a unbound arg
                if node.right.id in self.var_assignments and self.var_assignments[node.right.id] == 0:
                    self.div_nodes.append(node)

        self.generic_visit(node)


class DivisionByZeroChecker(checker_base):
    def __init__(self):
        super().__init__()
        self.if_has_div_by_zero = False #Flag
        self.binary_operator_nodes = []
        self.assign_nodes = set()

    def import_vars_from_visitor(self,nodes: list[ast.BinOp]):
        '''
        Params:
        nodes: this is where you want to import the assignment nodes 
        from your VariableNameChecker instance
        '''
        self.binary_operator_nodes = self.binary_operator_nodes + nodes

    def run_check(self, ast_tree:ast.AST):
        # Run visit
        my_scanner = DivisionOperatorChecker()
        my_scanner.visit(ast_tree)

        # Import the nodes
        self.import_vars_from_visitor(my_scanner.div_nodes)

        node: ast.BinOp
        for node in self.binary_operator_nodes:
            # print(node)
            # is_Constant = type(node.right) == ast.Constant
            self.if_has_div_by_zero = True
            self.violations.add(f"Division by Zero at {node.left.id} / 0 at line {node.lineno}")

            # if isinstance(node.right, ast.Constant):
            #     if node.right.value == 0:
            #         self.if_has_div_by_zero = True
            #         self.violations.add(f"Division by Zero at {node.left.id} / 0 at line {node.lineno}")
            # elif isinstance(node.right, ast.Name):
            #     get_name = node.right.id

        # Print all current violations
        # print(self)

    def __str__(self):
        string = f"{self.__class__.__name__} All Violations:\n"
        for violation in self.violations:
            string += violation +"\n"
        return string
        
    

def main():
    # Currently Using example where the right operand is a constant of 0
    string = '''
def divide_numbers(a, b):
    if b == 0:
        return "Cannot divide by zero!"
    return a / b

    '''
    # This function divides by 0

    ast_tree = ast.parse(string)



    print("ast tree:\n", ast.dump(ast_tree,indent= 4))
    # Scan for var assignmens
    # print("Scanning for Var assignments")
    # Init Var checker 

    # print(type(ast_tree))
    # my_scanner = DivisionOperatorChecker()
    # my_scanner.visit(ast_tree)
    # print(my_scanner.div_nodes)
    # for count, node in enumerate(my_scanner.div_nodes):

    #     print(f'Binary Node {count}:\n',ast.dump(node,indent= 4))
    


    # Case where operand is a assigned variable

    # Init and Run DivisionChecker
    my_checker = DivisionByZeroChecker()
    # my_checker.import_vars_from_visitor(ast_tree)
    # print(my_checker.binary_operator_nodes)
    my_checker.run_check(ast_tree)
    print(my_checker)
    

if __name__ == '__main__':
    main()