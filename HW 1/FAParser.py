import ply.yacc as yacc

from FALexer import tokens

# START OF GRAMMAR RULES
def p_dfa(p):
  'dfa : start final transitions' #Start of States of a DFA
  p[0] = (p[1],p[2],p[3])


def p_start(p):
  # Must have only one start state
  'start : START NAME'
  p[0] = p[2]


def p_final(p): 
  # Can have multiple final states 
  'final : FINAL names'
  p[0] = p[2]

def p_names_1(p): 
  #Implies empty state
  'names : '
  p[0] = []

def p_names_2(p):
  #Implies multiple states
  'names : names NAME'
  p[0] = p[1] + [p[2]]

# Transitions & Transitions from State to State

def p_transitions_1(p):
  'transitions : ' #Base case if empty transition
  p[0] = []

def p_transitions_2(p):
  'transitions : transitions transition' #Implies recursion, and cycles of pattern
  p[0] = p[1] + [p[2]]


def p_transition_1(p): 
  'transition : TRANS NAME COLON NAME COLON NAME' #Implies nonempty transition from one state to another
  p[0] = (p[2],p[4],p[6])

def p_transition_2(p):
  'transition : TRANS NAME COLON COLON NAME' #Implies empty transition from one state to another
  p[0] = (p[2],"",p[5])

def p_error(p):
  print("Syntax error in input!")

# END OF GRAMMAR RULES
# Create Parser Tree from grammar above
parser = yacc.yacc()