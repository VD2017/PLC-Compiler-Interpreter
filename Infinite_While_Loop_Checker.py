import ast
import inspect
import Sample_Cases.LinterCases as LC
from collections import deque

class NodeChecker(ast.NodeVisitor):
    def visit_Compare(self, node):
        
        return node.left.id, node.ops[0]
        

class WhileLoopScanner(ast.NodeVisitor):
    solution_table = {
            ast.GtE : (ast.Sub, ast.Div, ast.FloorDiv, ast.Lt), # >= (-, /, //, <)
            ast.LtE : (ast.Add,ast.Mult, ast.Gt), # <=, (+,*, >)
            ast.Gt : (ast.Sub, ast.Div, ast.FloorDiv, ast.LtE), # >, (-,/,//,<=)
            ast.Lt : (ast.Add,ast.Mult, ast.GtE) # <, (+,*,>=)

        }
    
    def __init__(self):
        
        
        # Stacks 
        self.while_loop_stack = deque() #For tracking 
        self.program_scope_stack = deque() #Can be used for parent tracing
        
        
        # Temp Variables
        self.current_loop = None
        # self.vars_set = [] #[(<var_id>, <var_value>, <current_while_loop_node>)]
        self.vars_set = {} #{<var_id>: [(<var_value>, <current_while_loop_node>),..], <var_id>:...}
        

        # Flags
        self.exit_flag = False #Will set if there is an exit() under a while, even if nested
        self.if_in_function = False #Flag for checking if in function, for checking returns
        self.if_infinite_loop = False

        # search parameters when while_loop
        self.solution_table
        self.search_params = None
        self.report_loops = set() #For reporting loops that give trouble
        



    # Helper methods
    # def var_search():
    #     pass

    def add_var(self, node:ast.Name, value, current_loop):
        '''
        Adds var to self.vars_set
        '''

        if node.id in self.vars_set:
            self.vars_set[node.id].append((value, current_loop))
        else:
            # self.vars_set[node.id] = [(value, current_loop)]
            self.vars_set.update({node.id: [(value,current_loop)]})

    def return_last_var_assign(self,id):
        '''
        
        '''
    def read_value(self, node: ast.AST):
        '''
        returns value of a node
        '''
        # Returns value of based if ast.Constant or ast.Name node
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.Name) and type(node.ctx)==ast.Load:
            pass
            # print(node.id)
            # print(self.vars_set)
            # print([x[0] for x in self.vars_set])
            # Recursively search value
            # if node.id in [x[0] for x in self.vars_set]:
            #     return self.read_value(node.value)
    

    def GCD(self):
        pass

    def LCD(self):
        pass


    def visit_Compare(self, node:ast.Compare):
        # if :


        return node.left.id, type(node.ops[0])
    
    def visit_Call(self, node:ast.Call):
        EXIT = 'exit' #id of exit function
        name: ast.Name
        name = node.func
        # ONLY sets flag tot True if an exit under a current_loop
        if name.id == EXIT and type(name.ctx) == ast.Load and self.current_loop:
            self.exit_flag = True
            return self.current_loop #Will use for flag that the loops ends
            # print("Exit detected!!")
        self.generic_visit(node)

        
    def visit_FunctionDef(self, node):
        # append the current context/scope
        self.program_scope_stack.append({node: self.vars_set})
        self.if_in_function = True

        #reset variables everytime we enter new scope
        self.vars_set = {}
        # print(self.program_scope_stack)
        
        self.generic_visit(node)

        # Restore vars_set when exit inner scope
        self.vars_set = (self.program_scope_stack.pop())[node]

    def visit_Module(self, node):
        # print(self.if_in_function)
        self.generic_visit(node)
        # When finally back to module scope, reset the flag

        print("Program Scope:",self.program_scope_stack)
        if len(self.program_scope_stack) == 0: 
            self.if_in_function = False
        # print(self.if_in_function)

        
    def visit_While(self, node):
        # Begin processing node here
        if isinstance(node, ast.While):
            node: ast.While
            self.while_loop_stack.append(node)
            self.current_loop = node 
            self.if_infinite_loop = True #Only set if approaching a while loop

        # if not a while_loop
        else:
            return self.visit(node)
        
        # Check the test attribute of while block and define search parameters
        if isinstance(node.test, ast.Compare):
            self.search_params = self.visit_Compare(node.test)
            # self.solution_table[self.visit_Compare(node.test)[1]]
        elif isinstance(node.test, (ast.Constant,ast.Name)):
            # As of now Assume it's only constant^^^^, think about Name later on!!
            # print(self.read_value(node.test))

            if not self.read_value(node.test): #In the case constant == False
                self.if_infinite_loop = False

            
        
        for item in node.body:
            print("visiting body item", item)
            self.visit(item)
        print(self.vars_set)
        
        
        # print(self.vars_set)
        # variable: ast.AST
        # for variable in self.vars_set:
        #     print("reading variable", variable)
        #     print(self.read_value(variable[1]))
            
        # print(self.program_scope_stack)
        
        # If the flag is still set, append loop to 
        if self.if_infinite_loop and self.current_loop not in self.report_loops:
            self.report_loops.add(self.current_loop)
        # End of processing node here, start revisiting from last node of while loop body

        self.generic_visit(node.body[-1])
        # If exiting to outer nested loop
        if len(self.while_loop_stack)> 1:
            # print(f"exiting loop: {self.current_loop}")
            self.while_loop_stack.pop()
            
            self.current_loop = self.while_loop_stack[-1]
        # If no more nested loop set current_loop to None
        else:
            self.current_loop = None

    # def visit_Name(self, node:ast.Name):

    #     pass
        # self.generic_visit(node)
    
    # While in while-loop enforce these at visit time

    def visit_BinOp(self, node):
        print(self.current_loop)
        if self.current_loop:
            if self.current_loop == self.while_loop_stack[-1]:
                pass
        
        self.generic_visit(node)

    def visit_Break(self, node):
        
        # Note: what to do if encountered nested while loops??
        if self.current_loop and len(self.while_loop_stack) == 1:
            self.if_infinite_loop = False
        
        self.generic_visit(node)
        
            
        
        
        
        
        
    # def visit_Expr(self, node):
        
    #     if self.current_loop:
    #         pass
    #     self.generic_visit(node)

    # def visit_Pass(self, node):
    #     # Note: what to do if encountered nested while loops??
    #     if self.current_loop and len(self.while_loop_stack) == 1:
    #         self.if_infinite_loop = False
        
    #     self.generic_visit(node)
        

    def visit_Return(self, node):
        
        if self.current_loop:
            self.if_infinite_loop = False
        self.generic_visit(node)


    def visit_AugAssign(self, node):
        # print(ast.dump(node, indent=4))
        target: ast.Name
        target = node.target
        # Check if the given node is an instance of variable name is being assigned
        if isinstance(target, ast.Name) and type(target.ctx)== ast.Store and self.current_loop:
            # self.vars_set.append((target.id, node.value,self.current_loop))
            pass

            
        # self.generic_visit(node)
    
    
            
    def visit_Assign(self, node: ast.Assign):
        # print(ast.dump(node, indent=4))
        target: ast.Name
        for target in node.targets:
            # Check if the given node is an instance of variable name is being assigned
            if isinstance(target, ast.Name) and type(target.ctx)== ast.Store:
                # Append node obj to var_nodes
                # Can be a tuple. Formatted like this: (<var_id>, <var_value>, <current_while_loop_node>)
                value = self.read_value(node.value)
                self.add_var(target, value, self.current_loop)
                # self.vars_set.append((target.id, value,self.current_loop))
        self.generic_visit(node)

    # def visit_Compare(self, node):
    #     self.generic_visit(node)
    #     pass
    

class InfiniteWhileLoopChecker():
        
        def __init__(self):
            self.violations = set()
            self.if_infinite_loop_detected = False
            
            # print(self.solution_table)

        def run_check(self, ast_tree:ast.AST):
            # Initialize scanner
            my_scanner = WhileLoopScanner()
            result = my_scanner.visit(ast_tree)
            
            pass

        
    
def main():
    
    string = inspect.getsource(LC.infinite_loop)
    ast_tree = ast.parse(
        # string
'''
i = True
while True:
    # break
    i = False
    print(i)
    x = 10

y = 5

z = x + y

'''
    )
    print("ast tree:\n", ast.dump(ast_tree,indent= 4))

    
    my_checker = InfiniteWhileLoopChecker()
    my_checker.run_check(ast_tree)

if __name__ == '__main__':
    main()