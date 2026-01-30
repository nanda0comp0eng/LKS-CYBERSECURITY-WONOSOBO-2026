#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// Some decoy functions to make it look harder
void decoy_function_1() {
    char fake[] = "flag{this_is_not_the_flag}";
    printf("Checking authentication...\n");
}

void decoy_function_2() {
    char fake[] = "CTF{fake_flag_123}";
    printf("Verifying credentials...\n");
}

void decoy_function_3() {
    char fake[] = "password123";
    printf("Processing input...\n");
}

static const char part1[] = "LKSWNSB{str1ngs_4re_";
static const char part2[] = "y0ur_fr13nd}";

int main() {
    char input[100];

    /* gabungkan flag saat runtime */
    char secret[64];
    strcpy(secret, part1);
    strcat(secret, part2);

    printf("===================================\n");
    printf("  Welcome to Reverse CTF!\n");
    printf("===================================\n");
    printf("\n");
    printf("Can you find the flag?\n");
    printf("Hint: Sometimes the answer is right in front of you...\n");
    printf("\n");
    printf("Enter the flag: ");

    if (fgets(input, sizeof(input), stdin) != NULL) {
        // Remove newline
        input[strcspn(input, "\n")] = 0;

        if (strcmp(input, secret) == 0) {
            printf("\n Congratulations! You found the flag!\n");
            return 0;
        } else {
            printf("\n Wrong flag! Try again.\n");
            return 1;
        }
    }

    return 1;
}
