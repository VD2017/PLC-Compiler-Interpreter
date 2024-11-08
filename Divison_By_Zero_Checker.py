import ast
import inspect
import Sample_Cases.LinterCases as LC

class DivisionOperatorChecker(ast.NodeVisitor):
    # Visits instances of the division operator being used
    def __init__(self):
        self.div_nodes = []

    # def visit_Module(self, node):
    #     # To reset scope when entering a python Module
    #     self.div_nodes = []
    #     self.generic_visit(node)

    # def visit_FunctionDef(self,node):
    #     # To reset scope when entering a FunctionDef
    #     # Note Should make more stable for nested functions in python modules
    #     # print("entered Function definition")
    #     self.div_nodes = []
    #     self.generic_visit(node)
        
    def visit_BinOp(self, node):
        
        # Check if that instance is div operation and the right operand is a constant
        if type(node.op) == ast.Div:
            # Check if the right constant is 0
            is_Constant = type(node.right) == ast.Constant
            if is_Constant:
                if node.right.value == 0:
                    self.div_nodes.append(node)
            # Consider check for id of var name
            else:
                pass
        self.generic_visit(node)


class DivisionByZeroChecker():
    def __init__(self):
        self.violations = set()
        self.if_has_div_by_zero = False #Flag
        self.binary_operator_nodes = []

    def import_vars_from_visitor(self,nodes: list[ast.BinOp]):
        '''
        Params:
        nodes: this is where you want to import the assignment nodes 
        from your VariableNameChecker instance
        '''
        self.binary_operator_nodes = self.binary_operator_nodes + nodes

    def run_check(self,input_tree):
        # Run visit
        my_scanner = DivisionOperatorChecker()
        my_scanner.visit(input_tree)

        # Import the nodes
        self.import_vars_from_visitor(my_scanner.div_nodes)

        node: ast.BinOp
        for node in self.binary_operator_nodes:
            # print(node)
            is_Constant = type(node.right) == ast.Constant
            if is_Constant:
                if node.right.value == 0:
                    self.if_has_div_by_zero = True
                    self.violations.add(f"Division by Zero at {node.left.id} / 0")
        # Print all current violations
        print(self)

    def __str__(self):
        string = f"{self.__class__.__name__} All Violations:\n"
        for violation in self.violations:
            string += violation +"\n"
        return string
        
    

def main():
    # Currently Using example where the right operand is a constant of 0
    string = inspect.getsource(LC.divide_by_constant)
    # This function divides by 0

    ast_tree = ast.parse(string)



    print("ast tree:\n", ast.dump(ast_tree,indent= 4))
    # Scan for var assignmens
    print("Scanning for Var assignments")
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
    

if __name__ == '__main__':
    main()