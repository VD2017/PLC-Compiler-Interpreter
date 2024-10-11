from DFA import *
# Driver Program
#To run HW2 Example
# Note had to modify program to fit my DFA class

def main():
  dfa1 = DFA({'a','b'},{'q0','q1'})
  dfa1.start= 'q0'
  dfa1.final = {'q0'}
  dfa1.add_transition('q0','a','q1')
  dfa1.add_transition('q0','b','q1')
  dfa1.add_transition('q1','a','q0')
  dfa1.add_transition('q1','b','q0')
  print(dfa1.delta)
  

  

  dfa2 = DFA({'a','b'},{'q2','q3'})
  dfa2.start = 'q2'
  dfa2.final = {'q3'}
  dfa2.add_transition('q2','a','q3')
  dfa2.add_transition('q2','b','q2')
  dfa2.add_transition('q3','a','q3')
  dfa2.add_transition('q3','b','q2')
  print(dfa2.delta)
  dfa = dfa1.union(dfa2)

  print(dfa)
if __name__ == "__main__":
    main()