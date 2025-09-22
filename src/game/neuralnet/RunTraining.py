import torch
from ActionEncoder import total_actions
from ChessRL import ChessRL
from ReplayBuffer import ReplayBuffer
from Model import PolicyValueNet
from SelfPlay import play_one_game
from Collect import add_game_to_buffer
from Train import train_step


def main(device="cpu"):
    print(f"Starting Chess RL training on {device}...")

    env = ChessRL()
    in_channels = 13
    policy_size = total_actions()

    model = PolicyValueNet(
        in_channels=in_channels,
        policy_size=total_actions(),
        hidden_channels=128,  # filters per conv
        num_blocks=2,  # how many conv layers
        head_channels=32  # channels in heads
    ).to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)
    buffer = ReplayBuffer(capacity=100_000)

    num_iterations = 1000
    for iteration in range(num_iterations):
        # --- Self-play ---
        traj, z_white = play_one_game(env, model, device=device, temperature=1.0, mcts_simulations=50)

        # Log game result
        num_moves = len(traj)
        result_str = "Draw" if z_white == 0 else ("White win" if z_white == 1 else "Black win")
        print(f"[Game {iteration + 1}] Moves: {num_moves}, Result: {result_str}")

        # Add game to buffer
        add_game_to_buffer(traj, z_white, buffer)
        print(f"Replay buffer size: {len(buffer)}")

        # --- Train if we have enough data ---
        if len(buffer) >= 512:
            batch = buffer.sample(256)
            metrics = train_step(model, optimizer, batch, device=device, policy_size=policy_size)

            if iteration % 10 == 0:
                print(f"[Train it {iteration}] "
                      f"loss={metrics['loss']:.3f}, "
                      f"p_loss={metrics['policy_loss']:.3f}, "
                      f"v_loss={metrics['value_loss']:.3f}, "
                      f"top1={metrics['policy_top1_acc']:.2%}")

    print("Training completed!")


if __name__ == "__main__":
    main(device="cuda" if torch.cuda.is_available() else "cpu")
