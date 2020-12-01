from main import Actions


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


def check_possible_actions(state):
    split = str(state)
    listas = [int(d) for d in str(split)]
    if state == 1:
        return [Actions.DOWN, Actions.RIGHT]
    elif state == 10:
        return [Actions.DOWN, Actions.LEFT]
    elif state == 100:
        return [Actions.UP, Actions.LEFT]
    elif state == 91:
        return [Actions.UP, Actions.RIGHT]
    elif len(listas) == 1:
        return [Actions.DOWN, Actions.LEFT, Actions.RIGHT]
    elif listas[1] == 1:
        return [Actions.UP, Actions.DOWN, Actions.LEFT]
    elif listas[0] == 9:
        return [Actions.UP, Actions.UP, Actions.LEFT]
    elif listas[1] == 0:
        return [Actions.UP, Actions.DOWN, Actions.RIGHT]
    else:
        return [Actions.UP, Actions.DOWN, Actions.LEFT, Actions.RIGHT]
