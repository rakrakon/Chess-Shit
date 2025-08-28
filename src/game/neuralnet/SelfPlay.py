import copy

import torch
from RLUtils import masked_softmax, sample_action
from src.game.Color import Color

# TODO: Fix pins

@torch.no_grad()
def play_one_game(env, model, device="cpu", temperature=1.0):
    """
    Returns a list of (state_tensor, action_idx, player_sign) and the final outcome z in {-1,0,1} for White.
    player_sign: +1 if the stored state was from White-to-move, -1 if from Black-to-move.
    """
    traj = []
    game = [env.board]
    state = env.reset() # shape (8, 8, 13)
    done = False
    print("Started Game with Board:")
    env.board.print_board()

    while not done:
        # Convert (H,W,C) -> (C,H,W)
        s = torch.from_numpy(state).float().permute(2, 0, 1).unsqueeze(0).to(device)  # (1, C, 8, 8)

        # Forward pass
        policy_logits, _ = model(s)          # (1, A), (1,1)
        policy_logits = policy_logits.squeeze(0)

        # Mask invalid moves
        valid_actions = env.get_valid_actions()  # list[int]
        probs = masked_softmax(policy_logits, valid_actions, temperature=temperature)
        # Sample an action
        action_idx = sample_action(probs)
        # Player sign (+1 for White, -1 for Black)
        current_player_is_white = env.board.get_current_turn() == Color.WHITE
        player_sign = 1.0 if current_player_is_white else -1.0

        # Store trajectory (raw state, not permuted)
        traj.append((state, action_idx, player_sign))

        # Apply move
        state, reward, done = env.step(action_idx)
        game.append(copy.deepcopy(env.board))

    # Determine final outcome from White's perspective.
    winner = env.get_winner()  # should be "WHITE", "BLACK", or None
    if winner is None:
        z_white = 0.0
    else:
        z_white = 1.0 if winner == Color.WHITE else -1.0

    return traj, z_white
