'''
This code provides the plotting functions for testing the obtained policy.
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import directed_hausdorff
from scipy import stats
from scipy.stats import wasserstein_distance


def plot_replicated_action_prob(q_values, state_indices, test_folder, label):
    plt.figure(figsize=(10, 3))
    plt.imshow(q_values[state_indices].T, cmap="plasma", aspect='auto')
    plt.title("Policy "+ label +" : Action Probabilities along the Trajectory", fontsize=22)
    plt.tick_params(axis='x', which='major', labelsize=18)
    plt.tick_params(axis='y', which='minor', labelsize=18)
    plt.xlabel("Trajectory Step Index", fontsize=20)
    plt.ylabel("Action Index", fontsize=20)
    plt.gca().invert_yaxis()
    cbar = plt.colorbar()
    cbar.ax.tick_params(labelsize=18)
    plt.tight_layout()
    plt.savefig(test_folder+'actions_probability_trajectory.png')

def plot_expert_action_traj(actions, n_actions, test_folder):
    plt.figure(figsize=(8, 3))
    if n_actions == 6:
        plt.eventplot([np.where(actions == i)[0] for i in range(6)], lineoffsets=1, linelengths=0.5, colors=['red', 'blue', 'green', 'orange', 'purple', 'brown'])
        # plt.yticks(range(6), labels=["Action 0", "Action 1", "Action 2", "Action 3", "Action 4", "Action 5"])
        plt.yticks(range(6))
    elif n_actions == 5:
        plt.eventplot([np.where(actions == i)[0] for i in range(5)], lineoffsets=1, linelengths=0.5, colors=['red', 'blue', 'green', 'orange', 'purple'])
        # plt.yticks(range(5), labels=["Action 0", "Action 1", "Action 2", "Action 3", "Action 4"])
        plt.yticks(range(5))
    plt.tick_params(axis='x', which='major', labelsize=18)
    plt.tick_params(axis='y', which='minor', labelsize=18)
    plt.xlabel("Trajectory Step Index", fontsize=20)
    plt.ylabel("Action Index", fontsize=20)
    plt.title("Actions along the Expert Trajectory", fontsize=22)
    plt.tight_layout()
    plt.savefig(test_folder+'actions_along_trajectories.png')

def evaluate_action_distribution_metrics(actions, action_probability, action_of_interest):
    # Ensure input trajectories are NumPy arrays
    actions = np.array(actions)
    action_probability = np.array(action_probability)

    # Filter the trajectories for the action of interest
    expert_trajectory = np.where(actions == action_of_interest, 1.0, 0.0)
    replicated_action_prob = action_probability[:, action_of_interest]

    # print(f"Expert Action Shape: {expert_trajectory.shape}")
    # print(expert_trajectory)
    # print(f"Replicated Action Shape: {replicated_action_prob.shape}")
    # print(replicated_action_prob)

    # Reshape for compatibility with metrics
    expert_trajectory = expert_trajectory.reshape(-1, 1)
    replicated_action_prob = replicated_action_prob.reshape(-1, 1)

    # Modified Hausdorff Distance (MHD)
    def modified_hausdorff_distance(a, b):
        forward_hausdorff = directed_hausdorff(a, b)[0]
        backward_hausdorff = directed_hausdorff(b, a)[0]
        return max(forward_hausdorff, backward_hausdorff)
    mhd = modified_hausdorff_distance(expert_trajectory, replicated_action_prob)

    # Sliced Wasserstein Distance (SWD)
    swd = wasserstein_distance(
        expert_trajectory.flatten(), replicated_action_prob.flatten()
    )

    # p-value
    _,p_value = stats.ttest_ind(replicated_action_prob,expert_trajectory) 


    # Print results
    print('------')
    print(f"Metrics for Action {action_of_interest}:")
    print(f"Modified Hausdorff Distance (MHD): {mhd}")
    print(f"Sliced Wasserstein Distance (SWD): {swd}")
    print(f"p-value: {p_value}")

    # Return results as a dictionary
    return {
        "mhd": mhd,
        "swd": swd,
        "p_value": p_value,
    }