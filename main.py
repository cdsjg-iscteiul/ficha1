import random
from enum import Enum
import time
import numpy as np


class Actions(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Robot:
    def __init__(self, initial_x, initial_y):
        self.initial_x = initial_x
        self.initial_y = initial_y
        self._state = 0
        self._reward = 0
        self._current_x = initial_x
        self._current_y = initial_y

    @property
    def reward(self):
        return self._reward

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @reward.setter
    def reward(self, value):
        self._reward = value

    @property
    def current_x(self):
        return self._current_x

    @current_x.setter
    def current_x(self, value):
        self._current_x = value

    @property
    def current_y(self):
        return self._current_y

    @current_y.setter
    def current_y(self, value):
        self._current_y = value


def make_board_and_place_robot(robot):
    board = np.arange(1, 101, dtype=int)

    board_made = board.reshape(10, 10)

    robot_initial_state = board_made[robot.initial_x][robot.initial_y]
    robot.state = robot_initial_state

    return board_made


def movement_free(state, action):
    switcher = {
        Actions.UP: state - 10,
        Actions.DOWN: state + 10,
        Actions.RIGHT: state - 1,
        Actions.LEFT: state + 1
    }
    return switcher.get(action, "Invalid")


def movement_with_up(state, action):
    switcher = {
        Actions.UP: state,
        Actions.DOWN: state + 10,
        Actions.RIGHT: state - 1,
        Actions.LEFT: state + 1
    }
    return switcher.get(action, "Invalid")


def movement_with_left(state, action):
    switcher = {
        Actions.UP: state - 10,
        Actions.DOWN: state + 10,
        Actions.RIGHT: state - 1,
        Actions.LEFT: state
    }
    return switcher.get(action, "Invalid")


def movement_with_down(state, action):
    switcher = {
        Actions.UP: state - 10,
        Actions.DOWN: state,
        Actions.RIGHT: state - 1,
        Actions.LEFT: state + 1
    }
    return switcher.get(action, "Invalid")


def movement_with_right(state, action):
    switcher = {
        Actions.UP: state - 10,
        Actions.DOWN: state + 10,
        Actions.RIGHT: state,
        Actions.LEFT: state + 1
    }
    return switcher.get(action, "Invalid")


def movement_corner_top_right(state, action):
    switcher = {
        Actions.UP: state,
        Actions.DOWN: state + 10,
        Actions.RIGHT: state,
        Actions.LEFT: state + 1
    }
    return switcher.get(action, "Invalid")


def movement_corner_top_left(state, action):
    switcher = {
        Actions.UP: state,
        Actions.DOWN: state + 10,
        Actions.RIGHT: state - 1,
        Actions.LEFT: state
    }
    return switcher.get(action, "Invalid")


def movement_corner_bot_right(state, action):
    switcher = {
        Actions.UP: state - 10,
        Actions.DOWN: state,
        Actions.RIGHT: state,
        Actions.LEFT: state + 1
    }
    return switcher.get(action, "Invalid")


def movement_corner_bot_left(state, action):
    switcher = {
        Actions.UP: state - 10,
        Actions.DOWN: state,
        Actions.RIGHT: state,
        Actions.LEFT: state
    }
    return switcher.get(action, "Invalid")


def master_movement(state, action):
    split = str(state)
    listas = [int(d) for d in str(split)]

    if state == 1:
        return movement_corner_top_right(state, action)
    elif state == 10:
        return movement_corner_top_left(state, action)
    elif state == 100:
        return movement_corner_bot_left(state, action)
    elif state == 91:
        return movement_corner_bot_right(state, action)
    elif len(listas) == 1:
        return movement_with_up(state, action)
    elif listas[1] == 1:
        return movement_with_right(state, action)
    elif listas[0] == 9:
        return movement_with_down(state, action)
    elif listas[1] == 0:
        return movement_with_left(state, action)
    else:
        return movement_free(state, action)


def reward(state):
    if state == 100:
        return 100
    else:
        return 0


def random_action():
    return random.choice(list(Actions))


def run_xk_random(value):
    robot = Robot(0, 0)
    make_board_and_place_robot(robot)
    times = 0

    for x in range(30):
        total_reward = 0
        mid_time = 0
        for t in range(value):
            start_time = time.process_time()
            action = random_action()
            robot.state = master_movement(robot.state, action)
            robot.reward = reward(robot.state)
            if robot.reward == 100:
                robot.state = 1
            total_reward += robot.reward
            end_time = time.process_time()
            process_time = (end_time - start_time)
            mid_time += process_time
        times += mid_time
        average_reward = total_reward / value
        print("REWARD: " + str(x + 1) + "  VALOR MÉDIO REWARD:  " + str(average_reward) + "   TEMPO:  " + str(mid_time))
    time_average = (times / value)
    print("MEDIA DE TEMPO:   " + str(time_average))


def time1k():
    run_xk_random(200000)


time1k()
