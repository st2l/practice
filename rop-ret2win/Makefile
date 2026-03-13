CC = gcc
SRC = main.c
BUILD = build
TARGET = rop_ret2win

CFLAGS = -O0 -fno-stack-protector -fno-omit-frame-pointer -no-pie
LDFLAGS =

all: $(BUILD)/$(TARGET)

$(BUILD):
	mkdir -p $(BUILD)

$(BUILD)/$(TARGET): $(SRC) | $(BUILD)
	$(CC) $(CFLAGS) $(SRC) -o $@ $(LDFLAGS)

clean:
	rm -rf $(BUILD)
