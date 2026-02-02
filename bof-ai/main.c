#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

const char *BAD_LIST[] = {
    "AAAAAAA", "BBBBBBBBBBBB", "%s",     "%x%x%x%x", "%p%p%p",
    "%n",      "../../../",    "A%pB%p", "%%%%%%%%", NULL};

int check_bad_payload(char *s) {
  for (size_t i = 0; BAD_LIST[i]; ++i) {
    if (strstr(s, BAD_LIST[i])) {
      return 1;
    }
  }
  for (size_t i = 0; i < 265; i++) {
    if (!((s[i] >= 'A' && s[i] <= 'Z') || (s[i] >= 'a' && s[i] <= 'z') ||
          (s[i] == '\n'))) {
      return 1;
    }
  }
  return 0;
}

int junk() { puts("its junk bro..."); }
int junk1() { puts("its junk bro..."); }
int junk2() { puts("its junk bro..."); }
int junk3() { puts("its junk bro..."); }
int junk4() { puts("its junk bro..."); }
int junk5() { puts("its junk bro..."); }
int junk6() { puts("its junk bro..."); }
int junk7() { puts("its junk bro..."); }

int instance(int check_ai);

void m() { instance(1); }

int instance(int check_ai) {

  puts("Hello! I am bof AI assistant. I can do some things if u ask me.");
  puts("> ");

  char inp[256];
  read(0, inp, 265);

  if (check_ai == 1 && check_bad_payload(inp)) {
    puts("BAD PAYLOAD DETECTED - ATTEMPTED HACKING!!! CALLING S.W.A.T. TEAM!");
    exit(0);
  }
}

void win() { system("cat flag.txt"); }

int main() { m(); }
