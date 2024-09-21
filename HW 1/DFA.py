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
    # print(t)
    # print(type(t))
    # print(f"from{f}, symbol{c}, to{t}")



    if f not in self.delta: #If already not in delta add state
      self.delta[f] = {c: t} #Add if state not there, add inner dict
    # elif self.delta: 
    # elif c in self.delta[f]: #If symbol exists, add to_state
    else:
      self.delta[f][c] = t

    # else: #currently having trouble adding empty set
    #   if t != set():
    #     self.delta[f].update({c: set([t])})
    #   else:
    #     self.delta[f].update({c: set(t)})


  # to String method
  def __str__(self):
    string = f"Debug print:\nstart {self.start} \nfinal {set_to_str(self.final)} \n"
    all_trans_str = ""

    for transition in self.delta:

      for symbol in self.sigma:

        all_trans_str += f'trans {transition}:{symbol}:{self.delta[transition][symbol]}\n'
      
    # for transition in self.delta:
    #   temp_trans_str = f"trans {transition}"
      
    #   for symbol in self.delta[transition]:
    #     temp_trans_str += f" {symbol}"
    #     for to in self.delta[transition][symbol]:
    #       temp_trans_str += f" {to}"

    #   all_trans_str += f"{temp_trans_str}\n"
    
    return string + all_trans_str

  
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