#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>

static const char *CMD = "/bin/sh";

void banner(void) {
  puts("=== Static Support Desk ===");
  puts("We keep everything in-house. Even the libs.");
}

static void leak_token(void) {
  uintptr_t p = (uintptr_t)&banner;
  uintptr_t token = (p ^ 0x5a5aa5a5aa55aa55ULL) + 0x1337;
  printf("Session token: %lx\n", token);
}

static void read_review(void) {
  char buf[128];
  unsigned int n = 0;

  puts("How long is your review? (max 512)");
  if (scanf("%u", &n) != 1) {
    exit(0);
  }
  int c;
  while ((c = getchar()) != '\n' && c != EOF) {
  }

  if (n < 16) {
    puts("Too short. We value details.");
    return;
  }
  if (n > 512) {
    n = 512;
  }

  puts("Write your review:");
  read(0, buf, n);
  puts("Thanks for the feedback.");
}

static void touch_system(void) {
  if (getenv("HELPDESK_DEBUG")) {
    system("/bin/true");
  }
}

int main(void) {
  setvbuf(stdout, NULL, _IONBF, 0);

  touch_system();

  while (1) {
    banner();
    puts("1) Get session token");
    puts("2) Leave a review");
    puts("0) Exit");
    puts("> ");

    int opt = 0;
    if (scanf("%d", &opt) != 1) {
      exit(0);
    }
    int c;
    while ((c = getchar()) != '\n' && c != EOF) {
    }

    if (opt == 0) {
      puts("Bye.");
      break;
    } else if (opt == 1) {
      leak_token();
    } else if (opt == 2) {
      read_review();
    } else {
      puts("Unknown option.");
    }
  }

  return 0;
}
