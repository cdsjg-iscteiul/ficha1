import random
import time
import numpy as np
import seaborn as sea
import matplotlib.pyplot as plt
import aux_file


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


class SaveState:
    state = None
    number = None

    def __init__(self, numbers, states):
        self.number = numbers
        self.state = states

    def __hash__(self):
        return hash(self.state)

    def __eq__(self, other):
        return self.state == other.state


def make_board_and_place_robot(robot):
    board = np.arange(1, 101, dtype=SaveState)
    board_made = board.reshape(10, 10)

    robot_initial_state = board_made[robot.initial_x][robot.initial_y]
    robot.state = robot_initial_state

    return board_made


def master_movement(state, action):
    split = str(state)
    listas = [int(d) for d in str(split)]

    if state == 1:
        return aux_file.movement_corner_top_right(state, action)
    elif state == 10:
        return aux_file.movement_corner_top_left(state, action)
    elif state == 100:
        return aux_file.movement_corner_bot_left(state, action)
    elif state == 91:
        return aux_file.movement_corner_bot_right(state, action)
    elif len(listas) == 1:
        return aux_file.movement_with_up(state, action)
    elif listas[1] == 1:
        return aux_file.movement_with_right(state, action)
    elif listas[0] == 9:
        return aux_file.movement_with_down(state, action)
    elif listas[1] == 0:
        return aux_file.movement_with_left(state, action)
    else:
        return aux_file.movement_free(state, action)


def reward(state):
    if state == 100:
        return 100
    else:
        return 0



def evaluation(estado_velho, estado_novo):
    # V(s) = ( 1 - alpha) * V(s) + alpha * ( Reward(s) + discount * V(s')
    learning_rate = 0.01
    discount_rate = 0.99

    valor_reward_inicial = reward(estado_velho.number)

    value = (1 - learning_rate) * estado_velho.number + learning_rate * (
            valor_reward_inicial + discount_rate * estado_novo.number)

    print(value)

    valor = SaveState(value, estado_velho.number)

    return valor


def run_xk_random(value):
    robot = Robot(0, 0)
    make_board_and_place_robot(robot)
    times = 0

    for x in range(30):
        total_reward = 0
        mid_time = 0
        for t in range(value):
            start_time = time.process_time()
            action = aux_file.random_action()
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


def run_x_evaluation_20000(value):
    robot = Robot(0, 0)

    for x in range(30):
        total_reward = 0
        total_time = 0
        v_final = q_vector()
        for t in range(value):
            v = []
            moviment = aux_file.random_action()
            old_state = robot.state
            mid = v_final.__getitem__(robot.state - 1)
            avaliation_1 = evaluation(v_final.__getitem__(robot.state), mid)
            v.append(avaliation_1)
            robot.state = master_movement(old_state, moviment)
            robot.reward = reward(robot.state)
            avaliation_2 = evaluation(v_final.__getitem__(robot.state), mid)
            v.append(avaliation_2)
            v_final.append(remove_duplicates(v))
            if robot.reward == 100:
                robot.state = 1
            total_reward += robot.reward


def transform_and_heatmap(list_evaluation):
    sorted_list = sorted(list_evaluation, key=lambda x: x.state)

    lista123 = remove_duplicates(sorted_list)

    last_list = []
    for x in lista123:
        last_list.append(x.number)

    sea.heatmap(np.reshape(last_list, (10, 10)), annot=True)
    plt.show()


def remove_duplicates(list_11):
    last_list = []
    for x in list_11:
        if x not in last_list:
            last_list.append(x)

    last_list.append(SaveState(0, 100))
    return last_list


def q_table():
    columns = []
    grid = []
    # creates the matrix
    for x in range(1, 10):
        for y in range(1, 10):
            for t in range(1, 100):
                columns.append(SaveState(0, t))
            grid.append(columns.copy())
            columns = []


def q_vector():
    vector = []
    for t in range(1, 100):
        vector.append(SaveState(0, t))
    return vector


def test():
    robot = Robot(9, 0)
    make_board_and_place_robot(robot)

    v_final = q_vector()

    mid = v_final.__getitem__(robot.state - 1)

    print(mid.state)


run_x_evaluation_20000(20000)
