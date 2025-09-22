import math
import numpy as np
import torch
from collections import defaultdict

from src.game.neuralnet.RLUtils import masked_softmax


class MCTSNode:
    def __init__(self, state_key, prior):
        self.state_key = state_key
        self.P = prior        # action -> prior prob
        self.N = defaultdict(int)  # visit counts
        self.W = defaultdict(float) # total value
        self.Q = defaultdict(float) # mean value
        self.children = {}    # action -> state_key

def run_mcts(env, model, root_state, sims=25, device="cpu", c_puct=1.0):
    """
    env      : ChessRL env (cloned each sim)
    model    : PolicyValueNet
    root_state: (1,C,8,8) torch tensor of current state
    sims     : how many simulations to run
    returns  : action index chosen by max visits
    """
    # Convert state to a hashable key (string)
    def state_to_key(state_np):
        return state_np.tobytes()  # simple but works

    # Evaluate root
    state_np = root_state.squeeze(0).permute(1,2,0).cpu().numpy()  # back to (8,8,C)
    key = state_to_key(state_np)
    valid_actions = env.get_valid_actions()

    with torch.no_grad():
        policy_logits, value = model(root_state.to(device))
        policy_logits = policy_logits.squeeze(0)
    probs = masked_softmax(policy_logits, valid_actions, temperature=1.0).cpu().numpy()
    prior = {a: probs[a] for a in valid_actions}
    root = MCTSNode(key, prior)
    nodes = {key: root}

    # --- Simulations ---
    for _ in range(sims):
        sim_env = env.copy() # TODO: Write that shit
        node = root
        path = []
        done = False

        # Selection
        while True:
            valid_actions = sim_env.get_valid_actions()
            if len(valid_actions) == 0 or done:
                break

            # Pick action using PUCT
            best_u, best_a = -1e9, None
            total_N = sum(node.N[a] for a in valid_actions) + 1
            for a in valid_actions:
                Q = node.Q[a]
                U = c_puct * node.P.get(a, 1e-8) * math.sqrt(total_N) / (1 + node.N[a])
                score = Q + U
                if score > best_u:
                    best_u, best_a = score, a
            a = best_a
            path.append((node, a))

            # Step
            _, reward, done = sim_env.step(a)
            state_np = sim_env.board.encode()  # must return (8,8,C)
            key = state_to_key(state_np)

            if key not in nodes:
                # Expand
                s_tensor = torch.from_numpy(state_np).float().permute(2,0,1).unsqueeze(0).to(device)
                with torch.no_grad():
                    policy_logits, value = model(s_tensor)
                policy_logits = policy_logits.squeeze(0)
                valid_actions = sim_env.get_valid_actions()
                probs = masked_softmax(policy_logits, valid_actions, temperature=1.0).cpu().numpy()
                prior = {a: probs[a] for a in valid_actions}
                new_node = MCTSNode(key, prior)
                nodes[key] = new_node
                node.children[a] = new_node
                node = new_node
                break
            else:
                node = nodes[key]

        # Use terminal value or NN value
        if done:
            v = sim_env.get_winner()
            if v is None:  # draw
                value = 0.0
            else:
                value = 1.0 if v == env.board.get_current_turn() else -1.0
        else:
            # value from last eval above
            value = float(value.item())

        # Backprop
        for n, a in reversed(path):
            n.N[a] += 1
            n.W[a] += value
            n.Q[a] = n.W[a] / n.N[a]
            value = -value  # switch perspective

    # Pick action with highest visits
    visits = np.array([root.N[a] for a in valid_actions])
    best_a = valid_actions[int(np.argmax(visits))]
    return best_a
