#include <stdio.h>
#include <string.h>
#include <windows.h>

#define BUFFER_SIZE 10

void malicious_behavior(int threat_level) {
    printf("\n[!!!] Вредоносное поведение активировано!\n");
    printf("[!!!] Уровень угрозы: %d\n", threat_level);

    if (threat_level > 100) {
        printf("[!!!] Критическая угроза! Система заражена!\n");
        printf("[!!!] Имитация удаления файлов...\n");
        printf("[!!!] Файлы успешно удалены! (шутка)\n");
    } else if (threat_level > 10) {
        printf("[!!!] Высокий уровень угрозы! Система в опасности!\n");
    } else {
        printf("[!!!] Угроза обнаружена, но уровень низкий.\n");
    }
}

void vulnerable_copy(const char *input) {
    char buffer[BUFFER_SIZE];
    int critical_variable = 10;  

    printf("\n[!] Используется уязвимый метод (strcpy)...\n");
    printf("Значение critical_variable до переполнения: %d (нормальный статус)\n", critical_variable);

    strcpy(buffer, input);

    printf("Результат (буфер): %s\n", buffer);
    printf("Значение critical_variable после переполнения: %d\n", critical_variable);

    if (critical_variable != 10) {
        printf("\n[!] Обнаружено переполнение буфера!\n");
        malicious_behavior(critical_variable); 
    } else {
        printf("\n[+] Переполнение не произошло. Система в безопасности.\n");
    }
}

void safe_copy(const char *input) {
    char buffer[BUFFER_SIZE];
    int critical_variable = 10; 

    printf("\n[+] Используется защищённый метод (strncpy)...\n");
    printf("Значение critical_variable до копирования: %d (нормальный статус)\n", critical_variable);

    strncpy(buffer, input, BUFFER_SIZE - 1);
    buffer[BUFFER_SIZE - 1] = '\0';

    printf("Результат (буфер): %s\n", buffer);
    printf("Значение critical_variable после копирования: %d\n", critical_variable);

    if (critical_variable != 9) {
        printf("\n[!] Ошибка: critical_variable изменён, но переполнения не должно было быть!\n");
    } else {
        printf("\n[+] Система в безопасности. Переполнение предотвращено.\n");
    }
}

int main() {

    SetConsoleOutputCP(65001);

    char input[100];
    int mode;

    printf("Выберите режим тестирования:\n1 - Уязвимый режим\n2 - Защищённый режим\n");
    scanf("%d", &mode);
    getchar();

    printf("Введите строку для тестирования: ");
    fgets(input, sizeof(input), stdin);

    input[strcspn(input, "\n")] = 0;

    if (mode == 1) {
        vulnerable_copy(input);
    } else if (mode == 2) {
        safe_copy(input);
    } else {
        printf("Неверный режим. Пожалуйста, выберите 1 или 2.\n");
    }

    return 0;
}