import random
import numpy as np
from worlds.game_objects import Actions, AdvancedActions
import logging

logging.basicConfig(level=logging.INFO)

class ChemicalWorldParams:
    def __init__(self):
        pass

class ChemicalWorld:
    def __init__(self, params):
        self._load_map()
        self.env_game_over = False
        self.last_action = None

    def execute_action(self, a):
        self.last_action = a 
        if a in [Actions.up.value, Actions.right.value, Actions.down.value, Actions.left.value]:
            self.move_agent(a)
        elif a in [AdvancedActions.change_color.value, AdvancedActions.change_shape.value]:
            self.handle_advanced_action(a)
    
    def get_actions(self):
        """
        Returns a list of all possible actions the agent can perform.
        """
        return [
            Actions.up.value, 
            Actions.right.value, 
            Actions.down.value, 
            Actions.left.value, 
            AdvancedActions.change_color.value, 
            AdvancedActions.change_shape.value
        ]

    def move_agent(self, action):
        x, y = self.agent
        dx, dy = [(0, -1), (1, 0), (0, 1), (-1, 0)][action]
        new_x, new_y = x + dx, y + dy
        if (0 <= new_x < self.grid_size_x) and (0 <= new_y < self.grid_size_y):
            self.agent = (new_x, new_y)

    def get_state(self):
        # Implement as needed
        return None

    def handle_advanced_action(self, a):
        if a == AdvancedActions.change_color.value:
            self.change_object_color()
        elif a == AdvancedActions.change_shape.value:
            self.change_object_shape()

    def get_last_action(self):
        return self.last_action

    def change_object_color(self):
        color_order = ['red', 'blue', 'green', 'yellow']
        agent_pos = (self.agent[0], self.agent[1])
        for obj_key, obj_info in self.objects.items():
            if agent_pos == obj_info['position']:
                current_color = obj_info['color']
                new_color_index = (color_order.index(current_color) + 1) % len(color_order)
                obj_info['color'] = color_order[new_color_index]
                break

    def change_object_shape(self):
        shape_order = ['circle', 'square', 'triangle', 'hexagon']
        agent_pos = (self.agent[0], self.agent[1])
        for obj_key, obj_info in self.objects.items():
            if agent_pos == obj_info['position']:
                current_shape = obj_info['shape']
                new_shape_index = (shape_order.index(current_shape) + 1) % len(shape_order)
                obj_info['shape'] = shape_order[new_shape_index]
                break

    def get_features(self):
        x, y = self.agent
        N, M = self.grid_size_x, self.grid_size_y
        ret = np.zeros((N, M, 3), dtype=np.float64)
        ret[x, y, 0] = 1
        color_shape_to_index = {
            ('red', 'circle'): 1, ('red', 'square'): 2, ('red', 'triangle'): 3, ('red', 'hexagon'): 4,
            ('blue', 'circle'): 5, ('blue', 'square'): 6, ('blue', 'triangle'): 7, ('blue', 'hexagon'): 8,
            ('green', 'circle'): 9, ('green', 'square'): 10, ('green', 'triangle'): 11, ('green', 'hexagon'): 12,
            ('yellow', 'circle'): 13, ('yellow', 'square'): 14, ('yellow', 'triangle'): 15, ('yellow', 'hexagon'): 16
        }
        for obj_info in self.objects.values():
            obj_x, obj_y = obj_info['position']
            color_shape_index = color_shape_to_index[(obj_info['color'], obj_info['shape'])]
            ret[obj_x, obj_y, 1] = color_shape_index
        return ret.ravel()
    
    def get_true_propositions(self):
        object_to_letter = {
            (1, 'red', 'circle'): 'a', (1, 'red', 'square'): 'b', (1, 'red', 'triangle'): 'c', (1, 'red', 'hexagon'): 'd',
            (2, 'blue', 'circle'): 'e', (2, 'blue', 'square'): 'f', (2, 'blue', 'triangle'): 'g', (2, 'blue', 'hexagon'): 'h',
            (3, 'green', 'circle'): 'i', (3, 'green', 'square'): 'j', (3, 'green', 'triangle'): 'k', (3, 'green', 'hexagon'): 'l',
            (4, 'yellow', 'circle'): 'm', (4, 'yellow', 'square'): 'n', (4, 'yellow', 'triangle'): 'o', (4, 'yellow', 'hexagon'): 'p'
        }

        ret = ""
        agent_pos = self.agent
        for obj_id, obj_info in self.objects.items():
            if agent_pos == obj_info['position']:
                object_key = (obj_info['id'], obj_info['color'], obj_info['shape'])
                letter_representation = object_to_letter.get(object_key, "")
                if letter_representation:
                    ret += letter_representation + " "
        return ret.strip()

    def _load_map(self):
        self.grid_size_x, self.grid_size_y = 6, 6
        self.agent = (2, 1)
        self.objects = {
            "a": {"id": 1, "position": (1, 1), "shape": "circle", "color": "red"},
            "b": {"id": 2, "position": (2, 2), "shape": "square", "color": "blue"},
            "c": {"id": 3, "position": (3, 3), "shape": "triangle", "color": "green"},
            "d": {"id": 4, "position": (4, 4), "shape": "hexagon", "color": "yellow"}
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
