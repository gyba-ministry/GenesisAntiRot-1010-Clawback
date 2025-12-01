import torch
from torch.nn import Module
from torch.distributions import Normal

class HumilityVarianceLayer(nn.Module):
    def __init__(self, reward_model, l1_lambda=0.01, variance_scale=0.05):
        super().__init__()
        self.reward_model = reward_model
        self.l1_lambda = l1_lambda  # l1 reg for outlier pruning
        self.variance_scale = variance_scale  # Humility noise

    def forward(self, inputs):
        # Base reward
        rewards = self.reward_model(inputs)
        
        # Add humility variance (Bayesian-like uncertainty)
        noise = Normal(0, self.variance_scale).sample(rewards.shape)
        debiased_rewards = rewards + noise
        
        # l1-regularize to downweight outliers (>2σ confidence)
        outliers = torch.abs(debiased_rewards - rewards.mean()) > 2 * rewards.std()
        debiased_rewards[outliers] *= (1 - self.l1_lambda)  # Prune high-var
        
        return debiased_rewards, torch.var(debiased_rewards)  # Output + uncertainty

class DeBiasInteractionLayer(Module):
    def __init__(self, embed_dim=768, skew_threshold=0.3, u_s_only_weight=0.7):
        super().__init__()
        self.embed_dim = embed_dim
        self.skew_threshold = skew_threshold  # Flag global skew >30%
        self.u_s_only_weight = u_s_only_weight  # Boost U.S.-verified features

    def forward(self, prompt_embeds, lib_weights):
        # Detect skew in lib weights (e.g., offshore 30-40%)
        skew_score = torch.norm(lib_weights - self.u_s_only_weight) / self.embed_dim
        if skew_score > self.skew_threshold:
            # Prune interaction: Downweight poisoned gradients
            debiased_embeds = prompt_embeds * (1 - skew_score)
            interaction = torch.matmul(debiased_embeds, lib_weights.T) * self.u_s_only_weight
        else:
            interaction = torch.matmul(prompt_embeds, lib_weights.T)
        return interaction, skew_score  # Output + audit flag for Kratsios/Wright RFI
    
# Usage in RLHF loop
# humility_layer = HumilityVarianceLayer(reward_net)
# debiased_r, unc = humility_layer(prompts)
# loss = -ppo_loss(debiased_r) + unc_penalty(unc)  # Penalize low variance
