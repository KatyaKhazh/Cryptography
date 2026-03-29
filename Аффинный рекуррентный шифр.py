from math import gcd

#Аффинный рекуррентный шифр
ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
M = len(ALPHABET)  # 33


def normalize_text(text: str) -> str:
    """
    Переводит текст в верхний регистр.
    """
    return text.upper()


def char_to_index(ch: str) -> int:
    """
    Возвращает индекс буквы в алфавите.
    """
    return ALPHABET.index(ch)


def index_to_char(index: int) -> str:
    """
    Возвращает букву по индексу.
    """
    return ALPHABET[index]


def extended_gcd(a: int, b: int):
    """
    Расширенный алгоритм Евклида.
    Возвращает (g, x, y), где:
    g = gcd(a, b)
    a*x + b*y = g
    """
    if a == 0:
        return b, 0, 1

    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y


def mod_inverse(a: int, m: int) -> int:
    """
    Находит обратный элемент a^(-1) по модулю m.
    """
    g, x, _ = extended_gcd(a, m)

    if g != 1:
        raise ValueError(
            f"Обратного элемента для a = {a} по модулю {m} не существует."
        )

    return x % m


def validate_single_key(a: int, b: int):
    """
    Проверка одного аффинного ключа (a, b).
    """
    if gcd(a, M) != 1:
        raise ValueError(
            f"Некорректный параметр a = {a}: gcd({a}, {M}) != 1."
        )

    if not (0 <= b < M):
        raise ValueError(
            f"Параметр b = {b} должен быть в диапазоне от 0 до {M - 1}."
        )


def validate_initial_keys(a1: int, b1: int, a2: int, b2: int):
    """
    Проверка двух начальных ключей.
    """
    validate_single_key(a1, b1)
    validate_single_key(a2, b2)


def generate_recurrent_keys(length: int, a1: int, b1: int, a2: int, b2: int):
    """
    Генерирует последовательность ключей длины length.

    k1 = (a1, b1)
    k2 = (a2, b2)
    далее:
    a_i = (a_{i-1} * a_{i-2}) mod M
    b_i = (b_{i-1} + b_{i-2}) mod M
    """
    validate_initial_keys(a1, b1, a2, b2)

    if length <= 0:
        return []

    if length == 1:
        return [(a1, b1)]

    keys = [(a1, b1), (a2, b2)]

    for i in range(2, length):
        prev_a1, prev_b1 = keys[i - 1]
        prev_a2, prev_b2 = keys[i - 2]

        new_a = (prev_a1 * prev_a2) % M
        new_b = (prev_b1 + prev_b2) % M

        # Для расшифрования необходимо, чтобы у каждого new_a существовал обратный элемент.
        if gcd(new_a, M) != 1:
            raise ValueError(
                f"На шаге {i + 1} получен коэффициент a = {new_a}, "
                f"для которого не существует обратного элемента по модулю {M}. "
                f"Выберите другие начальные ключи."
            )

        keys.append((new_a, new_b))

    return keys


def encrypt(text: str, a1: int, b1: int, a2: int, b2: int) -> str:
    """
    Шифрование аффинным рекуррентным шифром.
    """
    text = normalize_text(text)

    # Собираем только буквы алфавита, чтобы понять,сколько реально ключей нужно сгенерировать.
    letters = [ch for ch in text if ch in ALPHABET]
    keys = generate_recurrent_keys(len(letters), a1, b1, a2, b2)

    result = []
    pos = 0

    for ch in text:
        if ch in ALPHABET:
            a, b = keys[pos]
            x = char_to_index(ch)
            y = (a * x + b) % M
            result.append(index_to_char(y))
            pos += 1
        else:
            # Неалфавитные символы оставляем без изменений
            result.append(ch)

    return "".join(result)


def decrypt(text: str, a1: int, b1: int, a2: int, b2: int) -> str:
    """
    Расшифрование аффинного рекуррентного шифра.
    """
    text = normalize_text(text)

    letters = [ch for ch in text if ch in ALPHABET]
    keys = generate_recurrent_keys(len(letters), a1, b1, a2, b2)

    result = []
    pos = 0

    for ch in text:
        if ch in ALPHABET:
            a, b = keys[pos]
            a_inv = mod_inverse(a, M)
            y = char_to_index(ch)
            x = (a_inv * (y - b)) % M
            result.append(index_to_char(x))
            pos += 1
        else:
            # Неалфавитные символы оставляем без изменений
            result.append(ch)

    return "".join(result)
def print_valid_a_values():
    """
    Показывает допустимые значения a для m = 33.
    """
    valid_values = [a for a in range(M) if gcd(a, M) == 1]
    print("Допустимые значения a для русского алфавита:")
    print(valid_values)


def print_menu():
    print("\nВыберите действие:")
    print("1 - зашифровать текст")
    print("2 - расшифровать текст")
    print("0 - выход")


def main():
    print("Аффинный рекуррентный шифр")
    print(f"Алфавит:\n{ALPHABET}")
    print(f"Размер алфавита m = {M}")
    print_valid_a_values()

    while True:
        print_menu()
        choice = input("Введите номер действия: ").strip()

        if choice == "0":
            print("Программа завершена.")
            break

        if choice not in ("1", "2"):
            print("Ошибка: нужно ввести 1, 2 или 0.")
            continue

        try:
            a1 = int(input("Введите a1: "))
            b1 = int(input("Введите b1: "))
            a2 = int(input("Введите a2: "))
            b2 = int(input("Введите b2: "))

            text = input("Введите текст: ")

            if choice == "1":
                result = encrypt(text, a1, b1, a2, b2)
                print("\nЗашифрованный текст:")
                print(result)
            else:
                result = decrypt(text, a1, b1, a2, b2)
                print("\nРасшифрованный текст:")
                print(result)

        except ValueError as e:
            print("\nОшибка:", e)


if __name__ == "__main__":
    main()