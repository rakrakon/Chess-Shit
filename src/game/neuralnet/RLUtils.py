import torch

def masked_softmax(logits: torch.Tensor, valid_indices: list[int], temperature: float = 1.0):
    """
    logits: (A), tensor where A = total action space
    valid_indices: indices that are legal in current state
    """
    A = logits.shape[-1]
    mask = torch.full((A,), float("-inf"), device=logits.device)
    if len(valid_indices) == 0:
        raise RuntimeError("No legal actions available.")
    mask[valid_indices] = 0.0
    masked = (logits / max(1e-6, temperature)) + mask
    probs = torch.softmax(masked, dim=-1)
    return probs

def sample_action(probs: torch.Tensor):
    # probs: (A,)
    return torch.multinomial(probs, num_samples=1).item()
