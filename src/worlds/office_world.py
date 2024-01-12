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


    def execute_action(self, a):
        """
        We execute 'action' in the game
        """
        x,y = self.agent[:2]
        ssw1, ssw2 = self.agent[2:]
        temp = list(self.agent)
        # temp[2:] = ss1, ss2
        # print('temp in execute action:', temp)
        # print('temp in execute action:', temp)
        # exit()
        # self.agent = tuple(temp)

        # executing action
        self.agent = self.xy_MDP_slip(a,1, ssw1, ssw2) # progresses in x-y system
        print('agent is:',self.agent)
        # exit()
        # x,y = self.agent[:2]
        # temp = list(self.agent)
        # temp[2:] = ss1, ss2, ss3, ss4, cc1, cc2, cc3, cc4
        # print('temp in execute action:', temp)
        # # print('temp in execute action:', temp)
        # # exit()
        # self.agent = tuple(temp)
    
    def get_actions(self):
        """
        Returns a list of all possible actions the agent can perform.
        """
        return self.actions

    def xy_MDP_slip(self,a,p, ssw1, ssw2):
        x,y = self.agent[:2]
        shape, color = self.agent[2:4]
        slip_p = [p,(1-p)/2,(1-p)/2]
        check = 0.5

        # up    = 0
        # right = 1 
        # down  = 2 
        # left  = 3 

        if (check<=slip_p[0]):
            a_ = a
            print('action:', a)

        elif (check>slip_p[0]) & (check<=(slip_p[0]+slip_p[1])):
            if a == 0: 
                a_ = 3
            elif a == 2: 
                a_ = 1
            elif a == 3: 
                a_ = 2
            elif a == 1: 
                a_ = 0

        else:
            if a == 0: 
                a_ = 1
            elif a == 2: 
                a_ = 3
            elif a == 3: 
                a_ = 0
            elif a == 1: 
                a_ = 2

        # ssw1 = 0
        # ssw2 = 0
        action_ = Actions(a_)
        if (x,y,shape, color, action_) not in self.forbidden_transitions:
            if action_ == Actions.up:
                y+=1
            if action_ == Actions.down:
                y-=1
            if action_ == Actions.left:
                x-=1
            if action_ == Actions.right:
                x+=1
            if action_ == Actions.change_color_up:
                # if ssw2 > 15:
                #     ssw2 = 15
                # elif ssw2<0:
                #     ssw2 = 0
                # else:
                ssw2 +=1
            if action_ == Actions.change_color_down:
                # if ssw2 > 15:
                #     ssw2 = 15
                # elif ssw2<0:
                #     ssw2 = 0
                # else:
                ssw2 -=1
            if action_ == Actions.change_shape_up:
                # if ssw1 > 15:
                #     ssw1 = 15
                # elif ssw1<0:
                #     ssw1 = 0
                # else:
                ssw1 +=1
            if action_ == Actions.change_shape_down:
                # if ssw1 > 15:
                #     ssw1 = 15
                # elif ssw1<0:
                #     ssw1 = 0
                # else:
                ssw1 -=1  
                

        self.a_ = a_
        return (x,y, ssw1,ssw2)

    def get_state(self):
        return None # we are only using "simple reward machines" for the craft domain
        


    def get_last_action(self):
        """
        Returns agent's last action
        """
        return self.a_







    def get_features(self):
        x, y = self.agent[:2]
        print('x:', x, 'y', y)
        print('agent dim is', self.agent[:2])
        N, M = self.grid_size_x, self.grid_size_y  
        ret = np.zeros((N, M, 2, 2
                        ), dtype=np.float64)
        # print(x,y)
        print('ret dim:', ret.shape)
        ret[x, y,0,0] = 1
        # exit()[[[[
        # print(ret)
        # print('ret', ret.ravel())
        return ret.ravel()  # Flatten from 2D to 1D



    
    def get_true_propositions(self):
            """
            Returns the string with the propositions that are True in this state
            """
            ret = ""
            if self.agent in self.objects:
                ret += self.objects[self.agent]
            return ret


    def _load_map(self):
        self.objects = {}
        self.grid_size_x, self.grid_size_y = 6, 6
        self.agent = (1,1,0,0)
        self.objects[(1,2, 2,2)] = 'c'
        self.objects[(2,2, 3,2)] = 'b'
        self.objects[(3,2, 1,2)] = 'f'
        self.objects[(3,3, 3,3)] = 'g'

        self.forbidden_transitions = set()

        # self.objects = {
        #     "a": {"id": 1, "position": (2, 3), "shape": "diamond", "color": "green"},
        #     "b": {"id": 2, "position": (3, 2), "shape": "circle", "color": "green"},
        #     "c": {"id": 3, "position": (2, 2), "shape": "square", "color": "black"},
        #     "d": {"id": 4, "position": (5, 1), "shape": "diamond", "color": "brown"}
        # }
        self._add_external_walls()

    def _add_external_walls(self):
        
        print('grid size x', self.grid_size_x)
        print('grid size y', self.grid_size_y)
        # exit()
        self.actions = [Actions.up.value,Actions.right.value,Actions.down.value,Actions.left.value,
                         Actions.change_color_up.value, Actions.change_color_down.value,
                           Actions.change_shape_up.value, Actions.change_shape_down.value]

        for x in range(self.grid_size_x):
            for shape in range(16):
                for color in range(16):
                    self.forbidden_transitions.add((x, 0, shape, color, Actions.down))
                    self.forbidden_transitions.add((x, self.grid_size_y-1, shape, color , Actions.up))
        for y in range(self.grid_size_y):
            for shape in range(16):
                for color in range(16):
                    self.forbidden_transitions.add((0, y, shape, color, Actions.left))
                    self.forbidden_transitions.add((self.grid_size_x-1, y, shape, color, Actions.right))

        # for color in range(16):
        for shape in range(16):
            for color in range(16):
                for x in range(self.grid_size_x):
                    for y in range(self.grid_size_y):

                        self.forbidden_transitions.add((x, y, shape, 15, Actions.change_color_up))
                        self.forbidden_transitions.add((x, y, shape, 0, Actions.change_color_down))
                        self.forbidden_transitions.add((x, y, 15, color, Actions.change_shape_up))
                        self.forbidden_transitions.add((x, y, 0, color, Actions.change_shape_down))

        # for x in range(self.grid_size_x):
        #     for shape, color in zip(range(16), range(16)):
        #         self.forbidden_transitions.add((x, 0, shape, color, Actions.down))
        #         self.forbidden_transitions.add((x, self.grid_size_y-1, shape, color , Actions.up))
        # for y in range(self.grid_size_y):
        #     for shape, color in zip(range(16), range(16)):
        #         self.forbidden_transitions.add((0, y, shape, color, Actions.left))
        #         self.forbidden_transitions.add((self.grid_size_x-1, y, shape, color, Actions.right))

        # # for color in range(16):
        # for shape, color in zip(range(16), range(16)):
        #     for x, y in zip(range(self.grid_size_x), range(self.grid_size_y)):
        #         self.forbidden_transitions.add((x, y, shape, 15, Actions.change_color_up))
        #         self.forbidden_transitions.add((x, y, shape, 0, Actions.change_color_down))
        #         self.forbidden_transitions.add((x, y, 15, color, Actions.change_shape_up))
        #         self.forbidden_transitions.add((x, y, 0, color, Actions.change_shape_down))

                # self.forbidden_transitions.add((0, 0, Actions.change_color_down))
                # self.forbidden_transitions.add((15, 15, Actions.change_shape_up))
                # self.forbidden_transitions.add((0, 0, Actions.change_shape_down))
        
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
                    if (x // 2, y) == self.agent[:2]:
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
