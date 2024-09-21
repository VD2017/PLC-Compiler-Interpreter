import DFA as DFAclass
from collections import deque as dq
class NFA:

  def __init__(self,sig,q=set()):
    self.sigma = sig # Alphabet utilized
    self.states = q # Set of states
    self.delta = {} # Set of Transitions, format: '{state: {symbol: q1,...,qn}}'
    self.start = None #State where start of NFA begins;
    self.final = None #States where start of NFA Terminates; Stored as set

  # getters and setters

  # add state s to NFA
  def add_state(self,s):
    self.states.add(s)
  

  # add transition (f,c,t) to DFA
  def add_transition(self,f,c,t):
    '''
    Params:
    f: from node- dict key
    c: symbol -inner key
    t: to node - state
    '''
    if f not in self.delta:
      self.delta[f] = {c: set([t])}
    elif self.delta:
      if c in self.delta[f]:
        self.delta[f][c].add(t)
      else:
        self.delta[f].update({c: set([t])})
    
    

  # convert NFA to DFA, Put NTD algorithm here
  def convert_to_dfa(self): #Currently stuck here
    DFAobj = DFAclass.DFA(sig=self.sigma) #Create instance of DFA
    # print(type(self.start))
    
    DFAobj.start = '[' + self.start + ']'
    
    #Don't add empty set or all sets right away
          # DFAobj.states = self.states
    
    
    # print("NFAobj.start:",self.start)
    # queue = dq(set([self.start])) #Add as a set to avoid confusion, ensure is a list
    
    queue = [set([self.start])]

    while queue: #While not the Queue is not empty

      # print("Current Queue:",queue)

      # Dequeue dfa_state from Queue as a 'Set'
      
      # dfa_state = queue.pop() # Dequeue the current set
      
      dfa_state = queue[0] 
      
      queue = queue[1:]
      
      #Process State
      for symbol in self.sigma:
        to_state = set([]) #Init empty set

        # print('After poping dfa_state from queue is :',dfa_state, symbol) #Print dfa_state after 

        for state in dfa_state: #Take state from dfa_state set
          
          if state in self.delta and symbol in self.delta[state]:
            to_state = to_state.union(self.delta[state][symbol]) 
        
        if_added = DFAobj.add_state(set_to_str(to_state)) #Stored as a flag for appending to Queue
        # print('Printing to_state:',to_state) 

        #dfa_state & to_state can be listed as multiple states
        DFAobj.add_transition(set_to_str(dfa_state), symbol, set_to_str(to_state)) 

        if if_added: #Take flag and decide if already processed
          queue.append(to_state)


      #Set Final and Start states; Accumlate in while loop
      
      #Final: Look all DFA states & intersect with NFA final states; Setup for-loop; 
      # Possible 4-line code; Note DFA-states have become str's; Done in 2-lines :)
      # Start state:  NOTE: Convert NFA start state to string for DFA obj start state
      
      if len(set.intersection(dfa_state, self.final)) >= 1:
        # print("Sending DFA_state to DFA.final",dfa_state) DEBUG

        DFAobj.final.add(set_to_str(dfa_state))
    
    return DFAobj
    
def str_to_set(string_obj):
  '''
   #To manipulate as a set
  Params:
  string: enter a string to convert to a set
  '''
  return set(string_obj[1:-1].split(","))

def set_to_str(set_obj): #For storing
  '''
  Params:
  set: enter a set to convert to a str
  '''

  return "[" + ",".join(sorted(list(set_obj))) + "]"

  # to String method
def __str__(self):
  string = f"Debug print:\nstart {self.start} \nfinal {self.final[:]} \n"
  all_trans_str = ""
  for transition in self.delta:
    temp_trans_str = f"trans {transition}"
    
    for symbol in self.delta[transition]:
      temp_trans_str += f" {symbol}"
      for to in self.delta[transition][symbol]:
        temp_trans_str += f" {to}"

    all_trans_str += f"{temp_trans_str}\n"
  
  return string + all_trans_str

  