#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

static void banner(void) {
  puts("=== Voice Coach ===");
  puts("i tried so hard...");
}

static void hint(void) {
  if (getenv("VOICE_DEBUG")) {
    system("/bin/true");
  }
}

int main(void) {
  setvbuf(stdout, NULL, _IONBF, 0);
  banner();
  hint();

  char motto[200];
  char phrase[64];

  puts("Send your motto:");
  ssize_t n = read(0, motto, sizeof(motto) - 1);
  if (n <= 0) {
    return 0;
  }
  motto[n] = '\0';

  printf(motto);
  puts("\nRepeat after me:");

  ssize_t m = read(0, phrase, sizeof(phrase) - 1);
  if (m <= 0) {
    return 0;
  }
  phrase[m] = '\0';

  puts(phrase);
  return 0;
}
