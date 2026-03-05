#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

static void banner(void) {
  puts("=== Helpdesk (Legacy) ===");
  puts("We still accept handwritten notes.");
}

static void leave_note(void) {
  char note[96];
  puts("Your temporary clipboard is ready.");
  printf("Clipboard address: %p\n", (void *)note);
  puts("Write your note:");
  read(0, note, 300);
  puts("Stored. We'll review it soon.");
}

int main(void) {
  setvbuf(stdout, NULL, _IONBF, 0);
  banner();
  leave_note();
  puts("Bye.");
  return 0;
}
