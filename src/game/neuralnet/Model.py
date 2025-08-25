import torch.nn as nn

class PolicyValueNet(nn.Module):
    def __init__(self, in_channels: int, policy_size: int):
        super().__init__()
        # Small, simple CNN trunk (start small; you can grow it later)
        self.trunk = nn.Sequential(
            nn.Conv2d(in_channels, 128, 3, padding=1), nn.ReLU(),
            nn.Conv2d(128, 128, 3, padding=1), nn.ReLU(),
        )
        self.policy_head = nn.Sequential(
            nn.Conv2d(128, 32, 1), nn.ReLU(),
            nn.Flatten(),
            nn.Linear(32 * 8 * 8, policy_size)
        )
        self.value_head = nn.Sequential(
            nn.Conv2d(128, 32, 1), nn.ReLU(),
            nn.Flatten(),
            nn.Linear(32 * 8 * 8, 128), nn.ReLU(),
            nn.Linear(128, 1),
            nn.Tanh()  # outputs in [-1, 1]
        )

    def forward(self, x):
        # x: (B, C, 8, 8)
        h = self.trunk(x)
        policy_logits = self.policy_head(h)  # (B, A)
        value = self.value_head(h)           # (B, 1)
        return policy_logits, value
