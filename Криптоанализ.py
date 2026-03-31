# -*- coding: utf-8 -*-

import math
import random
from collections import Counter
from typing import Optional


# --------------------------------------------------
# 1. Алфавит
# --------------------------------------------------
# Русский алфавит:
# АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ
ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
M = len(ALPHABET)  # 33

CHAR_TO_NUM = {ch: i for i, ch in enumerate(ALPHABET)}
NUM_TO_CHAR = {i: ch for i, ch in enumerate(ALPHABET)}


# --------------------------------------------------
# 2. Вспомогательные функции
# --------------------------------------------------
def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)


def is_invertible_mod(a: int, m: int = M) -> bool:
    """
    Проверяет, существует ли обратный элемент к a по модулю m.
    Для этого нужно gcd(a, m) = 1.
    """
    return gcd(a, m) == 1


def mod_inv(a: int, m: int = M) -> int:
    """
    Обратный элемент по модулю.
    Работает только если gcd(a, m) = 1.
    """
    if not is_invertible_mod(a, m):
        raise ValueError(f"Элемент {a} не имеет обратного по модулю {m}")
    return pow(a, -1, m)


def normalize_text(text: str) -> str:
    """
    Приведение текста к нижнему регистру
    и удаление символов вне заданного алфавита.
    """
    text = text.lower()
    return "".join(ch for ch in text if ch in CHAR_TO_NUM)


def text_to_nums(text: str) -> list[int]:
    return [CHAR_TO_NUM[ch] for ch in text]


def nums_to_text(nums: list[int]) -> str:
    return "".join(NUM_TO_CHAR[n] for n in nums)


# --------------------------------------------------
# 3. Допустимые значения a
# --------------------------------------------------
VALID_A_VALUES = [a for a in range(M) if is_invertible_mod(a, M)]
# Для m = 33 это будут числа, не кратные 3 и 11

VALID_A_SET = set(VALID_A_VALUES)


def nearest_valid_a(a: int) -> int:
    """
    Возвращает ближайшее допустимое значение a по модулю 33,
    для которого существует обратный элемент.
    """
    a %= M

    if a in VALID_A_SET:
        return a

    for delta in range(1, M + 1):
        left = (a - delta) % M
        right = (a + delta) % M

        if left in VALID_A_SET:
            return left
        if right in VALID_A_SET:
            return right

    # Теоретически сюда не дойдем
    return VALID_A_VALUES[0]


# --------------------------------------------------
# 4. Рекуррентные ключи
# --------------------------------------------------
def build_key_sequences(length: int, a1: int, a2: int, b1: int, b2: int) -> tuple[list[int], list[int]]:
    """
    Строит последовательности ключей:
        a_i = a_{i-1} * a_{i-2} mod 33
        b_i = b_{i-1} + b_{i-2} mod 33
    """
    a = [a1, a2]
    b = [b1, b2]

    for i in range(2, length):
        a_next = (a[i - 1] * a[i - 2]) % M
        b_next = (b[i - 1] + b[i - 2]) % M
        a.append(a_next)
        b.append(b_next)

    return a, b


def key_is_valid_for_length(length: int, a1: int, a2: int, b1: int, b2: int) -> bool:
    """
    Проверяет, что для всей длины текста все a_i обратимы по модулю 33.
    Иначе расшифрование невозможно.
    """
    a, _ = build_key_sequences(length, a1, a2, b1, b2)
    return all(is_invertible_mod(ai, M) for ai in a)


# --------------------------------------------------
# 5. Шифрование / расшифрование
# --------------------------------------------------
def encrypt(plaintext: str, a1: int, a2: int, b1: int, b2: int) -> Optional[str]:
    plaintext = normalize_text(plaintext)
    x = text_to_nums(plaintext)

    if not key_is_valid_for_length(len(x), a1, a2, b1, b2):
        return None

    a, b = build_key_sequences(len(x), a1, a2, b1, b2)

    y = []
    for i, xi in enumerate(x):
        yi = (a[i] * xi + b[i]) % M
        y.append(yi)

    return nums_to_text(y)


def decrypt(ciphertext: str, a1: int, a2: int, b1: int, b2: int) -> Optional[str]:
    ciphertext = normalize_text(ciphertext)
    y = text_to_nums(ciphertext)

    if not key_is_valid_for_length(len(y), a1, a2, b1, b2):
        return None

    a, b = build_key_sequences(len(y), a1, a2, b1, b2)

    x = []
    for i, yi in enumerate(y):
        ai_inv = mod_inv(a[i], M)
        xi = (ai_inv * ((yi - b[i]) % M)) % M
        x.append(xi)

    return nums_to_text(x)


# --------------------------------------------------
# 6. Языковая модель
# --------------------------------------------------
def build_ngram_log_model(corpus_text: str, n: int = 3):
    """
    Простая n-граммная модель языка с лапласовским сглаживанием.
    """
    corpus_text = normalize_text(corpus_text)

    counts = Counter()
    total = 0

    for i in range(len(corpus_text) - n + 1):
        gram = corpus_text[i:i + n]
        counts[gram] += 1
        total += 1

    vocab_size = M ** n

    def score(text: str) -> float:
        text = normalize_text(text)

        if len(text) < n:
            return float("-inf")

        s = 0.0
        for i in range(len(text) - n + 1):
            gram = text[i:i + n]
            prob = (counts.get(gram, 0) + 1) / (total + vocab_size)
            s += math.log(prob)

        return s

    return score


# --------------------------------------------------
# 7. Эвристики для русского текста
# --------------------------------------------------
COMMON_BIGRAMS = [
    "ст", "но", "то", "на", "ен", "ов", "ни", "ра", "ко", "ро",
    "по", "ос", "пр", "не", "ли", "ре", "го", "ал", "ан", "от"
]

BAD_BIGRAMS = [
    "аъ", "оъ", "уы", "йъ", "ъы", "щщ", "жы", "шы", "ьыы", "ъь"
]


def heuristic_bonus(text: str) -> float:
    score = 0.0

    for bg in COMMON_BIGRAMS:
        score += text.count(bg) * 2.0

    for bg in BAD_BIGRAMS:
        score -= text.count(bg) * 8.0

    return score


def full_text_score(text: Optional[str], ngram_score_func) -> float:
    if text is None:
        return float("-inf")

    return ngram_score_func(text) + heuristic_bonus(text)


# --------------------------------------------------
# 8. Случайный допустимый ключ и мутация
# --------------------------------------------------
def random_valid_a() -> int:
    return random.choice(VALID_A_VALUES)


def random_key_for_length(length: int, max_tries: int = 5000) -> tuple[int, int, int, int]:
    """
    Пытается найти случайный ключ, который пригоден
    для расшифрования текста данной длины.
    """
    for _ in range(max_tries):
        a1 = random_valid_a()
        a2 = random_valid_a()
        b1 = random.randint(0, M - 1)
        b2 = random.randint(0, M - 1)

        if key_is_valid_for_length(length, a1, a2, b1, b2):
            return a1, a2, b1, b2

    raise RuntimeError("Не удалось подобрать случайный допустимый ключ")


def mutate_key(key: tuple[int, int, int, int], length: int, max_tries: int = 200) -> tuple[int, int, int, int]:
    """
    Случайно слегка меняет один из параметров ключа.
    После мутации проверяет, что ключ по-прежнему
    корректен для всей длины текста.
    """
    a1, a2, b1, b2 = key

    for _ in range(max_tries):
        na1, na2, nb1, nb2 = a1, a2, b1, b2
        which = random.randint(0, 3)

        if which == 0:
            delta = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            na1 = nearest_valid_a(na1 + delta)

        elif which == 1:
            delta = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            na2 = nearest_valid_a(na2 + delta)

        elif which == 2:
            nb1 = (nb1 + random.randint(-6, 6)) % M

        else:
            nb2 = (nb2 + random.randint(-6, 6)) % M

        if key_is_valid_for_length(length, na1, na2, nb1, nb2):
            return na1, na2, nb1, nb2

    return key


# --------------------------------------------------
# 9. Стохастический поиск
# --------------------------------------------------
def stochastic_search(
    ciphertext: str,
    corpus_text: str,
    restarts: int = 60,
    iterations_per_restart: int = 4000,
    seed: int = 42,
    top_k: int = 10,
) -> tuple[tuple[int, int, int, int], str, float, list[tuple[float, tuple[int, int, int, int], str]]]:
    """
    Статистический поиск ключа без полного перебора.
    """
    random.seed(seed)
    ciphertext = normalize_text(ciphertext)
    text_len = len(ciphertext)

    ngram_score = build_ngram_log_model(corpus_text, n=3)

    global_best_key = None
    global_best_text = None
    global_best_score = float("-inf")

    best_candidates: list[tuple[float, tuple[int, int, int, int], str]] = []

    for restart in range(restarts):
        current_key = random_key_for_length(text_len)
        current_text = decrypt(ciphertext, *current_key)
        current_score = full_text_score(current_text, ngram_score)

        best_local_key = current_key
        best_local_text = current_text
        best_local_score = current_score

        for step in range(iterations_per_restart):
            candidate_key = mutate_key(current_key, text_len)
            candidate_text = decrypt(ciphertext, *candidate_key)
            candidate_score = full_text_score(candidate_text, ngram_score)

            temperature = max(0.001, 2.0 * (1.0 - step / iterations_per_restart))

            if candidate_score > current_score:
                accept = True
            else:
                delta = candidate_score - current_score
                accept_prob = math.exp(delta / temperature)
                accept = random.random() < accept_prob

            if accept:
                current_key = candidate_key
                current_text = candidate_text
                current_score = candidate_score

                if current_score > best_local_score:
                    best_local_key = current_key
                    best_local_text = current_text
                    best_local_score = current_score

        if best_local_score > global_best_score:
            global_best_key = best_local_key
            global_best_text = best_local_text
            global_best_score = best_local_score

        best_candidates.append((best_local_score, best_local_key, best_local_text))
        best_candidates.sort(key=lambda x: x[0], reverse=True)
        best_candidates = best_candidates[:top_k]

        print(
            f"[restart {restart + 1}/{restarts}] "
            f"best_score={best_local_score:.2f} "
            f"key={best_local_key}"
        )

    return global_best_key, global_best_text, global_best_score, best_candidates

# --------------------------------------------------
# 10. Пример корпуса
# --------------------------------------------------
DEFAULT_CORPUS = """
вначалебылословоизадачейкриптоаналитикаявляетсявосстановлениеисходноготекстапошифротексту
статистическиеметодывкриптоанализеопираютсяначастотыбуквбиграммитриграмм
длярусскогоязыкахарактерныопределённыесочетаниясимволовкоторыевстречаютсягораздочащедругих
еслипослерасшифрованияполучаетсятекстсестественнойструктуройвероятностьправильногоключавозрастает
длинныйшифротекстгораздолучшеподходитдлястатистическогоанализачемкороткий
врусскомтекстечастовстречаютсясочетаниястноеноватопринеправильнойрасшифровкетакихсочетанийобычномало
рекуррентныйаффинныйшифринтересентемчтоключивнёмменяютсяотпозициикпозициинонеявляютсяслучайными
онипорождаютсядетерминированнойрекурсиейпоэтомусуществуетструктуракоторуюможнопытатьсявосстановить
"""


# --------------------------------------------------
# 11. Запуск
# --------------------------------------------------
if __name__ == "__main__":
    # Вставь сюда свой шифротекст
    ciphertext = "ЗФЗАЦЗКШЧДЯГВВЬФДЯРДЦУИРЦЛЩЩЭУБЯТЮРЩЩХЫБЭТФЕХЩЪЫЖШНЩЗЭМВЖУЖСЧЕПЩЫЁИЛЩУЗБЗЫШЪАЕССШВКЯФПМВА"

    corpus_text = DEFAULT_CORPUS

    ciphertext = normalize_text(ciphertext)

    if not ciphertext:
        raise ValueError("Шифротекст пустой после нормализации")

    best_key, best_text, best_score, top_candidates = stochastic_search(
        ciphertext=ciphertext,
        corpus_text=corpus_text,
        restarts=80,
        iterations_per_restart=5000,
        seed=12345,
        top_k=10,
    )

    print("\nЛучший найденный ключ:")
    print(best_key)

    print("\nОценка:")
    print(best_score)

    print("\nЛучшая расшифровка:")
    print(best_text)
    print("\nТоп лучших кандидатов:")
    for idx, (score, key, text) in enumerate(top_candidates, start=1):
        print("-" * 70)
        print(f"{idx}. score = {score:.2f}")
        print(f"   key   = {key}")
        print(f"   text  = {text}")