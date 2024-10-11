import DFA as DFAclass
from collections import deque as dq
class NFA:

  def __init__(self,sig,q=set()):
    self.sigma = sig # Alphabet utilized
    self.states = q # Set of states; stored as a set
    self.delta = {} # Set of Transitions, format: '{state: {symbol: q1,...,qn}}'
    self.start = None #State where start of NFA begins; Stored as lone str
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
      # self.delta[f] = {c: set([t])}
      self.delta[f] = {}
      if type(t) == set:
        self.delta[f] = {c: set.union(t)}
      else:
        self.delta[f] = {c: set([t])}

    elif self.delta:
      if c in self.delta[f] and type(t) == str:
        self.delta[f][c].add(t)
      else:
        if type(t) == set and c in self.delta[f]:
          print(f"union set on {c}")
          self.delta[f][c] = self.delta[f][c].union(t)
        else:
          print(f"update set on {c}")
          self.delta[f].update({c: t}) #Note not safe for str only as of RMET implement!!!
    # if f not in self.delta: #If already not in delta add state
    #   self.delta[f] = {c: t} #Add if state not there, add inner dict
    
    # else:
    #   self.delta[f][c] = t


  def RMET(self):
    #Elipison Closure method to find e-closure 
    # Pseudocode
    # Process from_state with symbol ''
    # For every non-E in alphabet 
        # for every to_state2 on to_state1
          # process on E-closure
      # process to_state on non-E alphabet
    
    def e_closure(nfa_state): #Helper function; Consider moving method outside
      
      to_state_empty = set([]) #Init empty set
      # Note: code in empty-to-empty transition
      # Some states may require multiple iterations
      to_state_empty.add(nfa_state) #Add itself
      # print(nfa_state,to_state_empty)
      queue = [set([nfa_state])]
      change = False
      while queue:
        # set_len = len(to_state_empty) # Changed len flag if there was an add or not from union
        to_state_set = queue[0]
        queue = queue[1:]
        # if self.delta[set_to_str(current_state)]['']:
        #   to_state_empty.add(self.delta[set_to_str(current_state)][''])
        for to_state in to_state_set:
          # print("to_state:", to_state)
          # print(to_state, self.delta[to_state][''])

          if to_state in self.delta and self.delta[to_state][''] not in to_state_empty:
            # to_state_empty.add(self.delta[to_state][''])
            to_state_empty = to_state_empty.union(self.delta[to_state][''])
            queue.append(self.delta[to_state][''])
          elif to_state in self.states and to_state not in self.delta:
            to_state_empty = to_state_empty.union(set({to_state}))

        # print(to_state_empty)


      return to_state_empty

    def direct_trans(nfa_state, symbol):
      # to_state_direct = set([]) #Init empty set
      # if nfa_state in self.delta and symbol in self.delta[nfa_state]: #If symbol exists in that state
      #   for direct_tran in self.delta[nfa_state][symbol]:
      #     to_state_direct.add(direct_tran)

      # return to_state_direct #Return states that lead symbol
      if symbol in self.delta[nfa_state]:
        return self.delta[nfa_state][symbol]
      else:
        # Flag if symbol not in nfa_state transition
        return False


    
    # Initialize Queue for processing empty states
    # queue = dq()

    #Transfer attributes to new_nfa_obj
    new_nfa_obj = NFA(sig = self.sigma)
    new_nfa_obj.states = self.states
    new_nfa_obj.start = self.start

    # Dictionary to store e-closures 
    first_on_empty_states_dict = {}

    #First empty closure(Most inner)
    for from_state in self.states: 
      #Add to dict if has multiple trans on empty
      if from_state in self.delta and '' in self.delta[from_state]: 
        
        first_on_empty_states = e_closure(from_state)
        first_on_empty_states_dict.update({from_state: first_on_empty_states})
      # print("from_state, E-closure:",from_state, ',', first_on_empty_states)
      else: #Add only self if single or no transitions; Implicit case
        first_on_empty_states_dict.update({from_state: set([from_state])})


    
    # print("first_on_empty_states_dict:",first_on_empty_states_dict)
    

    # Inner direct transition
    
    for alphabet in self.sigma:
      for from_state in first_on_empty_states_dict:
        # to_state_direct_set = direct_trans(from_state,alphabet)
        # print("from_state",from_state)

        # Store to_state on alphabet in temp var
        temp1 = set([])
        for to_state in first_on_empty_states_dict[from_state]:

          if to_state in self.delta and alphabet in self.delta[to_state]:
            temp1 = temp1.union(direct_trans(to_state, alphabet))
            
            # second_on_empty_states = self.delta[to_state][alphabet]
        
        
        
        
        if temp1: #Only add if temp1 isn't empty
          # Add transition
          for to_state in temp1:
            
            print(from_state, alphabet, first_on_empty_states_dict[to_state])
            new_nfa_obj.add_transition(from_state, alphabet, first_on_empty_states_dict[to_state])
            print(new_nfa_obj.delta)
          

    # Set final states
    new_nfa_obj.final = self.final
    # temp_final_states = set([])
    

    # for state in new_nfa_obj.states:
    #   if state in new_nfa_obj.delta:

    #     if self.final in new_nfa_obj.delta[state].values():
    #       temp_final_states.add(state)
    # new_nfa_obj.final = temp_final_states
          
          
    # print(inner_direct_trans)

        # print(to_state_direct_set)
        

    # print("Dictionary:",direct_trans_dict)

    

    # Add transitions to new_nfa_obj
    

    # print(new_nfa_obj) #DEBUG print to prove success
    return new_nfa_obj
    

  # convert NFA to DFA, Put NTD algorithm here
  def convert_to_dfa(self): 
    DFAobj = DFAclass.DFA(sig=self.sigma) #Create instance of DFA
    
    
    DFAobj.start = '[' + self.start + ']'
    
    #Don't add empty set or all sets right away
          
    
    
    # print("NFAobj.start:",self.start)
    # queue = dq(set([self.start])) #Add as a set to avoid confusion, ensure is a list
    
    queue = [set([self.start])]

    while queue: #While not the Queue is not empty

      # OPTIONAL TASK: USE DEQUE Library
      # print("Current Queue:",queue)
      # Dequeue dfa_state from Queue as a 'Set'
      # dfa_state = queue.pop() # Dequeue the current set
      
      #Current Implementation of Queue(Python Array)
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
    


  # to String method
  def __str__(self):
    #NOTE to self: redo this method for HW2, it was messy in the HW1

    # Add start & final state from nfa obj
    string = f"Debug print:\nstart {self.start} \nfinal"
    for state in self.final:
      string += f" {state}"
    string += '\n'

    all_trans_str = ""

    sigma_with_empty = [alphabet for alphabet in self.sigma]
    sigma_with_empty.append("")
    for from_state in self.delta:

      for symbol in sigma_with_empty:
        if symbol in self.delta[from_state]:

          all_trans_str += f'trans {from_state}:{symbol}:{self.delta[from_state][symbol]}\n'
        
        # elif symbol:
        #   all_trans_str += f'trans {from_state}:\'\':{self.delta[from_state][symbol]}\n'

      
    
      
    return string + all_trans_str

    # string = f"Debug print:\nstart {self.start} \nfinal {self.final[:]} \n"
    # all_trans_str = ""
    # for transition in self.delta:
    #   temp_trans_str = f"trans {transition}"
      
    #   for symbol in self.delta[transition]:
    #     temp_trans_str += f" {symbol}"
    #     for to in self.delta[transition][symbol]:
    #       temp_trans_str += f" {to}"

    #   all_trans_str += f"{temp_trans_str}\n"
    
    # return string + all_trans_str

def str_to_set(string_obj): #For manipulating
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