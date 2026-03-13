#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

static void banner(void) {
    puts("=== mymyymymmmmymymmymymymmymymym ===");
}

void win(void) {
    int fd;
    char out[128];
    ssize_t n;

    fd = open("flag.txt", O_RDONLY);
    if (fd < 0) {
        puts("flag not found");
        _exit(1);
    }

    n = read(fd, out, sizeof(out));
    if (n > 0) {
        write(1, out, (size_t)n);
    }
    close(fd);
    _exit(0);
}

void vuln(void) {
    char buf[64];

    puts("Send your payload:");
    read(0, buf, 256);
    puts("Thanks!");
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    banner();
    vuln();
    return 0;
}
