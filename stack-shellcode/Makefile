CC = gcc
SRC = main.c
BUILD = build
TARGET = legacy_helpdesk

CFLAGS = -O0 -fno-stack-protector -fno-omit-frame-pointer -fno-optimize-sibling-calls -fstack-reuse=none -no-pie -fno-pie -z execstack
LDFLAGS = -no-pie -z execstack

all: $(BUILD)/$(TARGET)

$(BUILD):
	mkdir -p $(BUILD)

$(BUILD)/$(TARGET): $(SRC) | $(BUILD)
	$(CC) $(CFLAGS) $(SRC) -o $@ $(LDFLAGS)

clean:
	rm -rf $(BUILD)
