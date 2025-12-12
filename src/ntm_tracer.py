from src.helpers.turing_machine import TuringMachineSimulator


# ==========================================
# PROGRAM 1: Nondeterministic TM [cite: 137]
# ==========================================
class NTM_Tracer(TuringMachineSimulator):
    def run(self, input_string, max_depth):
        """
        Performs a Breadth-First Search (BFS) trace of the NTM.
        Ref: Section 4.1 "Trees as List of Lists" [cite: 146]
        """
        print(f"Tracing NTM: {self.machine_name} on input '{input_string}'")

        # Initial Configuration: ["", start_state, input_string]
        # Note: Represent configuration as triples (left, state, right) [cite: 156]
        # adding the transition id to the end; -1 signifies the starting state and -2 is a placeholder for transitions to the reject
        initial_config = ["", self.start_state, input_string, -1]

        # The tree is a list of lists of configurations
        tree = [[initial_config]]

        depth = 0
        number_transitions_taken = 0
        accepted = False
        accepted_final_state = []

        while depth < max_depth and not accepted:
            current_level = tree[-1]
            next_level = []
            all_rejected = True

            # TODO: STUDENT IMPLEMENTATION NEEDED
            # 1. Iterate through every config in current_level.
            # 2. Check if config is Accept (Stop and print success) [cite: 179]
            # 3. Check if config is Reject (Stop this branch only) [cite: 181]
            # 4. If not Accept/Reject, find valid transitions in self.transitions.
            # 5. If no explicit transition exists, treat as implicit Reject.
            # 6. Generate children configurations and append to next_level[cite: 148].

            # each con is a list of the NTM configurations (think the path)
            # 1. Iterate through every config in current_level.
            for s_id, state in enumerate(current_level):
                current_state = state[1]
                transition_taken = False
                
                # Check if the configuration is at the accept or reject state. If accepted, print this. Else, stop this configuration from continuing by not adding to the config
                # 2. Check if config is Accept (Stop and print success) [cite: 179]
                if current_state == self.accept_state:
                    print("Success.")
                    accepted = True
                    accepted_final_state = state
                    break
                    # 3. Check if config is Reject (Stop this branch only) [cite: 181]
                elif accepted:
                    break 
                elif current_state == self.reject_state:
                    continue
                
                reading_char = state[2][0]
                left_string = state[0]
                right_string = state[2][1:]

                transition_taken = False

                # 4. If not Accept/Reject, find valid transitions in self.transitions.
                for t_id, transition in enumerate(self.transitions[current_state]):
                    if reading_char == transition['read'][0]:
                        number_transitions_taken += 1
                        # found a valid transition
                        new_state = transition["next"]
                        write_char = transition["write"][0] 

                        if transition["move"][0] == "R":
                            # check that we can move to the right
                            if len(right_string) == 0:
                                right_string = "_"
                            new_left = state[0] + write_char
                            new_right = right_string
                        elif transition["move"][0] == "L":
                            # check that we can move to the left
                            if state[1] == "q0" and new_state == "q1" and left_string == "11":
                                print("LEFT")
                                print(left_string)
                                print("Right " +state[2][1:])
                            if len(left_string) == 0:
                                left_string = "_"
                            new_right = left_string[len(left_string)-1] + write_char + state[2][1:]
                            new_left = left_string[:-1]
                        else: # Stay
                            new_left = left_string
                            new_right = write_char + state[2][1:]
                            
                        
                        new_conf = [[new_left, new_state, new_right, [s_id, t_id]]]
                        next_level += new_conf
                        transition_taken = True
                        all_rejected = False
                
                # 5. If no explicit transition exists, treat as implicit Reject.
                if not transition_taken:
                    new_conf = [[left_string + reading_char, self.reject_state, right_string, -2]]
                    next_level += new_conf
            
            # 6. Generate children configurations and append to next_level[cite: 148].
            # if at this level, there was an accept, we do not need to keep exploring
            if not accepted:
                tree.append(next_level)
                depth += 1

            # Placeholder for logic:
            if not accepted and all_rejected:
                # TODO: Handle "String rejected" output [cite: 258]
                print(f"String rejected in {depth} steps")
                break

        if depth >= max_depth:
            print(f"Execution stopped after {max_depth} steps.")  # [cite: 259]
        else:
            print(f"The depth of the tree is {depth} and the number of transitions taken was {number_transitions_taken}, excluding transitions to the reject state!")
            if accepted:
                print(f"String accepted in {depth} transitions")
                print(f"\nThe Path to {self.accept_state} Taken Was:")
                self.print_trace_path(accepted_final_state, tree, depth)

        print("\n\nThe Tree Was:")
        for l in tree:
            line = []
            for c in l:
                line = line + [c[:-1]]
            print(line)

    def print_trace_path(self, final_node, tree, depth):
        """
        Backtrack and print the path from root to the accepting node.
        Ref: Section 4.2 [cite: 165]
        """
        previous = final_node[3]

        if depth == 0:
            if len(final_node[0]):
                print(f"{final_node[0]}  {final_node[1]} {final_node[2]}")
            else:
                print(f"{final_node[1]} {final_node[2]}")

            return
        else:
            previous_state = tree[depth-1][previous[0]]
            transition_info = self.transitions[previous_state[1]][previous[1]]

            self.print_trace_path(previous_state, tree, depth-1)

            print(f"\nTransition take to state {final_node[1]}: {transition_info["read"][0]} -> {transition_info["write"][0]}, {transition_info["move"][0]}")
            if len(final_node[0]):
                print(f"{final_node[0]}  {final_node[1]} {final_node[2]}")
            else:
                print(f"{final_node[1]} {final_node[2]}")