from math import gcd

# Аффинный шифр

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
    Например:
    А -> 0
    Б -> 1
    ...
    Я -> 32
    """
    return ALPHABET.index(ch)


def index_to_char(index: int) -> str:
    """
    Возвращает букву алфавита по индексу.
    """
    return ALPHABET[index]


def extended_gcd(a: int, b: int):
    """
    Расширенный алгоритм Евклида.
    Возвращает тройку (g, x, y), где:
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
    Он существует только если gcd(a, m) = 1.
    """
    g, x, _ = extended_gcd(a, m)

    if g != 1:
        raise ValueError(
            f"Обратного элемента для a = {a} по модулю {m} не существует."
        )

    return x % m


def validate_key(a: int, b: int):
    """
    Проверяет корректность ключа.
    Для аффинного шифра обязательно:
    gcd(a, M) = 1
    """
    if gcd(a, M) != 1:
        raise ValueError(
            f"Ключ некорректен: gcd({a}, {M}) != 1.\n"
            f"Для русского алфавита с Ё (m = {M}) параметр a должен быть взаимно прост с {M}."
        )

    if not (0 <= b < M):
        raise ValueError(
            f"Параметр b должен быть в диапазоне от 0 до {M - 1}."
        )


def encrypt(text: str, a: int, b: int) -> str:
    """
    Шифрование аффинным шифром:
    y = (a*x + b) mod M
    """
    validate_key(a, b)
    text = normalize_text(text)

    result = []

    for ch in text:
        if ch in ALPHABET:
            x = char_to_index(ch)
            y = (a * x + b) % M
            result.append(index_to_char(y))
        else:
            # Неалфавитные символы оставляем без изменений
            result.append(ch)

    return "".join(result)


def decrypt(text: str, a: int, b: int) -> str:
    """
    Расшифрование аффинного шифра:
    x = a^(-1) * (y - b) mod M
    """
    validate_key(a, b)
    text = normalize_text(text)

    a_inv = mod_inverse(a, M)
    result = []

    for ch in text:
        if ch in ALPHABET:
            y = char_to_index(ch)
            x = (a_inv * (y - b)) % M
            result.append(index_to_char(x))
        else:
            # Неалфавитные символы оставляем без изменений
            result.append(ch)

    return "".join(result)


def print_valid_a_values():
    """
    Показывает значения a, которые подходят для m = 33.
    """
    valid_values = [a for a in range(M) if gcd(a, M) == 1]
    print("Допустимые значения a для данного алфавита:")
    print(valid_values)


def main():
    print("Аффинный шифр")
    print("Русский алфавит с буквой Ё")
    print(f"Алфавит:\n{ALPHABET}")
    print(f"Размер алфавита m = {M}")
    print_valid_a_values()

    while True:
        print("\nВыберите действие:")
        print("1 - зашифровать текст")
        print("2 - расшифровать текст")
        print("0 - выход")

        choice = input("Введите номер действия: ").strip()

        if choice == "0":
            print("Программа завершена.")
            break

        if choice not in ("1", "2"):
            print("Ошибка: нужно ввести 1, 2 или 0.")
            continue

        text = input("Введите текст: ")

        try:
            a = int(input("Введите параметр a: "))
            b = int(input("Введите параметр b: "))

            if choice == "1":
                result = encrypt(text, a, b)
                print("\nЗашифрованный текст:")
                print(result)
            else:
                result = decrypt(text, a, b)
                print("\nРасшифрованный текст:")
                print(result)

        except ValueError as e:
            print("\nОшибка:", e)


if __name__ == "__main__":
    main()