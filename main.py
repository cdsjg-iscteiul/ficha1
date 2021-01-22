import time
import numpy as np
import seaborn as sea
import matplotlib.pyplot as plt
import matplotlib.pylab as hmp
import aux_file

legend = 1


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
    learning_rate = 0.99
    discount_rate = 0.99

    valor_reward_inicial = reward(estado_velho.state)

    if estado_velho.state == 100 and estado_novo.state == 1:
        value_final = 0
        # print("ENTREI teste")
    else:
        value_pt1 = (1 - learning_rate)
        # print("PART1:    " + str(value_pt1))
        value_pt2 = (discount_rate * estado_novo.number)
        # print("PART2:    " + str(value_pt2))
        value_pt3 = (valor_reward_inicial + value_pt2)
        # print("PART3:    " + str(value_pt3))
        value_pt4 = value_pt1 * estado_velho.number
        # print("PART4:    " + str(value_pt4))
        value_pt5 = learning_rate * value_pt3
        # print("PART5:    " + str(value_pt5))
        value_final = value_pt4 + value_pt5
        # print("PART6:    " + str(value_final))

    valor = SaveState(value_final, estado_velho.state)

    # print(valor.number)

    return valor


def one_run(steps, robot):
    total_reward = 0
    nxt_state = robot.state

    for i in range(steps):
        nxt_state = master_movement(nxt_state, aux_file.random_action())
        robot.reward = reward(robot.state)
        total_reward += robot.reward
        if nxt_state == 100:
            nxt_state = 1

    average_reward = total_reward / steps

    return average_reward


def new_rand():
    robot = Robot(0, 0)
    make_board_and_place_robot(robot)
    times_deviation = []
    average_list_1_20k = []

    next_state = robot.state
    times_pos = [0] * 100
    times_pos[0] = robot.state
    for i in range(30):
        start_time = time.time()

        for x in range(20000):
            if x == 0:
                avg_1 = one_run(1000, robot)
                average_list_1_20k.append(avg_1)

            times_pos[next_state-1] += 1

            next_state = master_movement(next_state, aux_file.random_action())
            robot.reward = reward(next_state)

            if x == (20000 - 1):
                avg_20k = one_run(1000, robot)
                average_list_1_20k.append(avg_20k)

        times_deviation.append(time.time() - start_time)
    print(times_pos)
    draw_heatmap(times_pos)


def run_xk_random(value):
    robot = Robot(0, 0)
    make_board_and_place_robot(robot)
    times = 0
    times_deviation = []

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
        times_deviation.append([x, mid_time])
        average_reward = total_reward / value
        print("RUN: " + str(x + 1) + "  VALOR MÉDIO REWARD:  " + str(average_reward) + "   TEMPO:  " + str(mid_time))
    time_average = (times / value)
    print("DESVIO DE TEMPO:   " + str(np.std(times_deviation[1])))
    print("MEDIA DE TEMPO:   " + str(time_average))
    print("TEMPO:   " + str(times))
    ax = sea.boxplot(x=times_deviation[1])
    plt.show()


def run_x_evaluation_20000(value):
    v_final = q_vector()
    v = q_vector()
    for x in range(2):
        robot = Robot(0, 0)
        make_board_and_place_robot(robot)
        for t in range(value):
            moviment = aux_file.random_action()
            old_state = robot.state
            robot.state = master_movement(old_state, moviment)
            # print(moviment)
            # print("NEW STATE:  " + str(robot.state))
            robot.reward = reward(robot.state)
            if robot.state == 100:
                avaliation_2 = evaluation(next((x for x in v_final if x.state == old_state), None),
                                          next((x for x in v_final if x.state == 1), None))
            else:
                avaliation_2 = evaluation(next((x for x in v_final if x.state == old_state), None),
                                          next((x for x in v_final if x.state == robot.state), None))

            # avaliation_2 = evaluation(SaveState(100, 100), SaveState(100, 1))
            v.append(avaliation_2)

            if robot.reward == 100:
                robot.state = 1
        print("ANTES DO REMOVE DUPLICATES:" + str(len(v_final)))
        v_final = remove_duplicates(v)
        transform_and_heatmap(v_final)
        print("DEPOIS DO REMOVE DUPLICATES:" + str(len(v_final)))
        v.clear()
        # print("TESTE     " + str(v[3].number))


def draw_heatmap(vector):
    global legend
    tx = sea.heatmap(np.reshape(vector, (10, 10)), linewidth=0.5)
    tx.set_title('Figure ' + str(legend))
    legend += 1
    hmp.show()


def transform_and_heatmap(list_evaluation):
    sorted_list = sorted(list_evaluation, key=lambda shadow: shadow.state)

    # lista123 = remove_duplicates(sorted_list)

    last_list = []
    for x in sorted_list:
        last_list.append(x.number)
        print(x.state)

    sea.heatmap(np.reshape(last_list, (10, 10)))
    plt.show()


def remove_duplicates(list_11):
    last_list = []
    for x in list_11:
        if x not in last_list:
            last_list.append(x)

    return last_list


def q_table():
    columns = []
    grid = []
    # creates the matrix
    for x in range(1, 10):
        for y in range(1, 10):
            for t in range(1, 101):
                columns.append(SaveState(0, t))
            grid.append(columns.copy())
            columns = []


def q_vector():
    vector = []
    for t in range(1, 101):
        vector.append(SaveState(0.12, t))
    return vector


new_rand()
