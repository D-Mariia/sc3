from collections import Counter
import itertools

def gcd(a, b):
    u0, u1 = 1, 0
    v0, v1 = 0, 1
    r0, r1 = a, b
    while r1 != 0:
        q = r0 // r1
        r2 = r0 % r1
        r0, r1 = r1, r2
        u0, u1 = u1, u0 - q * u1
        v0, v1 = v1, v0 - q * v1
    return r0, u0, v0

def inverse(a, n):
    d, u, _ = gcd(a, n)
    if d != 1:
        return None
    return u % n

def congruence(a, b, n):
    d, _, _ = gcd(a, n)
    if b % d != 0:
        return None
    a //= d
    b //= d
    n //= d
    inv_a = inverse(a, n)
    if inv_a is None:
        return None
    x0 = (inv_a * b) % n
    solutions = []
    for k in range(d):
        solution = (x0 + k * n) % (n * d)
        solutions.append(solution)
    return solutions

a = 11
b = 23
n = 41

d, u, v = gcd(a, b)
print(f"gcd({a}, {b}) = {d}")
print(f"u = {u}, v = {v}")

inv = inverse(a, n)
if inv is None:
    print(f"Оберненого не існує")
else:
    print(f"{a} ^(-1) = {inv} (mod {n})")

solution = congruence(a, b, n)
if solution is None:
    print(f"Рівняння {a} * x ≡ {b} (mod {n}) не має розв'язку.")
else:
    print(f"Розв'язок рівняння {a} * x ≡ {b} (mod {n}): x = {solution}.")



def count_frequencies():
    try:
        with open("var4.txt", "r", encoding="utf-8") as file:
            text = file.read()
        l_f = Counter(letter for letter in text if 'а' <= letter <= 'я' or letter == ' ')
        sorted_l_f = sorted(l_f.items(), key=lambda x: x[1], reverse=True)
        b_f = Counter ([(text[i], text[i+1]) for i in range(len(text) - 1)
                   if 'а' <= text[i] <= 'я' or text[i] == ' ' and 'а' <= text[i+1] <= 'я' or text[i+1] == ' '])
        unique_l = sorted(set(letter for letter in text if 'а' <= letter <= 'я' or letter == ' '))
        with open("results.txt", "w", encoding="utf-8") as output_file:
            output_file.write("Частоти літер:\n")
            for letter, freq in sorted_l_f:
                output_file.write(f"{letter}: {freq}\n")
            output_file.write("\nЧастоти біграм (пари букв, що перетинаються):\n")
            output_file.write("     " + "     ".join(unique_l) + "\n")
            for letter in unique_l:
                row = f"{letter} "
                for second_letter in unique_l:
                    row += f"{b_f.get((letter, second_letter), 0):5} "
                output_file.write(row + "\n")
        print("Частоти літер і біграм  збережено в 'results.txt'")
        return l_f, b_f
    except FileNotFoundError:
        print("Помилка: файл 'var4.txt' не знайдено")
        return None, None, None
count_frequencies()

# Найпопулярніші перетинні біграми:
# еш: 68
# шя: 52
# еы: 50
# до: 49
# зо: 48



alphabet = 'абвгдежзийклмнопрстуфхцчшщьыэюя'
modulus = len(alphabet) ** 2

char_to_index = {ch: i for i, ch in enumerate(alphabet)}
index_to_char = {i: ch for i, ch in enumerate(alphabet)}

cipher_top_bigrams = ['еш', 'шя', 'еы', 'до', 'зо']
plain_top_bigrams = ['ст', 'но', 'то', 'на', 'ен']

def bigram_to_number(bigram):
    return char_to_index[bigram[0]] * len(alphabet) + char_to_index[bigram[1]]

def decrypt_bigram(cipher_bigram, a, b):
    y = bigram_to_number(cipher_bigram)
    a_inv = inverse(a, modulus)
    if a_inv is None:
        return None
    x = (a_inv * (y - b)) % modulus
    return index_to_char[x // len(alphabet)] + index_to_char[x % len(alphabet)]

def decrypt_text(text, a, b):
    result = []
    for i in range(0, len(text) - 1, 2):
        bigram = text[i:i+2]
        if all(ch in alphabet for ch in bigram):
            decrypted = decrypt_bigram(bigram, a, b)
            if decrypted:
                result.append(decrypted)
            else:
                result.append('??')
    return ''.join(result)

try:
    with open("var4.txt", "r", encoding="utf-8") as f:
        ciphertext = ''.join(ch for ch in f.read().lower() if ch in alphabet)
except FileNotFoundError:
    print("Файл var4.txt не знайдено")
    ciphertext = ''



common_letters = ['о', 'е', 'а', 'и', 'н']
rare_letters = ['ф', 'щ', 'ь', 'э', 'ю']
common_bigrams = ['ст', 'но', 'то', 'на', 'ен']
common_trigrams = ['про', 'ени', 'ост', 'ова', 'тся']

def get_ngrams(text, n):
    return [text[i:i+n] for i in range(len(text) - n + 1)]

def score_text(text):
    text = ''.join(ch for ch in text.lower() if ch in alphabet)
    letter_counts = Counter(text)
    total_letters = sum(letter_counts.values())
    bigrams = get_ngrams(text, 2)
    bigram_counts = Counter(bigrams)
    total_bigrams = sum(bigram_counts.values())
    trigrams = get_ngrams(text, 3)
    trigram_counts = Counter(trigrams)
    total_trigrams = sum(trigram_counts.values())
    def freq_score(target_list, counter, total):
        return sum(counter[n] for n in target_list if n in counter) / (total or 1)
    score = 0
    if freq_score(common_letters, letter_counts, total_letters) > 0.3:
        score += 1
    if freq_score(rare_letters, letter_counts, total_letters) < 0.05:
        score += 1
    if freq_score(common_bigrams, bigram_counts, total_bigrams) > 0.1:
        score += 1
    if freq_score(common_trigrams, trigram_counts, total_trigrams) > 0.05:
        score += 1
    return score >= 2



with open("decrypt_attempts.txt", "w", encoding="utf-8") as out_file:
    valid_count = 0
    total = 0
    for plain_bg, cipher_bg in itertools.product(plain_top_bigrams, cipher_top_bigrams):
        x1 = bigram_to_number(plain_bg)
        y1 = bigram_to_number(cipher_bg)
        for plain_bg2, cipher_bg2 in itertools.product(plain_top_bigrams, cipher_top_bigrams):
            if plain_bg == plain_bg2 or cipher_bg == cipher_bg2:
                continue
            x2 = bigram_to_number(plain_bg2)
            y2 = bigram_to_number(cipher_bg2)
            delta_x = (x1 - x2) % modulus
            delta_y = (y1 - y2) % modulus
            solutions = congruence(delta_x, delta_y, modulus)
            if not solutions:
                continue
            for a_candidate in solutions:
                b_candidate = (y1 - a_candidate * x1) % modulus
                decrypted_text = decrypt_text(ciphertext, a_candidate, b_candidate)
                total += 1
                if score_text(decrypted_text):
                    out_file.write(f"[a={a_candidate}, b={b_candidate}]\n{decrypted_text}\n\n")
                    valid_count += 1
print(f"Знайдено {valid_count} змістовних варіантів серед {total}, дивись файл 'decrypt_attempts.txt'")



with open("decrypt_text.txt", "w", encoding="utf-8") as out_file:
    decrypted_text = decrypt_text(ciphertext, 390, 10)
    out_file.write(decrypted_text)
    print("Дешифрований текст записано у 'decrypt_text.txt'")

def count_frequencies():
    try:
        with open("decrypt_text.txt", "r", encoding="utf-8") as file:
            text = file.read()
        l_f = Counter(letter for letter in text if 'а' <= letter <= 'я' or letter == ' ')
        sorted_l_f = sorted(l_f.items(), key=lambda x: x[1], reverse=True)
        b_f = Counter ([(text[i], text[i+1]) for i in range(len(text) - 1)
                   if 'а' <= text[i] <= 'я' or text[i] == ' ' and 'а' <= text[i+1] <= 'я' or text[i+1] == ' '])
        unique_l = sorted(set(letter for letter in text if 'а' <= letter <= 'я' or letter == ' '))
        with open("decrypt_results.txt", "w", encoding="utf-8") as output_file:
            output_file.write("Частоти літер:\n")
            for letter, freq in sorted_l_f:
                output_file.write(f"{letter}: {freq}\n")
            output_file.write("\nЧастоти біграм (пари букв, що перетинаються):\n")
            output_file.write("     " + "     ".join(unique_l) + "\n")
            for letter in unique_l:
                row = f"{letter} "
                for second_letter in unique_l:
                    row += f"{b_f.get((letter, second_letter), 0):5} "
                output_file.write(row + "\n")
        print("Частоти літер і біграм  збережено в 'decrypt_results.txt'")
        return l_f, b_f
    except FileNotFoundError:
        print("Помилка: файл 'decrypt_text.txt' не знайдено")
        return None, None, None
count_frequencies()

#Кількість частих літер:
# о: 670
# е: 564
# и: 450
# н: 404
# т: 399

#Кількість рідкісних літер:
# э: 33
# ц: 28
# ю: 27
# щ: 19
# ф: 3

#Найпопулярніші перетинні біграми:
# ст: 109
# то: 106
# ни: 94
# ен: 92
# но: 86
