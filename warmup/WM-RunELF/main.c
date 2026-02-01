#include <stdio.h>
#include <string.h>

int main() {
    char input[64];

    printf("=============================================================\n");
    printf("  SELAMAT DATANG PESERTA LKS CYBER SECURITY KAB. WONOSOBO\n");
    printf("             INTI DARI CTF ITU HAVE FUN\n");
    printf("           JADI SILAHKAN ENJOY SAJA YAHHH\n");
    printf("             inputkan key ini 'LKSWNSB'\n");
    printf("=============================================================\n");
    printf("Enter key: ");
    fgets(input, sizeof(input), stdin);

    // remove newline
    input[strcspn(input, "\n")] = 0;

    if (strcmp(input, "LKSWNSB") == 0) {
        puts("Correct!");
        puts("Flag: LKSWNSB{ELF_f1le_e4sy_t0_run}");
    } else {
        puts("Wrong key!");
    }

    return 0;
}
