# PLC-Compiler-Interpreter

-Current prototype build of my HW1 for NFA to DFA conversion
-To run use terminal command to enter arguments: like this:
python3 NTD.py <nfa_file.nfa>

NOTE: nfa_file.nfa is a txt file that contains a Non-finite Automata formatted like this:
start <start_state> 

final <final_state,...more_final_states> 

trans <from_state>:<symbol>:<to_state> 
.
.
.

trans ...

see n1.nfa as example
