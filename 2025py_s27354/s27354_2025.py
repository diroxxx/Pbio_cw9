import random

def generate_dna_sequence(length):
    return ''.join(random.choices('ACGT', k=length))

def calculate_statistics(sequence):
    counts = {nuc: sequence.count(nuc) for nuc in 'ACGT'}
    total = len(sequence)
    percentages = {nuc: (counts[nuc] / total * 100) for nuc in counts}
    cg = counts['C'] + counts['G']
    at = counts['A'] + counts['T']
    cg_at_ratio = (cg / at * 100) if at > 0 else 0
    return percentages, cg_at_ratio

def insert_name(sequence, name):
    pos = random.randint(0, len(sequence))
    return sequence[:pos] + name + sequence[pos:]

def main():
    length = int(input("Podaj długość sekwencji: "))
    seq_id = input("Podaj ID sekwencji: ")
    description = input("Podaj opis sekwencji: ")
    name = input("Podaj imię: ")

    dna_sequence = generate_dna_sequence(length)
    stats, cg_at_ratio = calculate_statistics(dna_sequence)
    sequence_with_name = insert_name(dna_sequence, name)

    filename = f"{seq_id}.fasta"
    with open(filename, 'w') as f:
        f.write(f">{seq_id} {description}\n")
        f.write(sequence_with_name + "\n")

    print(f"\nSekwencja została zapisana do pliku {filename}")
    print("Statystyki sekwencji:")
    for nuc in 'ACGT':
        print(f"{nuc}: {stats[nuc]:.1f}%")
    print(f"%CG: {stats['C'] + stats['G']:.1f}")
    print(f"Stosunek CG do AT: {cg_at_ratio:.1f}%")

if __name__ == "__main__":
    main()
