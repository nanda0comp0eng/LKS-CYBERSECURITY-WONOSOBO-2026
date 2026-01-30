#include <stdio.h>
#include <string.h>
#include <stdlib.h>

// XOR key
#define XOR_KEY 7

// Function to XOR decrypt the flag
void decrypt_flag(unsigned char *encrypted, char *output, int len) {
    for (int i = 0; i < len; i++) {
        output[i] = encrypted[i] ^ XOR_KEY;
    }
    output[len] = '\0';
}

// Function to check if the input matches the flag
int check_flag(char *input) {
    // Encrypted flag: CTF{x0r_1s_n0t_s3cur3_0bfusc4t10n}
    // Each character XORed with key 7
    unsigned char encrypted[] = {
    0x4b, 0x4c, 0x54, 0x50, 0x49, 0x54, 0x45, 0x7c,
    0x7f, 0x68, 0x75, 0x58, 0x6b, 0x66, 0x60, 0x6e,
    0x58, 0x7f, 0x68, 0x75, 0x58, 0x6b, 0x66, 0x60,
    0x6e, 0x7a
};

int flag_len = sizeof(encrypted) / sizeof(encrypted[0]);
    char decrypted[100];
    
    // Decrypt the flag in memory
    decrypt_flag(encrypted, decrypted, flag_len);
    
    // Compare with user input
    if (strcmp(input, decrypted) == 0) {
        return 1;
    }
    
    return 0;
}

// Decoy function with fake operations
void decoy_check_1(char *input) {
    char fake[] = "flag{fake}";
    if (strlen(input) > 5) {
        printf("nooooo its fakeeee\n");
    }
}

// Another decoy function
void decoy_check_2(char *input) {
    char fake[] = "password123";
    if (input[0] == 'C') {
        printf("palsu lagi wkkakwkawk...\n");
    }
}

int main() {
    char input[100];
    
    printf("========================================\n");
    printf("         Reverse Engineering\n");
    printf("           CTF Challenge\n");
    printf("========================================\n");
    printf("\n");
    printf("This challenge requires actual reversing!\n");
    printf("\n");
    printf("Enter the flag: ");
    
    if (fgets(input, sizeof(input), stdin) != NULL) {
        // Remove newline
        input[strcspn(input, "\n")] = 0;
        
        // Run decoy checks
        decoy_check_1(input);
        decoy_check_2(input);
        
        // Check the actual flag
        if (check_flag(input)) {
            printf("\n");
            printf("========================================\n");
            printf("   CORRECT! KAMU NEMU FLAG ASLINYA!\n");
            printf("========================================\n");
            printf("\n");
            printf("Great job reverse engineering!\n");
            return 0;
        } else {
            printf("\nIncorrect flag. Keep reversing!\n");
            return 1;
        }
    }
    
    return 1;
}
