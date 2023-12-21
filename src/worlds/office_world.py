if __name__ == '__main__':
    # This is a terrible hack just to be able to execute this file directly
    import sys
    sys.path.insert(0, '../')

import random
import numpy as np
from worlds.game_objects import Actions
import logging

logging.basicConfig(level=logging.INFO)

class OfficeWorldParams:
    def __init__(self):
        pass

class OfficeWorld:
    def __init__(self, params):
        self._load_map()
        self.env_game_over = False
        self.last_action = None
        self.objects = {
            1: {"position": (1, 1), "shape": "circle", "color": "red", "color_changed": False, "shape_changed": False},
            2: {"position": (2, 2), "shape": "circle", "color": "red", "color_changed": False, "shape_changed": False},
            3: {"position": (3, 3), "shape": "circle", "color": "red", "color_changed": False, "shape_changed": False},
            4: {"position": (4, 4), "shape": "circle", "color": "red", "color_changed": False, "shape_changed": False},
        }

    def execute_action(self, a):
        self.last_action = a 
        if a in [Actions.up.value, Actions.right.value, Actions.down.value, Actions.left.value]:
            self.move_agent(a)
            # print("move")
        elif a in [Actions.change_color.value, Actions.change_shape.value]:
            self.handle_advanced_action(a)
            # print("change")
    
    def get_actions(self):
        """
        Returns a list of all possible actions the agent can perform.
        """
        return self.actions

    def move_agent(self, action):
        x, y = self.agent
        dx, dy = [(0, -1), (1, 0), (0, 1), (-1, 0)][action]
        new_x, new_y = x + dx, y + dy
        if (0 <= new_x < self.grid_size_x) and (0 <= new_y < self.grid_size_y):
            self.agent = (new_x, new_y)

    def get_state(self):
        return None

    def handle_advanced_action(self, a):
        # print("action:", a)
        if a == Actions.change_color.value:
            self.change_object_color()
        elif a == Actions.change_shape.value:
            self.change_object_shape()

    def get_last_action(self):
        return self.last_action

    def change_object_color(self):
        color_order = ['red', 'blue', 'green', 'yellow']
        agent_pos = self.agent
        for obj_id, obj_info in self.objects.items():
            if agent_pos == obj_info['position']:
                # Randomly choose a color different from the current one
                new_color = random.choice([c for c in color_order if c != obj_info['color']])
                obj_info['color'] = new_color
                obj_info['color_changed'] = True
                break

    def change_object_shape(self):
        shape_order = ['circle', 'square', 'triangle', 'hexagon']
        agent_pos = self.agent
        for obj_id, obj_info in self.objects.items():
            if agent_pos == obj_info['position']:
                # Randomly choose a shape different from the current one
                new_shape = random.choice([s for s in shape_order if s != obj_info['shape']])
                obj_info['shape'] = new_shape
                obj_info['shape_changed'] = True
                break

    def get_features(self):
        x, y = self.agent
        N, M = self.grid_size_x, self.grid_size_y  # Assuming these are defined in your environment
        ret = np.zeros((N, M), dtype=np.float64)
        ret[x, y] = 1
        return ret.ravel()  # Flatten from 2D to 1D



    
    def get_true_propositions(self):
        object_to_letter = {
            (1, 'red', 'circle'): 'q', (1, 'red', 'square'): 'r', (1, 'red', 'triangle'): 's', (1, 'red', 'hexagon'): 't',
            (2, 'blue', 'circle'): 'e', (2, 'blue', 'square'): 'f', (2, 'blue', 'triangle'): 'g', (2, 'blue', 'hexagon'): 'h',
            (3, 'green', 'circle'): 'i', (3, 'green', 'square'): 'j', (3, 'green', 'triangle'): 'k', (3, 'green', 'hexagon'): 'l',
            (4, 'yellow', 'circle'): 'm', (4, 'yellow', 'square'): 'n', (4, 'yellow', 'triangle'): 'o', (4, 'yellow', 'hexagon'): 'p'
        }

        propositions = []
        for obj_id, obj_info in self.objects.items():
            obj_color = obj_info['color']
            obj_shape = obj_info['shape']
            if obj_info['color_changed'] or obj_info['shape_changed']:
                label = object_to_letter.get((obj_id, obj_color, obj_shape), f"unknown_{obj_id}")
                propositions.append(label)

        return ', '.join(propositions) if propositions else ""



    



    def _load_map(self):
        self.grid_size_x, self.grid_size_y = 6, 6
        self.agent = (2, 1)
        self.objects = {
            "a": {"id": 1, "position": (1, 1), "shape": "circle", "color": "red"},
            "b": {"id": 2, "position": (2, 2), "shape": "circle", "color": "red"},
            "c": {"id": 3, "position": (3, 3), "shape": "circle", "color": "red"},
            "d": {"id": 4, "position": (4, 4), "shape": "circle", "color": "red"}
        }
        self._add_external_walls()

    def _add_external_walls(self):
        self.forbidden_transitions = set()
        for x in range(self.grid_size_x):
            self.forbidden_transitions.add((x, 0, Actions.up.value))
            self.forbidden_transitions.add((x, self.grid_size_y - 1, Actions.down.value))
        for y in range(self.grid_size_y):
            self.forbidden_transitions.add((0, y, Actions.left.value))
            self.forbidden_transitions.add((self.grid_size_x - 1, y, Actions.right.value))

        self.actions = [Actions.up.value,Actions.right.value,Actions.down.value,Actions.left.value, Actions.change_color.value, Actions.change_shape.value]

        
    def show(self):
        for y in range(self.grid_size_y - 1, -1, -1):
            # Horizontal walls (top)
            for x in range(self.grid_size_x * 2):
                print("_" if (x // 2, y, Actions.up.value) in self.forbidden_transitions else " ", end="")
            print()

            # Vertical walls and objects
            for x in range(self.grid_size_x * 2):
                print("|" if (x // 2, y, Actions.left.value) in self.forbidden_transitions else " ", end="")

                if x % 2 == 0:  # Object or Agent position
                    if (x // 2, y) == self.agent:
                        print("A", end="")
                    else:
                        object_at_pos = [(obj_key, obj_info) for obj_key, obj_info in self.objects.items() if obj_info['position'] == (x // 2, y)]
                        if object_at_pos:
                            obj_id, _ = object_at_pos[0]
                            print(obj_id, end="")  # Use object's key as its ID
                        else:
                            print(" ", end="")
                else:
                    print(" ", end="")

                print("|" if (x // 2, y, Actions.right.value) in self.forbidden_transitions else " ", end="")
            print()

            # Horizontal walls (bottom)
            if y == 0:
                for x in range(self.grid_size_x * 2):
                    print("_" if (x // 2, y, Actions.down.value) in self.forbidden_transitions else " ", end="")
                print()


      
def play():
    from reward_machines.reward_machine import RewardMachine

    # Initialize actions and parameters
    str_to_action = {"up": Actions.up.value, "right": Actions.right.value, 
                     "down": Actions.down.value, "left": Actions.left.value, 
                     "change_color": Actions.change_color.value, 
                     "change_shape": Actions.change_shape.value}
    params = OfficeWorldParams()

    # Define tasks and reward machines
    tasks = ["../../experiments/office/reward_machines/t%d.txt"%i for i in [1]]
    reward_machines = [RewardMachine(t) for t in tasks]

    # Play the game for each task
    for i, rm in enumerate(reward_machines):
        print(f"Running task: {tasks[i]}")

        game = OfficeWorld(params)
        s1 = game.get_state()
        u1 = rm.get_initial_state()

        while True:
            # Show game state and handle action input
            game.show()
            print("Events:", game.get_true_propositions())
            action = input("Enter action: ").strip().lower()

            if action in str_to_action:
                game.execute_action(str_to_action[action])

                # Update state and reward
                s2 = game.get_state()
                events = game.get_true_propositions()
                u2 = rm.get_next_state(u1, events)
                r = rm.get_reward(u1, u2, s1, str_to_action[action], s2)

                print("---------------------")
                print("Reward:", r)
                print("---------------------")

                if game.env_game_over or rm.is_terminal_state(u2):
                    break

                s1 = s2
                u1 = u2
            else:
                print("Invalid action")

        game.show()
        print("Events:", game.get_true_propositions())
        print("Game Over for this task.")

    print("All tasks completed. Thank you for playing!")


if __name__ == '__main__':
    play()
