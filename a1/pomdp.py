import argparse

WIDTH = 4
HEIGHT = 3


def main():
    args = parse_args()
    b_s = [[0.111, 0.111, 0.111, 0],
           [0.111, -1, 0.111, 0],
           [0.111, 0.111, 0.111, 0]]
    if args.start:
        belief_state_start_given(b_s, args.start)
    for idx, action in enumerate(args.actions):
        calc_new_belief_state(b_s, action, args.observations[idx])

def belief_state_start_given(b_s, start):
    for i in range(0, HEIGHT):
        for j in range(0, WIDTH):
            if b_s[i][j] != -1:
                b_s[i][j] = 0
    start_idx = start.split(',')
    b_s[start_idx[0]][start_idx[1]] = 1

def calc_new_belief_state(b_s, action, obs):
    pass

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