#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define MAGIC 0xdeadbeefcafebabeULL

__attribute__((naked)) void pop_rdi_ret(void) {
    __asm__("pop %rdi; ret");
}

void win(unsigned long long key) {
    int fd;
    char out[128];
    ssize_t n;

    if (key != MAGIC) {
        puts("Wrong key");
        _exit(1);
    }

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

    puts("ueeee");
    read(0, buf, 256);
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);

    vuln();
    return 0;
}
