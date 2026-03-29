# Шифр простой замены

ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"


def normalize_text(text: str) -> str:
    """
    Переводит текст в верхний регистр.
    """
    return text.upper()


def validate_key(key: str) -> str:
    """
    Проверяет, что ключ:
    1) имеет ту же длину, что и алфавит;
    2) содержит все буквы алфавита ровно по одному разу.
    """
    key = normalize_text(key)

    if len(key) != len(ALPHABET):
        raise ValueError(
            f"Ключ должен содержать ровно {len(ALPHABET)} символа(ов)."
        )

    if sorted(key) != sorted(ALPHABET):
        raise ValueError(
            "Ключ должен быть перестановкой русского алфавита."
        )

    return key


def encrypt(text: str, key: str) -> str:
    """
    Шифрование шифром простой замены.
    Каждая буква исходного алфавита заменяется на букву из ключа с тем же индексом.
    """
    text = normalize_text(text)
    key = validate_key(key)

    result = []

    for ch in text:
        if ch in ALPHABET:
            index = ALPHABET.index(ch)
            result.append(key[index])
        else:
            # Символы вне алфавита оставляем без изменений
            result.append(ch)

    return "".join(result)


def decrypt(text: str, key: str) -> str:
    """
    Расшифрование шифра простой замены.
    Для каждой буквы шифртекста ищем её позицию в ключе
    и по этой позиции берём букву из исходного алфавита.
    """
    text = normalize_text(text)
    key = validate_key(key)

    result = []

    for ch in text:
        if ch in ALPHABET:
            index = key.index(ch)
            result.append(ALPHABET[index])
        else:
            # Символы вне алфавита оставляем без изменений
            result.append(ch)

    return "".join(result)


def main():
    print("Шифр простой замены")
    print(f"Алфавит:\n{ALPHABET}\n")

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
        print("\nВведите ключ.")
        print("Ключ должен быть полной перестановкой алфавита.")
        print("Пример структуры ключа: все 33 буквы, каждая ровно 1 раз.")
        key = input("Введите ключ: ")

        try:
            if choice == "1":
                result = encrypt(text, key)
                print("\nЗашифрованный текст:")
                print(result)
            else:
                result = decrypt(text, key)
                print("\nРасшифрованный текст:")
                print(result)

        except ValueError as e:
            print("\nОшибка:", e)


if __name__ == "__main__":
    main()