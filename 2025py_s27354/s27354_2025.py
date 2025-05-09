# Program: FASTA Sequence Generator
# Cel: Ten program generuje losową sekwencję DNA, umożliwia użytkownikowi określenie długości, ID i opisu sekwencji,
#       wstawia podane imię użytkownika w losowe miejsce (nie wpływające na statystyki) i zapisuje wynik w formacie FASTA.
# Kontekst: Bioinformatyka – generowanie danych testowych w formacie FASTA do analiz sekwencji DNA.

import random  # biblioteka do operacji losowych

# Funkcja do generowania sekwencji DNA z losowych nukleotydów A, C, G, T
def generate_dna_sequence(length):
    return ''.join(random.choices('ACGT', k=length))  # losowe wybieranie znaków z A, C, G, T i łączenie ich w sekwencję


# Funkcja do obliczania statystyk sekwencji DNA (procent A, C, G, T i stosunek CG/AT)
def calculate_statistics(sequence):
    # ORIGINAL:
    # counts = {nuc: sequence.count(nuc) for nuc in 'ACGT'}
    # MODIFIED (zoptymalizowano liczenie znaków, aby wykonać tylko jedno przejście po sekwencji):
    counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0}  # inicjalizacja słownika do zliczania wystąpień nukleotydów
    for nuc in sequence:  # przejście przez każdy znak w sekwencji
        if nuc in counts:  # jeśli znak to A, C, G lub T
            counts[nuc] += 1  # zwiększ licznik odpowiedniego nukleotydu

    total = len(sequence)  # całkowita długość sekwencji
    percentages = {nuc: (counts[nuc] / total * 100) for nuc in
                   counts}  # obliczanie procentowego udziału każdego nukleotydu
    cg = counts['C'] + counts['G']  # suma wystąpień C i G
    at = counts['A'] + counts['T']  # suma wystąpień A i T
    cg_at_ratio = (cg / at * 100) if at > 0 else 0  # stosunek CG do AT jako procent
    return percentages, cg_at_ratio  # zwrócenie słownika procentów i stosunku

# Funkcja do wstawiania imienia w losowe miejsce w sekwencji
# Imię nie wpływa na statystyki nukleotydów, więc nie jest wliczane do obliczeń
def insert_name(sequence, name):
    pos = random.randint(0, len(sequence))  # losowa pozycja wstawienia imienia w sekwencji
    return sequence[:pos] + name + sequence[pos:]  # zwrócenie sekwencji z wstawionym imieniem

# Funkcja pomocnicza do dzielenia sekwencji na linie po 60 znaków (zgodnie z konwencją FASTA)
def format_fasta_sequence(seq, line_length=60):
    return '\n'.join(seq[i:i+line_length] for i in range(0, len(seq), line_length))  # podział sekwencji na linie po 60 znaków

# Główna funkcja programu
def main():
    # Pobieranie danych od użytkownika
    # ORIGINAL:
    # length = int(input("Podaj długość sekwencji: "))
    # seq_id = input("Podaj ID sekwencji: ")
    # description = input("Podaj opis sekwencji: ")
    # name = input("Podaj imię: ")
    # MODIFIED (walidacja wszystkich pól które użytkownik wprowadza)
    while True:
        try:
            length = int(input("Podaj długość sekwencji: "))  # pobranie długości sekwencji i rzutowanie na int
            if length <= 0:  # sprawdzenie, czy długość jest dodatnia
                raise ValueError("Długość musi być liczbą dodatnią.")
            break  # wyjście z pętli, jeśli dane poprawne
        except ValueError as e:
            print(f"Błąd: {e}")  # informacja o błędnych danych wejściowych

    seq_id = input("Podaj ID sekwencji: ").strip()  # pobranie ID sekwencji i usunięcie białych znaków
    while not seq_id.isalnum():  # sprawdzenie, czy ID zawiera tylko litery i cyfry
        print("ID sekwencji może zawierać tylko litery i cyfry.")
        seq_id = input("Podaj poprawne ID sekwencji: ").strip()

    description = input("Podaj opis sekwencji: ").strip()  # pobranie opisu sekwencji

    name = input("Podaj imię: ").strip()  # pobranie imienia użytkownika
    while not name.isalpha():  # sprawdzenie, czy imię zawiera tylko litery
        print("Imię może zawierać tylko litery.")
        name = input("Podaj poprawne imię: ").strip()

    dna_sequence = generate_dna_sequence(length)  # generowanie losowej sekwencji DNA
    stats, cg_at_ratio = calculate_statistics(dna_sequence)  # obliczenie statystyk sekwencji
    sequence_with_name = insert_name(dna_sequence, name)  # wstawienie imienia w losowe miejsce sekwencji

    # ORIGINAL:
    # filename = f"{seq_id}.fasta"
    # MODIFIED (walidacja ID – usunięcie niedozwolonych znaków z nazwy pliku):
    filename = f"{''.join(c for c in seq_id if c.isalnum())}.fasta"  # tworzenie nazwy pliku na podstawie ID

    with open(filename, 'w') as f:  # otwarcie pliku do zapisu
        f.write(f">{seq_id} {description}\n")  # zapis nagłówka FASTA z ID i opisem
        f.write(format_fasta_sequence(sequence_with_name) + "\n")  # zapis sekwencji DNA w liniach po 60 znaków

    # Wyświetlenie wyników i statystyk
    print(f"\nSekwencja została zapisana do pliku {filename}")  # informacja o zapisanym pliku
    print("Statystyki sekwencji:")
    for nuc in 'ACGT':  # iteracja po nukleotydach
        print(f"{nuc}: {stats[nuc]:.1f}%")  # wyświetlenie procentowego udziału danego nukleotydu
    print(f"%CG: {stats['C'] + stats['G']:.1f}")  # suma udziału C i G
    print(f"Stosunek CG do AT: {cg_at_ratio:.1f}%")  # wyświetlenie stosunku CG do AT

# Uruchomienie programu
if __name__ == "__main__":
    main()  # uruchomienie głównej funkcji programu

