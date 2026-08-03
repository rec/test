import unicodedata

def get_accented_variants():
    # Dictionaries to hold our results
    uppercase_variants = {}
    lowercase_variants = {}

    # Initialize keys for all standard English letters
    for char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        uppercase_variants[char] = []
    for char in "abcdefghijklmnopqrstuvwxyz":
        lowercase_variants[char] = []

    # Scan Latin-1 Supplement and Latin Extended Unicode blocks (0x00A0 to 0x024F)
    # This covers the vast majority of European accented characters
    for codepoint in range(0x00A0, 0x0250):
        char = chr(codepoint)

        # Normalize the character to decomposed form (NFD).
        # This splits a character like 'é' into ('e' + '◌́')
        normalized = unicodedata.normalize('NFD', char)

        # If the character decomposes into multiple parts, the first part is the base letter
        if len(normalized) > 1:
            base_letter = normalized[0]

            # Check if the base letter is a standard Latin character
            if base_letter in uppercase_variants:
                uppercase_variants[base_letter].append(char)
            elif base_letter in lowercase_variants:
                lowercase_variants[base_letter].append(char)

    return uppercase_variants, lowercase_variants

def print_variants(variants_dict, title):
    print(f"=== {title} ===")
    for base, variants in variants_dict.items():
        if variants:
            # Join the variants with a space for clean printing
            print(f"{base}: {' '.join(variants)}")
        else:
            print(f"{base}: (No variants found in this range)")
    print("\n")

if __name__ == "__main__":
    upper_dict, lower_dict = get_accented_variants()

    print_variants(upper_dict, "Uppercase Accented Variants")
    print_variants(lower_dict, "Lowercase Accented Variants")
