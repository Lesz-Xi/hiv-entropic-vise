"""
HXB2 Coordinate Mapper for Entropic Vise Analysis (v2)

Maps alignment indices to HXB2 reference numbering.
Critical for validating that identified conserved regions
correspond to known functional domains.

v2 Update:
- Primary target corrected to HXB2 546-556 (SGIVQQQNNLL)
- Previous coordinates (568-576) were incorrect
- Added V38A/N43D resistance context
"""

from entropy_calculator import load_fasta


# v2 Target Regions (HXB2 numbering)
V2_TARGETS = {
    "HR1_PRIMARY": {
        "hxb2_start": 546,
        "hxb2_end": 556,
        "sequence": "SGIVQQQNNLL",
        "description": "gp41 HR1 Domain - Primary Entropic Vise target",
        "resistance_mutations": ["V38A (HXB2 549)", "N43D (HXB2 554)"]
    },
    "MPER_SECONDARY": {
        "hxb2_start": 678,
        "hxb2_end": 682,
        "sequence": "WLWYI",
        "description": "Membrane Proximal External Region - Secondary target"
    }
}


def build_alignment_map(reference_seq):
    """
    Builds mapping from alignment position to HXB2 numbering.
    
    Args:
        reference_seq: HXB2 reference sequence from alignment
        
    Returns:
        Dict mapping alignment index -> (residue, HXB2_number)
    """
    align_map = {}
    hxb2_counter = 0
    
    for i, char in enumerate(reference_seq):
        if char not in ['-', '?', '.']:
            hxb2_counter += 1
            align_map[i] = (char, hxb2_counter)
        else:
            align_map[i] = (char, None)
            
    return align_map


def hxb2_to_alignment_index(align_map, hxb2_position):
    """
    Finds alignment index for a given HXB2 position.
    
    Args:
        align_map: Mapping from build_alignment_map()
        hxb2_position: HXB2 residue number
        
    Returns:
        Alignment index (0-based) or None if not found
    """
    for idx, (residue, hxb2_num) in align_map.items():
        if hxb2_num == hxb2_position:
            return idx
    return None


def map_alignment_to_hxb2(filepath, regions_of_interest):
    """
    Maps alignment indices to HXB2 numbering.
    HXB2 is assumed to be the first sequence in the file.
    
    Args:
        filepath: Path to aligned FASTA file
        regions_of_interest: List of (start, end) tuples (1-based alignment coords)
    """
    sequences = load_fasta(filepath)
    if not sequences:
        print("Error: No sequences loaded.")
        return

    hxb2_seq = sequences[0]
    print(f"Reference Length (Alignment): {len(hxb2_seq)}")
    
    align_map = build_alignment_map(hxb2_seq)

    print("\n--- Mapping Regions to HXB2 Numbering ---\n")
    print(f"{'Align Start':<12} {'Align End':<10} {'HXB2 Start':<12} {'HXB2 End':<10} {'Sequence':<25}")
    print("-" * 75)

    for start_align, end_align in regions_of_interest:
        idx_start = start_align - 1
        idx_end = end_align - 1 
        
        start_residue = align_map.get(idx_start, ('?', None))
        end_residue = align_map.get(idx_end, ('?', None))
        
        fragment = hxb2_seq[idx_start : idx_end+1].replace('-', '')
        
        hxb2_s_str = f"{start_residue[0]}{start_residue[1]}" if start_residue[1] else "Gap"
        hxb2_e_str = f"{end_residue[0]}{end_residue[1]}" if end_residue[1] else "Gap"
        
        print(f"{start_align:<12} {end_align:<10} {hxb2_s_str:<12} {hxb2_e_str:<10} {fragment:<25}")


def validate_v2_targets(filepath):
    """
    Validates that v2 target regions are present in the alignment.
    Extracts sequences at HXB2 546-556 and 678-682 for verification.
    """
    sequences = load_fasta(filepath)
    if not sequences:
        print("Error: No sequences loaded.")
        return
        
    hxb2_seq = sequences[0]
    align_map = build_alignment_map(hxb2_seq)
    
    print("\n" + "="*60)
    print("V2 TARGET VALIDATION")
    print("="*60)
    
    for target_name, target_info in V2_TARGETS.items():
        start_hxb2 = target_info["hxb2_start"]
        end_hxb2 = target_info["hxb2_end"]
        expected_seq = target_info["sequence"]
        
        # Find alignment indices
        start_idx = hxb2_to_alignment_index(align_map, start_hxb2)
        end_idx = hxb2_to_alignment_index(align_map, end_hxb2)
        
        if start_idx is None or end_idx is None:
            print(f"\n{target_name}: Could not locate in alignment")
            continue
            
        # Extract sequence
        extracted = hxb2_seq[start_idx:end_idx+1].replace('-', '')
        
        print(f"\n{target_name}:")
        print(f"  HXB2 Range: {start_hxb2}-{end_hxb2}")
        print(f"  Expected:   {expected_seq}")
        print(f"  Extracted:  {extracted}")
        print(f"  Match:      {'✓ VALID' if extracted == expected_seq else '✗ MISMATCH'}")
        print(f"  Description: {target_info['description']}")
        
        if "resistance_mutations" in target_info:
            print(f"  Known Escape: {', '.join(target_info['resistance_mutations'])}")


def main():
    filepath = "/Users/lesz/Documents/academic-integrity-agent/Caste_Study/Entropic_Vise/HIV_Sequence_DB/HIV1_FLT_2022_env_PRO.fasta"
    
    print("="*60)
    print("HXB2 COORDINATE MAPPER (v2)")
    print("Primary Target: HXB2 546-556 (SGIVQQQNNLL)")
    print("="*60)
    
    # Validate v2 targets
    validate_v2_targets(filepath)
    
    # Original analysis regions (for reference)
    print("\n\n--- Original Analysis Regions (Reference) ---")
    regions = [
        (1358, 1366),  # Primary candidate from entropy analysis
        (1328, 1333),
        (587, 591),
        (177, 181),
        (1552, 1556)
    ]
    map_alignment_to_hxb2(filepath, regions)


if __name__ == "__main__":
    main()
