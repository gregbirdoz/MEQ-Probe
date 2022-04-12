# MEQ-Probe Developer Challenge
Python solution created as per the python developer challenge.pdf

## A selection of generated state machine graphs can be found in the folder FSMs

### NOTE: behaviour of Finite State Machine differs from published FSM documentation:

#### PUBLISHED: 
Upon reaching the terminal state “Z”, the server moves back to the initial state “A” and respond to the client with both “Z” and “A”.

#### ACTUAL: 
Sometimes the results after terminal state return only initial state (ie "A\<LF\>") and then two states on next query (eg "L\<LF\>B\<LF\>") and sometimes it returns two states straight away (ie initial state and another state "A\<LF\>L\<LF\>").

#### The solution should work for both the published and actual behaviours (untested for published).
