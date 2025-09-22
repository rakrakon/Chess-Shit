import torch.nn as nn


class PolicyValueNet(nn.Module):
    def __init__(self, in_channels: int,
                 policy_size: int,
                 hidden_channels: int = 128,
                 num_blocks: int = 2,
                 head_channels: int = 32):
        super().__init__()

        # Build trunk dynamically
        layers = []
        in_ch = in_channels
        for i in range(num_blocks):
            layers += [
                nn.Conv2d(in_ch, hidden_channels, 3, padding=1),
                nn.ReLU()
            ]
            in_ch = hidden_channels
        self.trunk = nn.Sequential(*layers)

        # Policy head
        self.policy_head = nn.Sequential(
            nn.Conv2d(hidden_channels, head_channels, 1), nn.ReLU(),
            nn.Flatten(),
            nn.Linear(head_channels * 8 * 8, policy_size)
        )

        # Value head
        self.value_head = nn.Sequential(
            nn.Conv2d(hidden_channels, head_channels, 1), nn.ReLU(),
            nn.Flatten(),
            nn.Linear(head_channels * 8 * 8, hidden_channels), nn.ReLU(),
            nn.Linear(hidden_channels, 1),
            nn.Tanh()  # outputs in [-1, 1]
        )

    def forward(self, x):
        # x: (B, C, 8, 8)
        h = self.trunk(x)
        policy_logits = self.policy_head(h)  # (B, A)
        value = self.value_head(h)  # (B, 1)
        return policy_logits, value
