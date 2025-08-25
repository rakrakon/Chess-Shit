import random
from collections import deque

class ReplayBuffer:
    def __init__(self, capacity: int):
        self.buf = deque(maxlen=capacity)

    def push(self, state_tensor, action_idx: int, outcome: float):
        # outcome should be in [-1, 0, 1] from the perspective of the player to move at that state
        self.buf.append((state_tensor, action_idx, outcome))

    def sample(self, batch_size: int):
        batch = random.sample(self.buf, batch_size)
        states, actions, outcomes = zip(*batch)
        return states, actions, outcomes

    def __len__(self):
        return len(self.buf)
