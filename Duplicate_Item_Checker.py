import ast
import inspect
import Sample_Cases.LinterCases as LC

class VariableNameChecker(ast.NodeVisitor):
    # For visiting Nodes where variables are defined
    def __init__(self):
        self.var_nodes = []

    # Define what happens when ast.NodeVisitor visits a Assign node
    def visit_Assign(self, node):
        # Visit Target where variables are assigned
        
        if node.__class__.__name__ == "Assign":
            # print(node)
            for target in node.targets:
                # Check if the given node is an instance of variable name is being assigned
                if isinstance(target, ast.Name):
                    # Append node obj to var_nodes
                    self.var_nodes.append(node)
            
        self.generic_visit(node)

        

    def print_vars(self):
        # Probably use __str__ in the future
        # print(type(self.var_nodes[0]))
        print("Printing Detected variables and their values", self.var_nodes)
        var_node: ast.Assign
        for var_node in self.var_nodes:
            out_string = f'{var_node.targets[0].id} = '
            
            # The print out the r_value of the variable itself

            # if the binding is to a another variable name
            if type(var_node.value) == ast.Name:
                out_string += str(var_node.value.id)
            # if the binding is a constant/int
            else:
                out_string += str(var_node.value.value)

            print(out_string)



class DuplicateVarChecker(): 
    
    def __init__(self):
        # store violations in a set
        self.violations = set()
        self.if_has_duplicate = False #Flag if there is atleast one violation from running the check
        self.vars_dict = {}

    def import_vars_from_visitor(self,vars_nodes: list[ast.Assign]):
        '''
        Params:
        vars_nodes: this is where you want to import the assignment nodes 
        from your VariableNameChecker instance
        '''
        node : ast.Assign
        
        for node in vars_nodes:
            
            name = node.targets[0].id
            self.vars_dict.update({name: None})
            # Currently accounting for variable names and ints/constants
            # if the binding is to a another variable name
            if type(node.value) == ast.Name:
                self.vars_dict[name] = node.value.id

            # if the binding is a constant/int
            else:
                # out_string += str(var_node.value.value)
                self.vars_dict[name] = node.value.value

            

    def run_check(self):
        set_of_names = set(self.vars_dict.keys())
        set_of_values = set(self.vars_dict.values())
        
        # set self.if_has_duplicate flag based on a set intersection 
        # if there exists atleast one duplicate
        if len(set.intersection(set_of_names, set_of_values)) > 0:
            # Note/potential bug: should probably update this to be left-most intersection(var names) 
            # to intersection only variables names! 
            self.if_has_duplicate = True # Set flag
            where_set = set.intersection(set_of_names, set_of_values) # Store what duplicates are being referenced in a set
            
        else:
            return print(f"{self.__class__.__name__}:No violations detected!")
        
        # If the flag is set store and print a violation
        if self.if_has_duplicate:
            print(f"{self.__class__.__name__}: Has a violation!")
            print("Storing violation(s)")
            
            # Probably could optimize this; (T: O(n))
            for name, value in self.vars_dict.items():
                if value in where_set: 
                    self.violations.add(f"Duplicate at {name} = {value}")
            print("All violations:\n",self.violations)




        

    def store_violation(self):
        
        pass
    

class Linter(VariableNameChecker, DuplicateVarChecker):
    # Was planning on create a linter class
    pass

def main():
    # Currently Using example where  
    string = inspect.getsource(LC.duplicate_variables)

    ast_tree = ast.parse(string)
    


    print("ast tree:\n", ast.dump(ast_tree,indent= 4))
    # Scan for var assignmens
    print("Scanning for Var assignments")
    # Init Var checker 
    my_var_scanner = VariableNameChecker()
    my_var_scanner.visit_Assign(ast_tree)
    my_var_scanner.print_vars()


    # Init and Run DuplicateChecker
    my_duplicate_checker = DuplicateVarChecker()
    my_duplicate_checker.import_vars_from_visitor(my_var_scanner.var_nodes)
    print(my_duplicate_checker.vars_dict)
    my_duplicate_checker.run_check()

if __name__ == '__main__':
    main()