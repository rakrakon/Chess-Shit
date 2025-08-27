import numpy as np
import torch
import torch.nn as nn

def train_step(model, optimizer, batch, device="cpu", policy_size=None):
    states, actions, outcomes = batch
    # Stack and move to device
    x = torch.from_numpy(
        np.stack(states, axis=0)
    ).float().permute(0, 3, 1, 2).to(device)                        # (B,C,8,8)
    a = torch.tensor(actions, dtype=torch.long, device=device)   # (B,)
    z = torch.tensor(outcomes, dtype=torch.float32, device=device).unsqueeze(1)  # (B,1)

    policy_logits, v = model(x)                       # (B,A), (B,1)

    # Policy loss: cross-entropy with one-hot action
    policy_loss = nn.functional.cross_entropy(policy_logits, a)

    # Value loss: MSE to z
    value_loss = nn.functional.mse_loss(v, z)

    # (Optional) L2 weight decay handled by optimizer's weight_decay
    loss = policy_loss + value_loss

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    with torch.no_grad():
        acc = (policy_logits.argmax(dim=1) == a).float().mean().item()

    return {
        "loss": float(loss.item()),
        "policy_loss": float(policy_loss.item()),
        "value_loss": float(value_loss.item()),
        "policy_top1_acc": acc
    }
