import argparse
from pprint import pprint

WIDTH = 4
HEIGHT = 3
OBS_TO_GRID = {
    '1': [0.9, 0.1, 0],
    '2': [0.1, 0.9, 0],
    'end': [0, 0, 1]
}


def main():
    args = parse_args()
    b_s = [[0.111, 0.111, 0.111, 0],
           [0.111, 0, 0.111, 0],
           [0.111, 0.111, 0.111, 0.111]]
    if args.start:
        b_s = belief_state_start_given(args.start)
    for idx, action in enumerate(args.actions):
        b_s = calc_new_belief_state(b_s, action, args.observations[idx])
    _round_final_result(b_s)
    pprint(b_s)

def _round_final_result(b_s):
    for i in range(0, HEIGHT):
        for j in range(0, WIDTH):
            b_s[i][j] = round(b_s[i][j], 4)

def belief_state_start_given(start):
    b_s = [[0 for l in range(WIDTH)] for k in range(HEIGHT)] # instantiate empty bs
    start_idx = start.split(',')
    b_s[int(start_idx[0])][int(start_idx[1])] = 1
    return b_s

def calc_new_belief_state(b_s, action, obs):
    updated_b_s = [[0 for l in range(WIDTH)] for k in range(HEIGHT)] # instantiate empty bs
    cum_sum = 0
    for i in range(0, HEIGHT):
        for j in range(0, WIDTH):
            if _is_dead_square(i, j):
                continue
            updated_b_s[i][j] = _calc_new_belief_state(b_s, action, obs, i, j)
            cum_sum += updated_b_s[i][j]
    _normalize_b_s(updated_b_s, cum_sum)
    return updated_b_s

def _normalize_b_s(belief_state, cumulative_sum):
    for row in range(0, HEIGHT):
        for col in range(0, WIDTH):
            if _is_dead_square(row, col):
                continue
            belief_state[row][col] /= cumulative_sum

def _calc_new_belief_state(b_s, action, obs, row, col):
    if col == 2:
        prob_given_obs = OBS_TO_GRID[obs][0] # non-terminal 3rd col
    elif col == 3 and row != 2:
        prob_given_obs = OBS_TO_GRID[obs][2] # terminal 3rd col
    else:
        prob_given_obs = OBS_TO_GRID[obs][1] # all other non-terminal
    cumulative_val = _calc_belief_state_sum(b_s, action, row, col)

    # multiply the cumulative probabilities by the prob given by the observation
    return cumulative_val * prob_given_obs

def _calc_belief_state_sum(b_s, action, row, col):
    # 0.8 chance of moving in intended direction, 0.1 of moving at either 90 degree angle
    squares = []
    squares_dict = {}
    if action == 'right':
        # initial starting state is same square
        if _bounced(row, col, 'right'): # bounces in the direction it's trying to go
            squares.append((row, col, 0.8))
        if _bounced(row, col, 'down'): # bounces in the incorrect direction
            squares.append((row, col, 0.1))
        if _bounced(row, col, 'up'): # bounces in the incorrect direction
            squares.append((row, col, 0.1))

        # initial starting square is to the left
        if not _is_out_of_bounds(row, col-1) and not _is_dead_square(row, col-1):
            squares.append((row, col-1, 0.8))
        # initial starting square is above
        if not _is_out_of_bounds(row-1, col) and not _is_dead_square(row-1, col):
            squares.append((row-1, col, 0.1))
        # initial starting square is below
        if not _is_out_of_bounds(row + 1, col) and not _is_dead_square(row+1, col):
            squares.append((row+1, col, 0.1))

        # sum any same squares
        squares_dict = _conglomerate_same_squares(squares)

    elif action == 'left':
        # initial starting state is same square
        if _bounced(row, col, 'left'): # bounces in the direction it's trying to go
            squares.append((row, col, 0.8))
        if _bounced(row, col, 'down'): # bounces in the incorrect direction
            squares.append((row, col, 0.1))
        if _bounced(row, col, 'up'): # bounces in the incorrect direction
            squares.append((row, col, 0.1))

        # initial starting square is to the right
        if not _is_out_of_bounds(row, col + 1) and not _is_dead_square(row, col+1):
            squares.append((row, col+1, 0.8))
        # initial starting square is above
        if not _is_out_of_bounds(row - 1, col) and not _is_dead_square(row-1, col):
            squares.append((row-1, col, 0.1))
        # initial starting square is below
        if not _is_out_of_bounds(row + 1, col) and not _is_dead_square(row+1, col):
            squares.append((row+1, col, 0.1))

        # sum any same squares
        squares_dict = _conglomerate_same_squares(squares)

    elif action == 'up':
        # initial starting state is same square
        if _bounced(row, col, 'up'): # bounces in the direction it's trying to go
            squares.append((row, col, 0.8))
        if _bounced(row, col, 'left'): # bounces in the incorrect direction
            squares.append((row, col, 0.1))
        if _bounced(row, col, 'right'): # bounces in the incorrect direction
            squares.append((row, col, 0.1))

        # initial starting square is below
        if not _is_out_of_bounds(row + 1, col) and not _is_dead_square(row + 1, col):
            squares.append((row+1, col, 0.8))
        # initial starting square is to the right
        if not _is_out_of_bounds(row, col+1) and not _is_dead_square(row, col+1):
            squares.append((row, col+1, 0.1))
        # initial starting square is to the left
        if not _is_out_of_bounds(row, col-1) and not _is_dead_square(row, col-1):
            squares.append((row, col-1, 0.1))

        # sum any same squares
        squares_dict = _conglomerate_same_squares(squares)

    elif action == 'down':
        # initial starting state is same square
        if _bounced(row, col, 'down'): # bounces in the direction it's trying to go
            squares.append((row, col, 0.8))
        if _bounced(row, col, 'left'): # bounces in the incorrect direction
            squares.append((row, col, 0.1))
        if _bounced(row, col, 'right'): # bounces in the incorrect direction
            squares.append((row, col, 0.1))

        # initial starting square is above
        if not _is_out_of_bounds(row - 1, col) and not _is_dead_square(row - 1, col):
            squares.append((row - 1, col, 0.8))
        # initial starting square is to the right
        if not _is_out_of_bounds(row, col+1) and not _is_dead_square(row, col+1):
            squares.append((row, col+1, 0.1))
        # initial starting square is to the left
        if not _is_out_of_bounds(row, col-1) and not _is_dead_square(row, col-1):
            squares.append((row, col-1, 0.1))

        # sum any same squares
        squares_dict = _conglomerate_same_squares(squares)

    vals = []
    for sq, prob in squares_dict.items():
        vals.append(prob*b_s[sq[0]][sq[1]])
    if _is_absorbing_square(row, col): # probability for absorbing state should only go up
        return b_s[row][col] + sum(vals)
    return sum(vals)

def _conglomerate_same_squares(squares):
    ret = {}
    for square in squares:
        if (square[0], square[1]) not in ret:
            ret[(square[0], square[1])] = square[2]
        else:
            ret[(square[0], square[1])] += square[2]
    return ret

def _bounced(row, col, action):
    return _bounces_off_wall(row, col, action)

def _is_out_of_bounds(row, col):
    return (row < 0 or row >= HEIGHT) or (col < 0 or col >= WIDTH) or (_is_absorbing_square(row, col))

def _is_absorbing_square(row, col):
    return (row == 0 and col == 3) or (row == 1 and col == 3)

def _bounces_off_wall(row, col, action):
    if action == 'up':
        if row - 1 < 0 or _is_dead_square(row-1, col):
            return True
    elif action == 'left':
        if col - 1 < 0 or _is_dead_square(row, col-1):
            return True
    elif action == 'down':
        if row + 1 >= HEIGHT or _is_dead_square(row+1, col):
            return True
    elif action == 'right':
        if col + 1 >= WIDTH or _is_dead_square(row, col+1):
            return True
    return False

def _is_dead_square(row, col):
    return row == 1 and col == 1

def parse_args():
    """Parse cmd line arguments. """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--start",
        type=str,
        default="",
        required=False,
        help="The start square of the agent, in the form row,col. If not specified, this is randomized"
        )
    parser.add_argument(
        "--actions",
        type=str,
        required=True,
        nargs = '+',
        help="The actions the agent takes, comma delimited"
        )
    parser.add_argument(
        "--observations",
        type=str,
        required=True,
        nargs = '+',
        help="The observations the agent makes, comma delimited"
        )
    return parser.parse_args()

if __name__ == '__main__':
    main()
