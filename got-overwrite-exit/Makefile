CC = gcc
SRC = main.c
BUILD = build
TARGET = got_overwrite_exit

CFLAGS = -O0 -fno-stack-protector -fno-omit-frame-pointer -no-pie
LDFLAGS = -Wl,-z,norelro

all: $(BUILD)/$(TARGET)

$(BUILD):
	mkdir -p $(BUILD)

$(BUILD)/$(TARGET): $(SRC) | $(BUILD)
	$(CC) $(CFLAGS) $(SRC) -o $@ $(LDFLAGS)

clean:
	rm -rf $(BUILD)
