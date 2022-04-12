# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 16:02:56 2022

@author: gregb
"""

import socket
import random
import datetime
import graphviz
import Graph

HOST = "20.211.33.233" 
PORT = 65432
INITIAL = 'A'
TERMINAL = 'Z'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Initiate FSM & Graph
fsm = Graph.Graph()
state = client.recv(1024).decode("utf-8").rstrip()
fsm.add_state(state)
currentstate = state
loops=1

# While FSM not fully mapped
while not fsm.fully_populated(TERMINAL):
    # choose a random action number to interrogate FSM
    # helps to prevent infinite loops and ensures FSM transition exhaustion
    # TODO: examine ways to decrease number of loops. Difficulty lies in still
    #       needing to travel down already explored transitions as unexplored 
    #       segments could be further downstream in transition chain
    i = random.randint(1,3)
    
    # get the next state for this action transition
    n = client.send((str(i)+'\n').encode())  
    state = client.recv(1024).decode("utf-8").rstrip()
    
    # NOTE: behaviour differs from published FSM documentation:
    #       PUBLISHED: Upon reaching the terminal state “Z”, the server moves back to the 
    #       initial state “A” and respond to the client with both “Z” and “A”
    #       ACTUAL: sometimes the results after terminal state return only initial state 
    #       and then two states next and sometimes they return 
    #       two states straight away (ie initial state and another state)
    #       Following solution should work for both published and actual behaviour (untested for published)
    
    # Deal with the two states situation (same approach in either case)
    stateparts = state.partition('\n')
    
    if stateparts[2] !='' and stateparts[2] is not None:
        currentstate=stateparts[0]
        state=stateparts[2]
        
    # deal with the 'only initial state' situation
    if currentstate != TERMINAL and state != INITIAL:
        # add the state if it doesn't exist
        if not fsm.find_state(state):
            fsm.add_state(state)
        
        # add the transistion/action if it doesn't exist
        if not fsm.has_transition(currentstate,i):
            fsm.add_transition(currentstate, state, i)

    if (currentstate==TERMINAL):
        print('Finite State Machine pass #' + str(loops) + '...') 
        loops+=1
    
    currentstate = state
    
# get fully mapped FSM as graphviz object
#print(fsm)
date = datetime.datetime.now()
dt=date.strftime("%Y%m%d_%H%M%S")
fsm_viz = graphviz.Digraph('finite_state_machine', filename='fsm_'+dt+'.gv', directory='FSMs')
fsm_viz.attr(rankdir='TB', size='8,5')
fsm_viz.attr('node', shape='circle')
fsm_viz = fsm.graphviz_graph(fsm_viz)

# save and view as pdf
fsm_viz.view()

print ('Disconnect.')
client.close()
exit()


  