def caesar_cipher(text, shift, encrypt=True):
    result = ''
    for char in text:
        if char.isalpha():
            if 'а' <= char <= 'я' or 'А' <= char <= 'Я':
                start = ord('а') if char.islower() else ord('А')
                alphabet_size = 32
            else:
                start = ord('a') if char.islower() else ord('A')
                alphabet_size = 26 
            
            shifted_char = chr((ord(char) - start + (shift if encrypt else -shift)) % alphabet_size + start)
        elif char.isdigit():
            shifted_char = str((int(char) + (shift if encrypt else -shift)) % 10)
        else:
            shifted_char = char  # Не изменяем пробелы и знаки препинания
        result += shifted_char
    return result

def vigenere_cipher(text, key, encrypt=True):
    result = ''
    key_len = len(key)
    key_index = 0
    
    for char in text:
        if char.isalpha():
            if 'а' <= char <= 'я' or 'А' <= char <= 'Я':  
                start = ord('а') if char.islower() else ord('А')
                alphabet_size = 32
            else:  
                start = ord('a') if char.islower() else ord('A')
                alphabet_size = 26
            key_char = key[key_index % key_len].lower()
            if 'а' <= key_char <= 'я':
                shift = ord(key_char) - ord('а')
            else: 
                shift = ord(key_char) - ord('a')
            
            # Для расшифровки мы используем отрицательный сдвиг
            shifted_char = chr((ord(char) - start - (shift if encrypt else -shift)) % alphabet_size + start)
            key_index += 1
        else:
            shifted_char = char  # Не изменяем пробелы и знаки препинания
        result += shifted_char
    return result

def get_valid_choice(prompt, valid_choices):
    while True:
        choice = input(prompt)
        if choice in valid_choices:
            return choice
        else:
            print(f"Ошибка! Введите одно из значений: {', '.join(valid_choices)}")

def get_valid_int_input(prompt):
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Ошибка! Пожалуйста, введите целое число.")

def get_valid_string_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:  # Убедимся, что строка не пустая
            return value
        else:
            print("Ошибка! Пожалуйста, введите не пустую строку.")

def main():
    input_text = get_valid_string_input("Введите текст для обработки: ")

    action_choice = get_valid_choice("Выберите действие (1 - Зашифровать, 2 - Расшифровать): ", ["1", "2"])

    if action_choice == "1":
        cipher_choice = get_valid_choice("Выберите метод шифрования (1 - Цезарь, 2 - Виженер): ", ["1", "2"])

        if cipher_choice == "1":
            key = get_valid_int_input("Введите ключ для шифра Цезаря (целое число): ")
            ciphered_text = caesar_cipher(input_text, key)
            print("\nЗашифрованный текст:   " + ciphered_text + '\n')
        elif cipher_choice == "2":
            key = get_valid_string_input("Введите ключ для шифра Виженера (строка): ")
            ciphered_text = vigenere_cipher(input_text, key)
            print("\nЗашифрованный текст:   " + ciphered_text + '\n')

    elif action_choice == "2":
        cipher_choice = get_valid_choice("Выберите метод расшифрования (1 - Цезарь, 2 - Виженер): ", ["1", "2"])

        if cipher_choice == "1":
            key = get_valid_int_input("Введите ключ для шифра Цезаря (целое число): ")
            deciphered_text = caesar_cipher(input_text, key, encrypt=False)
            print("\nРасшифрованный текст:   " + deciphered_text + '\n')
        elif cipher_choice == "2":
            key = get_valid_string_input("Введите ключ для шифра Виженера (строка): ")
            deciphered_text = vigenere_cipher(input_text, key, encrypt=False)
            print("\nРасшифрованный текст:   " + deciphered_text + '\n')

if __name__ == "__main__":
    main()
