import ast
import inspect
import Sample_Cases.LinterCases as LC
from collections import deque

class WhileLoopScanner(ast.NodeVisitor):
    def __init__(self):
        self.while_loop_stack = deque()
        self.program_scope_stack = deque() #Can be used for parent tracing
        self.current_loop = None
        self.if_in_function = False #Flag for checking if in function
        self.vars_set = set() # Can be a tuple. Formatted like this: (<var_id>, <var_value>, <current_while_loop_node>)


    def visit_Call(self, node:ast.Call):
        EXIT = 'exit' #id of exit function
        name: ast.Name
        name = node.func
        if name.id == EXIT and type(name.ctx) == ast.Load:
            self.exit_flag = True
            # print("Exit detected!!")
        self.generic_visit(node)

        
    def visit_FunctionDef(self, node):
        # append the current context/scope
        self.program_scope_stack.append({node: self.vars_set})
        self.if_in_function = True
        #reset variables everytime we enter new scope
        self.vars_set = set() 
        print(self.program_scope_stack)
        
        self.generic_visit(node)

        # Restore vars_set when exit inner scope
        self.vars_set = (self.program_scope_stack.pop())[node]
        # When finally back to module scope
        if len(self.program_scope_stack) == 0: 
            self.if_in_function = False

        
    def visit_While(self, node:ast.While):
        if isinstance(node, ast.While):
            self.while_loop_stack.append(node)
            self.current_loop = node 
        # if type(node) == ast.While:
        # print(ast.dump(node,indent=4))
        print(self.vars_set)
        print(self.program_scope_stack)
        # print("While_loop stack",self.while_loop_stack)
        self.generic_visit(node)
        
        # If exiting to outer nested loop
        if self.while_loop_stack:
            print(f"exiting loop: {self.current_loop}")
            self.current_loop = self.while_loop_stack.pop()
        # If no more nested loop set current_loop to None
        else:
            self.current_loop = None

    def visit_Name(self, node:ast.Name):

        pass
        # self.generic_visit(node)

    def visit_AugAssign(self, node):
        # print(ast.dump(node, indent=4))
        self.generic_visit(node)
    
    def read_value(self, node: ast.AST):
        # Returns value of based if ast.Constant or ast.Name node
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Name) and type(node.ctx)==ast.Load:
            # read tuple here
            return self.read_value()
            


    def visit_Assign(self, node: ast.Assign):
        print(ast.dump(node, indent=4))
        target: ast.Name
        for target in node.targets:
            # Check if the given node is an instance of variable name is being assigned
            if isinstance(target, ast.Name) and type(target.ctx)== ast.Store:
                # Append node obj to var_nodes
                # Can be a tuple. Formatted like this: (<var_id>, <var_value>, <current_while_loop_node>)
                self.vars_set.add((target.id, node.value,self.current_loop))
        self.generic_visit(node)

    def visit_Compare(self, node):
        self.generic_visit(node)
        pass
    

class InfiniteWhileLoopChecker():
        solution_table = {
            ast.GtE : (), # >= ()
            ast.LtE : (), # <=, ()
            ast.Gt : (), # >, ()
            ast.Lt : () # <, 

        }

        def __init__(self):
            self.solution_table
            print(self.solution_table)

        def run_check(self):
            pass

        
    
def main():
    
    string = inspect.getsource(LC.infinite_loop)
    ast_tree = ast.parse(string)
    # print("ast tree:\n", ast.dump(ast_tree,indent= 4))

    my_scanner = WhileLoopScanner()
    my_scanner.visit_While(ast_tree)
    # my_checker = InfiniteWhileLoopChecker()


if __name__ == '__main__':
    main()