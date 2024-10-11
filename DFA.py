from typing import NewType
from collections import deque as dq

#To make it easier for recursive implement of DFA;
# Helps make class as custom type for class methods to appear for programming
DFA = NewType('DFA',object) 

class DFA:

  def __init__(self,sig,q=set()):
    self.sigma = sig # Alphabet utilized
    self.states = q # Set of states; must be as set!
    self.delta = {} # Set of Transitions, , format: '{state: {symbol: {q1},...,{qn}}}'
    self.start = None #State where start of NFA begins
    self.final = set() #States where start of NFA Terminates

  # getters and setters
  

  # add state s to DFA
  def add_state(self,s):
    if s in self.states:
      return False #Flag for if state was added to self.states
    else:
      self.states.add(s)
      
      return True #Flag for if state was added to self.states
    # else:
    #   self.states.update(set())
    # pass

  # add transition (f,c,t) to DFA
  def add_transition(self,f,c,t):
    '''
    Params:
    f: from node- dict key 
    c: symbol - inner key 
    t: to node - state; type: set
    '''
    # DEBUG Prints; Uncomment to check status
    # print(t)
    # print(type(t))
    # print(f"from{f}, symbol{c}, to{t}")



    if f not in self.delta: #If already not in delta add state
      self.delta[f] = {c: t} #Add if state not there, add inner dict
    
    else:
      self.delta[f][c] = t

    
    
  def union(self,dfa2_obj: DFA): 
    
    # Perform DFA product
    # Take pair from DFA1 and DFA2 at start and enqueue from consecutive pair of state from DFAs
    # Trace both DFAs on current symbol and add both state to same set 
    # as single state in output DFA
    # END program when pairs run out from the queue
    # Designating Final state: Check if set of states has a final state from both machines
    # return union_dfa_obj
    
    # Init new DFA with union of dfas
    union_dfa_obj = DFA(sig= sorted(self.sigma.union(dfa2_obj.sigma)))
    # ^^^ Assume dfas share same sigma anyways

    # print(str_to_set(dfa2_obj.start),str_to_set(self.start))

    # Set start of union dfa to be start of both
    union_dfa_obj.start = set.union(str_to_set(self.start),str_to_set(dfa2_obj.start))
    
    queue = dq()
    queue.append(union_dfa_obj.start)
    
    # Note to self to use dq use append to enqueue; popleft to dequeue
    # print("Start: ", queue)
    
    while queue: #Empty until queue is empty
      from_union_state = queue.popleft() 
      
      
      for alphabet in self.sigma:
        to_union_state = set([]) #Init empty set for temporary storage


        for to_state in from_union_state: 
          #Potential problems here: What if the two dfas have states with the same name?


          print("keying:",set_to_str(from_union_state))
          print("On alphabet, to_state",alphabet,to_state)
          

          # if to_union_state not in union_dfa_obj.states and not union_dfa_obj.delta[set_to_str(from_union_state)][alphabet]:
          if to_state in self.states: #Check if to_state exists in dfa1
            to_union_state.add(self.delta[to_state][alphabet])
          elif to_state in dfa2_obj.states: #Check if to_states exists in dfa2
            to_union_state.add(dfa2_obj.delta[to_state][alphabet])

          # input()

        # Add transition
        union_dfa_obj.add_transition(set_to_str(from_union_state), alphabet, set_to_str(to_union_state))
        # Enqueue after pair is created
        if set_to_str(to_union_state) not in union_dfa_obj.states:
          union_dfa_obj.add_state(set_to_str(to_union_state))
          queue.append(to_union_state)
        
        print("Union_states:", union_dfa_obj.states)
        print("alphabet,to_union_state: ",alphabet,to_union_state)

    # print("union delta: ",union_dfa_obj.delta)
    # Accumlate final states
    
    for state in union_dfa_obj.states:
      
      print(str_to_set(state),self.final, dfa2_obj.final)
      if self.final.intersection(str_to_set(state)) or dfa2_obj.final.intersection(set_to_str(state)):
        union_dfa_obj.final.add(f'{state}')


    
    return union_dfa_obj


    pass

  #OPTIONAL for HW2
  def mininmize(self):
    pass

  # to String method
  def __str__(self):
    string = f"Debug print:\nstart {set_to_str(self.start)} \nfinal "
    for state in self.final:
      string += state + ' '
    string = string[:-1]
    string += '\n'
    all_trans_str = ""

    for transition in self.delta:

      for symbol in self.sigma:

        all_trans_str += f'trans {transition}:{symbol}:{self.delta[transition][symbol]}\n'
      
    
    
    return string + all_trans_str

  
def str_to_set(string_obj): #For 
  '''
  #To manipulate as a set
  Params:
  string: enter a string to convert to a set
  '''
  if ',' in string_obj:
    return set(string_obj.split(","))
  else:
    return set([string_obj])

def set_to_str(set_obj): #For storing
  '''
  Params:
  set: enter a set to convert to a str
  '''

  return ",".join(sorted(list(set_obj)))

