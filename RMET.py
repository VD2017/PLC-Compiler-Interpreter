# NTD.py
from FAParser import parser
import sys
import DFA
import NFA as NFAclass
from collections import deque as dq
def get_sigma(tree: tuple):
  '''
  Returns Alphabet/Sigma of AST
  Params:
  tree : Input AST as a tuple. 
  '''
  temp = tree[2][0:] #sublist of transitions
  temp2 = [] 
  # Accumlate symbols from transitions
  for tuple in temp:
    # If not already in symbols
    if tuple[1] not in temp2:
      temp2 += tuple[1]
  
  
  
  return set(temp2)

def NFA_construction(tree):
  NFA_obj = NFAclass.NFA(sig=get_sigma(tree))
  # Set start & final states
  NFA_obj.start = tree[0]
  NFA_obj.final = set(tree[1])
  
  # initialize transitions for each state
  for transition in tree[2]:
    NFA_obj.states.add(transition[0])
    NFA_obj.states.add(transition[2])

  # initialize empty set for each state
  for state in NFA_obj.states:
    NFA_obj.delta[state] = {}
    for symbol in NFA_obj.sigma:
      NFA_obj.delta[state][symbol] = set() #Init on alphabet to empty set
    NFA_obj.delta[state][''] = set() #Init on empty transition to empty set
  

  # Collect transitions and add states to self.state in NFAobj
  for transition in tree[2]:
    NFA_obj.add_transition(transition[0],transition[1],transition[2])

    # From_state
    if transition[0] not in NFA_obj.states and transition[0] not in NFA_obj.sigma:
      NFA_obj.add_state(transition[0]) #Add state to NFA

    # To_state
    if transition[2] not in NFA_obj.states and transition[2] not in NFA_obj.sigma:
      NFA_obj.add_state(transition[2]) #Add state to NFA
  
  

  return NFA_obj



def main():
  # Driver Code for RMET
  with open(sys.argv[1]) as file:
  # For this HW give nfa with E-closures as arg
  
    string = file.read()
  # print(f"Found in \'{file.name}\':\n ",string)
  tree = parser.parse(string) #Parse into string into AST
  
  ne1 = NFA_construction(tree)
  # DEBUG prints for nfa obj
  # print("n1 start:",n1.start)
  # print("n1 final:",n1.final)
  # print("n1 sigma:",ne1.sigma)
  # print("n1 delta:", ne1.delta)
  # print("n1 states",ne1.states)

  print(ne1)
  
  # ne1.RMET()

  n1 = ne1.RMET()
  
  print(n1.states)
  
  print("n1.delta without E",n1.delta)
  print(n1)
  # print(n1) #Currently does not work because

main()