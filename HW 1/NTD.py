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
  temp = tree[2][0:]
  temp2 = []
  for tuple in temp:
    if tuple[1] not in temp2:
      temp2 += tuple[1]
  return set(temp2)

def NFA_construction(tree):
  NFA_obj = NFAclass.NFA(sig=get_sigma(tree))
  NFA_obj.start = tree[0]
  NFA_obj.final = set(tree[1])
  
  #Adding states to state set
  # NFA_obj.add_state(tree[0])
  # for state in tree[1]:
  #   NFA_obj.add_state(state)

  for transition in tree[2]:
    NFA_obj.add_transition(transition[0],transition[1],transition[2])
    if transition[0] not in NFA_obj.states and transition[0] not in NFA_obj.sigma:
      NFA_obj.add_state(transition[0])
    if transition[2] not in NFA_obj.states and transition[2] not in NFA_obj.sigma:
      NFA_obj.add_state(transition[2])

  # sorted(NFA_obj.states)

    # for state in transition:
    #   if state in NFA_obj.states: #If already in state skip
    #     continue
    #   if state not in NFA_obj.sigma: #If an alphabet skip over
    #     NFA_obj.add_state(state)

  return NFA_obj

# def read_input():
#   result = ''
#   while True:
#     data = input().strip() 
#     if ' ' in data:
#       i = data.index(' ')
#       result += data[0:i+1]
#       break
#     else:
#       result += data + ' '
#   return result

def main():
  with open(sys.argv[1]) as file:

  
    string = file.read()
  print(f"Found in \'{file.name}\':\n ",string)
  tree = parser.parse(string) #Parse into string into AST
  
  n1 = NFA_construction(tree)
  # print(n1.sigma)
  # print(n1.delta)
  # print(n1.states)
  
  d1 = n1.convert_to_dfa()
  # print("DFA.obj transitions: ",d1.delta)
  # print("DFA.obj start: ",d1.start)
  # print("DFA.obj final: ",d1.final)
  print("DFA.obj __str__ method:", d1)

main()