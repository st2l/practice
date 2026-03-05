CC = gcc
SRC = main.c
BUILD = build
TARGET = static_support

CFLAGS = -O0 -fno-stack-protector -fno-omit-frame-pointer -fno-optimize-sibling-calls -fstack-reuse=none -fPIE
LDFLAGS = -static -pie

all: $(BUILD)/$(TARGET)

$(BUILD):
	mkdir -p $(BUILD)

$(BUILD)/$(TARGET): $(SRC) | $(BUILD)
	$(CC) $(CFLAGS) $(SRC) -o $@ $(LDFLAGS)

clean:
	rm -rf $(BUILD)
