#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>

#define MAX_NOTES 8
#define MAX_SIZE 0x800

typedef struct {
  char *data;
  size_t size;
  int inuse;
} note_t;

static void say(char *s) { puts(s); }

static struct __attribute__((aligned(0x10))) {
  char pad1[0x80];
  void (*fn)(char *);
  char pad2[0x80];
} hooks = {.fn = say};

note_t notes[MAX_NOTES];

static void win(char *ignored) {
  (void)ignored;
  system("cat flag.txt");
}

static int read_int(void) {
  int v = 0;
  if (scanf("%d", &v) != 1) {
    exit(0);
  }
  int c;
  while ((c = getchar()) != '\n' && c != EOF) {
  }
  return v;
}

static size_t read_size(void) {
  size_t v = 0;
  if (scanf("%zu", &v) != 1) {
    exit(0);
  }
  int c;
  while ((c = getchar()) != '\n' && c != EOF) {
  }
  return v;
}

static void hexdump(const unsigned char *p, size_t n) {
  for (size_t i = 0; i < n; i++) {
    printf("%02x ", p[i]);
  }
  puts("");
}

static void menu(void) {
  puts("\n=== Heap Notes ===");
  puts("1) Create note");
  puts("2) Edit note");
  puts("3) Dump note bytes");
  puts("4) Delete note");
  puts("5) List notes");
  puts("6) Speak note");
  puts("0) Exit");
  puts("> ");
}

static int pick_index(void) {
  puts("Index:");
  int idx = read_int();
  if (idx < 0 || idx >= MAX_NOTES) {
    puts("Bad index.");
    return -1;
  }
  return idx;
}

static void create_note(void) {
  int idx = pick_index();
  if (idx < 0) {
    return;
  }

  puts("Size:");
  size_t sz = read_size();
  if (sz == 0 || sz > MAX_SIZE) {
    puts("Bad size.");
    return;
  }

  notes[idx].data = malloc(sz);
  notes[idx].size = sz;
  notes[idx].inuse = 1;

  puts("Fill now? (y/n)");
  char ans = getchar();
  int c;
  while ((c = getchar()) != '\n' && c != EOF) {
  }
  if (ans == 'y' || ans == 'Y') {
    puts("Data:");
    read(0, notes[idx].data, sz);
  } else {
    puts("Left as-is.");
  }
}

static void edit_note(void) {
  int idx = pick_index();
  if (idx < 0) {
    return;
  }
  if (!notes[idx].data) {
    puts("Empty slot.");
    return;
  }
  puts("Data:");
  read(0, notes[idx].data, notes[idx].size);
}

static void dump_note(void) {
  int idx = pick_index();
  if (idx < 0) {
    return;
  }
  if (!notes[idx].data) {
    puts("Empty slot.");
    return;
  }
  size_t n = notes[idx].size < 32 ? notes[idx].size : 32;
  hexdump((unsigned char *)notes[idx].data, n);
}

static void delete_note(void) {
  int idx = pick_index();
  if (idx < 0) {
    return;
  }
  if (!notes[idx].data) {
    puts("Empty slot.");
    return;
  }
  free(notes[idx].data);
  notes[idx].inuse = 0;
  puts("Deleted.");
}

static void list_notes(void) {
  for (int i = 0; i < MAX_NOTES; i++) {
    printf("[%d] ptr=%p size=%zu inuse=%d\n", i, notes[i].data,
           notes[i].size, notes[i].inuse);
  }
}

static void speak_note(void) {
  int idx = pick_index();
  if (idx < 0) {
    return;
  }
  if (!notes[idx].data) {
    puts("Empty slot.");
    return;
  }
  hooks.fn(notes[idx].data);
}

int main(void) {
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stdin, NULL, _IONBF, 0);

  while (1) {
    menu();
    int opt = read_int();
    switch (opt) {
      case 1:
        create_note();
        break;
      case 2:
        edit_note();
        break;
      case 3:
        dump_note();
        break;
      case 4:
        delete_note();
        break;
      case 5:
        list_notes();
        break;
      case 6:
        speak_note();
        break;
      case 0:
        puts("Bye.");
        return 0;
      default:
        puts("Unknown option.");
        break;
    }
  }
}
