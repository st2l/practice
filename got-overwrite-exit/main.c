#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void win(void) {
    system("cat flag.txt");
    _exit(0);
}

int main(void) {
    char name[256];

    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    puts("=== So SOFT and so SQUISHY ===");
    puts("Input your nickname:");

    if (!fgets(name, sizeof(name), stdin)) {
        return 0;
    }

    printf(name);
    puts("\nBye");

    exit(0);
}
