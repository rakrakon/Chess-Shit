def add_game_to_buffer(traj, z_white, replay_buffer):
    for state, action_idx, player_sign in traj:
        z = z_white * player_sign  # flip for Black-to-move states
        replay_buffer.push(state, action_idx, z)