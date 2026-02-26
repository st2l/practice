CC = gcc
SRC = main.c
BUILD = build
TARGET = chat_ai

CFLAGS = -O0 -fno-stack-protector -fno-omit-frame-pointer -fno-optimize-sibling-calls -fstack-reuse=none -no-pie -fno-pie
LDFLAGS = -no-pie

all: $(BUILD)/$(TARGET)

$(BUILD):
	mkdir -p $(BUILD)

$(BUILD)/$(TARGET): $(SRC) | $(BUILD)
	$(CC) $(CFLAGS) $(SRC) -o $@ $(LDFLAGS)

clean:
	rm -rf $(BUILD)
