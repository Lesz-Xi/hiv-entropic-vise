"""
Entropy Calculator for HIV-1 Sequence Analysis (v2)

Part of the Entropic Vise Framework for identifying
high-barrier thermodynamic constraints in viral proteins.

The algorithm calculates Shannon Entropy H(X) at each position
to identify highly conserved regions under purifying selection.

v2 Note: "High-barrier constraints" rather than "absolute immutability"
acknowledges that mutations (e.g., V38A, N43D in Enfuvirtide resistance)
can occur but impose severe fitness costs.
"""

import math
from collections import Counter


def calculate_shannon_entropy(sequences, min_occupancy=0.50):
    """
    Calculates Shannon Entropy for each position in an alignment.
    
    H(X) = - sum(p(x) * log2(p(x)))
    
    Args:
        sequences: List of aligned amino acid sequences
        min_occupancy: Minimum fraction of sequences with residue at position (default: 0.50)
        
    Returns:
        List of entropy values per position (None for invalid/gap-heavy positions)
        
    Note:
        - Ignores gaps ('-', '.', '?', '*')
        - Positions with <min_occupancy are marked as None (not "conserved", just absent)
        - Low entropy (<0.1 bits) indicates strong purifying selection
    """
    if not sequences:
        return []

    seq_length = len(sequences[0])
    num_sequences = len(sequences)
    entropies = []
    
    for i in range(seq_length):
        column_residues = []
        for seq in sequences:
            if i < len(seq):
                residue = seq[i]
                if residue not in ['-', '.', '?', '*']: 
                    column_residues.append(residue)
        
        # All-gap column = undefined (not conserved)
        if not column_residues:
            entropies.append(None)
            continue

        # Gap Filtering: Position must exist in sufficient sequences
        occupancy = len(column_residues) / num_sequences
        if occupancy < min_occupancy:
            entropies.append(None)
            continue

        # Calculate Shannon Entropy
        total_residues = len(column_residues)
        counts = Counter(column_residues)
        
        entropy = 0.0
        for residue, count in counts.items():
            probability = count / total_residues
            entropy -= probability * math.log2(probability)
            
        entropies.append(entropy)

    return entropies


def identify_conserved_regions(entropies, threshold=0.1, min_length=5):
    """
    Identifies contiguous regions with entropy below threshold.
    
    Args:
        entropies: List of entropy values from calculate_shannon_entropy()
        threshold: Maximum entropy to consider "conserved" (default: 0.1 bits)
        min_length: Minimum region length to report (default: 5 AA)
        
    Returns:
        List of tuples: (start, end, length) in 1-based coordinates
    """
    conserved_regions = []
    current_region = []
    
    for i, entropy in enumerate(entropies):
        if entropy is not None and entropy < threshold:
            if not current_region:
                current_region = [i + 1]  # 1-indexed
        else:
            if current_region:
                start = current_region[0]
                end = i
                length = end - start + 1
                if length >= min_length:
                    conserved_regions.append((start, end, length))
                current_region = []
                
    # Handle region active at end
    if current_region:
        start = current_region[0]
        end = len(entropies)
        length = end - start + 1
        if length >= min_length:
            conserved_regions.append((start, end, length))
            
    return conserved_regions


def load_fasta(filepath):
    """
    Simple FASTA parser.
    
    Args:
        filepath: Path to FASTA file
        
    Returns:
        List of sequence strings
    """
    sequences = []
    current_seq = []
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current_seq:
                    sequences.append("".join(current_seq))
                    current_seq = []
            else:
                current_seq.append(line)
        if current_seq:
            sequences.append("".join(current_seq))
            
    return sequences


def main():
    """
    Main analysis pipeline for Entropic Vise identification.
    
    Primary Target (v2): HXB2 residues 546-556 (SGIVQQQNNLL)
    This region shows near-zero entropy indicating strong purifying selection,
    though Enfuvirtide data shows mutations can occur with fitness cost.
    """
    filepath = "/Users/lesz/Documents/academic-integrity-agent/Caste_Study/Entropic_Vise/HIV_Sequence_DB/HIV1_FLT_2022_env_PRO.fasta"
    
    print("="*60)
    print("ENTROPIC VISE ANALYSIS (v2)")
    print("Framework: High-Barrier Thermodynamic Targeting")
    print("="*60)
    
    print(f"\nLoading sequences from {filepath}...")
    sequences = load_fasta(filepath)
    print(f"Loaded {len(sequences)} sequences.")
    
    if not sequences:
        print("Error: No sequences found.")
        return

    first_len = len(sequences[0])
    print(f"Alignment length: {first_len} positions.")
    
    print("\nCalculating Shannon Entropy per position...")
    entropies = calculate_shannon_entropy(sequences)
    
    print("\n--- Identifying High-Barrier Constraint Regions (Entropy < 0.1) ---")
    conserved_regions = identify_conserved_regions(entropies)
    
    print(f"\nFound {len(conserved_regions)} candidate regions > 5 AA length.\n")
    print(f"{'Start':<10} {'End':<10} {'Length':<10}")
    print("-" * 30)
    for start, end, length in conserved_regions:
        print(f"{start:<10} {end:<10} {length:<10}")
    
    print("\n" + "="*60)
    print("PRIMARY TARGET (v2): gp41 HR1 Domain")
    print("HXB2 Coordinates: 546-556")
    print("Sequence: SGIVQQQNNLL")
    print("Note: V38A/N43D mutations confer resistance but impose fitness costs")
    print("="*60)


if __name__ == "__main__":
    main()
