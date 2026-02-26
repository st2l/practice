#include <stdio.h>
#include <stdlib.h>

char storage[10][64];
int g_count = 0;

int main(int argc, char *argv[]) {
  setvbuf(stdout, NULL, _IONBF, 0);	

  puts("Welcome to our new notes manager!");
  puts("TOTALLY not vulnerable notes manager!");
  puts("If u will find any vulnerability - u will get a flag!!!");

  int idx;
  int option;
  char name[64];
  char *arr[10];

  while (1) {
    puts("Choose option:\n1) Change name\n2) Create note\n3) Edit note\n0) Exit");
    scanf("%d", &option);

    switch (option) {
      case 0:
        goto exit_loop;
        break;

      case 1:
        puts("Enter your name: ");
      	read(0, name, 1000);
        printf("Well... your new name! -> %s", name);
        break;

      case 2:
        if (g_count >= 10) {
          puts("No more notes for you today...");
          goto exit_loop;
        }
        puts("Enter your new note!");
        arr[g_count] = storage[g_count];
        scanf("%63s", arr[g_count]);
        g_count += 1;
        puts("Seccessfully saved!");
        break;

      case 3:
        puts("Enter index of note");
        scanf("%d", &idx);
        puts("Now write new data to your note!");
        scanf("%63s", arr[idx]);
        puts("Nice!");
        break;
    }
  }
exit_loop:
  puts("Bye!");
}
