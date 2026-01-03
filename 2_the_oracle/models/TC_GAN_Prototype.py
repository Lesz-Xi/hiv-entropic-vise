import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# --- CONFIGURATION ---
# The Entropic Vise: HR1 Sequence (LTVWGIKQL)
# In a real model, we would one-hot encode this. For prototype, we use integer indices.
VISE_SEQUENCE = [10, 18, 20, 21, 5, 7, 9, 15, 10]  # Placeholder Indices
VISE_START_IDX = 568
VISE_END_IDX = 576
SEQ_LENGTH = 850  # Approx length of Env

class ThermodynamicDiscriminator(nn.Module):
    """ 
    The 'Physicist'.
    This is NOT a learnable network. It is a differentiable physics engine.
    """
    def __init__(self, vise_seq, start_idx):
        super().__init__()
        self.vise_seq = torch.tensor(vise_seq, dtype=torch.long)
        self.start_idx = start_idx
        
    def forward(self, generated_seq_logits):
        """
        Input: generated_seq_logits (Batch, Seq_Len, Vocab_Size)
        Output: Physics_Loss (Scalar)
        """
        # Extract the Vise Region from the generated logits
        # Shape: (Batch, Vise_Len, Vocab_Size)
        vise_logits = generated_seq_logits[:, self.start_idx : self.start_idx + len(self.vise_seq), :]
        
        # Get the predicted amino acids (Softmax for differentiability)
        probs = torch.softmax(vise_logits, dim=-1)
        
        # Calculate Cross-Entropy Loss against the IMMUTABLE Reference
        # We want the model to predict the Vise Sequence with 100% probability.
        # Any deviation is a Thermodynamic Violation.
        
        # Flatten for loss calculation
        target = self.vise_seq.repeat(probs.shape[0]) # Repeat for batch
        input_flat = probs.view(-1, probs.shape[-1])
        
        # This acts as the "Infinite Wall"
        # If the model deviates, this loss skyrockets.
        physics_loss = nn.functional.cross_entropy(input_flat, target)
        
        return physics_loss

class BioDiscriminator(nn.Module):
    """
    The 'Virologist'. Standard GAN Discriminator.
    Checks if the sequence looks like valid HIV.
    """
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(SEQ_LENGTH, 512),
            nn.LeakyReLU(0.2),
            nn.Linear(512, 1),
            nn.Sigmoid()
        )
        
    def forward(self, x):
        return self.model(x.float())

class ViralGenerator(nn.Module):
    """
    The 'Virus'.
    Tries to generate valid Env sequences that escape detection.
    """
    def __init__(self, latent_dim=100):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(latent_dim, 256),
            nn.ReLU(),
            nn.Linear(256, SEQ_LENGTH), # simplified output for prototype
            # In production, output would be (Seq_Len, Vocab_Size)
        )
        
    def forward(self, z):
        return self.model(z)

# --- TRAINING LOOP PROTO ---
def train_tc_gan():
    # Hyperparameters
    LAMBDA_PHYS = 1000.0 # The "Infinite" Penalty Weight
    
    # Init Models
    generator = ViralGenerator()
    d_bio = BioDiscriminator()
    d_phys = ThermodynamicDiscriminator(VISE_SEQUENCE, VISE_START_IDX)
    
    optimizer_G = optim.Adam(generator.parameters(), lr=0.0002)
    
    print("--- INITIATING TC-GAN PROTOCOL ---")
    print(f"Thermodynamic Constraint Active on Residues {VISE_START_IDX}-{VISE_END_IDX}")
    print(f"Penalty Weight (Lambda): {LAMBDA_PHYS}")
    
    # Fake Training Step
    z = torch.randn(64, 100) # Batch of 64 latent vectors
    
    # 1. Generate Fake Sequences
    fake_seqs = generator(z) # (64, 850)
    
    # 2. Reshape for Physics Check (Simulating Vocab distribution for demo)
    # In real Transformer, this would be naturally (B, L, V)
    fake_logits = torch.randn(64, SEQ_LENGTH, 22) 
    
    # 3. Calculate Losses
    # Bio Loss: Does it look like HIV? (Standard GAN trickery)
    bio_validity = d_bio(fake_seqs) 
    g_loss_bio = -torch.mean(torch.log(bio_validity))
    
    # Physics Loss: Did it break the Vise?
    phys_loss = d_phys(fake_logits)
    
    # Total Generator Loss
    g_loss_total = g_loss_bio + (LAMBDA_PHYS * phys_loss)
    
    print("\n[EPOCH 1 REPORT]")
    print(f"Bio-Mimicry Loss: {g_loss_bio.item():.4f}")
    print(f"Thermodynamic Violation Loss: {phys_loss.item():.4f}")
    print(f"Total Weighted Loss: {g_loss_total.item():.4f}")
    
    if phys_loss.item() > 0.1:
        print(">> ALERT: Thermodynamic Laws Violated. Mutation Rejected.")
    else:
        print(">> SUCCESS: Escape Mutant Generated within Physical Constraints.")

if __name__ == "__main__":
    train_tc_gan()
