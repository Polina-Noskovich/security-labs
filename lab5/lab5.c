#include <stdio.h>
#include <string.h>

void hacked() {
    printf("Ход выполнения программы изменен! Атака удалась!\n");
}

void vulnerable() {
    char buffer[16];  // Переполняемый буфер
    printf("Введите данные: ");
    gets(buffer);  // Уязвимая функция (использует незащищенный ввод)
    printf("Вы ввели: %s\n", buffer);
}

int main() {
    printf("Программа запущена...\n");
    vulnerable();
    printf("Завершение программы.\n");
    return 0;
}
