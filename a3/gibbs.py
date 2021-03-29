# Compute the Gibb's sampling from given distributions
import argparse
import random

import matplotlib.pyplot as plt

PROBABILITIES = {
    'A': {0: {'B': { 0: 30, 1: 5},
              'D': { 0: 100, 1: 1}
             },
          1: {'B': { 0: 1, 1: 10},
              'D': { 0: 1, 1: 100}
             }
    },
    'B': {0: {'C': { 0: 100, 1: 1},
              'A': { 0: 30, 1: 1}
             },
          1: {'C': { 0: 1, 1: 100},
              'A': { 0: 30, 1: 10}
             }
    },
    'C': {0: {'D': { 0: 1, 1: 100},
              'B': { 0: 100, 1: 1}
             },
          1: {'D': { 0: 100, 1: 1},
              'B': { 0: 1, 1: 100}
             }
    },
    'D': {0: {'A': { 0: 100, 1: 1},
              'C': { 0: 1, 1: 100}
             },
          1: {'A': { 0: 1, 1: 100},
              'C': { 0: 100, 1: 1}
             }
    }
}
GRAPH = {
    'A': ['B', 'D'],
    'B': ['C', 'A'],
    'C': ['D', 'B'],
    'D': ['D', 'A']
}


def main():
    args = parse_args()
    assignments = {
        'A': random.randint(0,1),
        'B': 1,
        'C': random.randint(0,1),
        'D': random.randint(0,1)
    }
    sample_distributions = []
    for _ in range(0, args.samples):
        for var in ['A', 'C', 'D']:
            # calculate the true/false assignment probabilities
            assignments[var] = 0
            prob_false = calculate_probability(assignments, var)
            assignments[var] = 1
            prob_true = calculate_probability(assignments, var)
            # RNG to determine the random sample
            rng = random.uniform(0, 1)
            assignments[var] = 1 if rng < prob_true else 0
            if var == 'A':
                normalization_factor = prob_false + prob_true
                sample_distributions.append((
                    prob_true/normalization_factor,
                    prob_false/normalization_factor))
    # arbitrarily plot P(a_1|b_1)
    y_axis = [x[0] for x in sample_distributions]
    x_axis = list(range(1, args.samples + 1))
    plt.plot(x_axis, y_axis)
    plt.show()

def gibbs_random_sample(assignments):
    ''' Sample a random variable that is not our observed variable'''
    lst = ['A', 'C', 'D']
    var_to_sample = lst[random.randint(0,2)]
    assignments[var_to_sample] = random.randint(0, 1)
    return assignments

def calculate_probability(assignments, var):
    ''' Calculate sample probability using formula P(a|N(X))'''
    curr_prob = 1
    # compute the probability based on the MB of the node
    for neighbour in PROBABILITIES[var][assignments[var]]:
        curr_prob *= PROBABILITIES[var][assignments[var]][neighbour][assignments[neighbour]]
    return curr_prob

def parse_args():
    """Parse cmd line arguments. """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--samples",
        type=int,
        required=True,
        help="The number of samples to use in the Gibb's sampling"
        )
    return parser.parse_args()

if __name__ == '__main__':
    main()