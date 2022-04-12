
import graphviz

class State:
    ''' 
        The State class represents each vertex of the graph 
        The attribute value represents the stored data
        The list of transition attributes represents the vertices with a connection 
    '''
    def __init__(self, value, transitions=None):
        self.value = value
        if transitions is None:
            self.transitions = []
        else:
            self.transitions = transitions

    ''' Return True if the vertex is connected with at least one vertex
    otherwiee returns false '''
    def has_transitions(self):
        if len(self.transitions) == 0:
            return False
        return True

    ''' Returns the number of vertices which have a connection '''
    def number_of_transitions(self):
        return len(self.transitions)

    ''' Adds a new connection to the transition list'''
    def add_transition_action(self, transition):
        self.transitions.append(transition)

    ''' Returns True if the action attribute exists for a given transition'''
    def has_transition_action(self, action):
        if self.has_transitions():
            for transition in self.transitions:
                if transition[1] == action:
                    return True
                    
        return False
        
    ''' Builds the text formatted veiw of a state's transitions and actions'''
    def __str__(self):
        returned_string = f"{self.value} -> "
        if self.has_transitions():
            for transition in self.transitions:
                returned_string += f"{transition[0].value} [{transition[1]}] -> "  
     
        returned_string += "None"     
        return returned_string

    ''' Builds the graphviz formatted veiw of a state's transitions and actions'''
    def add_state_to_viz(self, viz):
        if self.has_transitions():
            for transition in self.transitions:
                viz.edge(f"{self.value}", f"{transition[0].value}", label=f"{transition[1]}")
      
        return viz


class Graph:
    '''
        Graph class represents the graph data structure. 
        It contains a state attributes (list) with all the states of the graph
    '''
    def __init__(self, states=None):
        if states is None:
            self.states = []
        else:
            self.states = states


    ''' Add a new state (vertex) in the graph'''
    def add_state(self, value, transitions=None):
        self.states.append(State(value, transitions))


    '''Return True if the state with the given value exists. Otherwise it returns False'''
    def find_state(self, value):
        for state in self.states:
            if state.value == value:
                return state 
        return None


    '''Add a new transition between two states'''
    def add_transition(self, value1, value2, action=1):
        state1 = self.find_state(value1)        
        state2 = self.find_state(value2)

        if (state1 is not None) and (state2 is not None):
            state1.add_transition_action((state2, action))
        else:
            print("Error: One or more states were not found")

    def has_transition(self, value, action):
        state = self.find_state(value) 
        return state.has_transition_action(action)
        
    '''Return the number of states of the graph'''
    def number_of_states(self):
        return f"The graph has {len(self.states)} states"


    ''' Return True if the given states are connected. Otherwise return false'''
    def are_connected(self, state_one, state_two):
        state_one = self.find_state(state_one)
        state_two = self.find_state(state_two)

        for transition in state_one.transitions:
            if transition[0].value == state_two.value:
                return True
        return False
    ''' Return True if each state (except terminal) has three transitions. Otherwise return false'''
    def fully_populated(self, terminal):
        for state in self.states:
            if state.value != terminal and state.number_of_transitions()<3:
                return False
        return True

    ''' Print the graph in simple text format '''
    def __str__(self):
        graph = ""
        for state in self.states:
            graph += f"{state.__str__()}\n" 
        return graph

    ''' Generate the graph in graphviz format'''
    def graphviz_graph(self, fsm_viz):
        
        for state in self.states:
            fsm_viz.node(state.value)
            fsm_viz = state.add_state_to_viz(fsm_viz)

        return fsm_viz