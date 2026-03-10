import pymem
from typing import Iterable 

def resolve_pointer_chain(
    pm: pymem.Pymem,
    start_addr: int,
    offsets: Iterable[int],
    *,
    final_add_only: bool = True,
) -> int:
    is_64 = pymem.process.is_64_bit(pm.process_handle)
    read_ptr = pm.read_ulonglong if is_64 else pm.read_uint

    addr = read_ptr(start_addr)
    offs = list(offsets)

    for off in offs[:-1]:
        addr = read_ptr(addr + off)
    
    if not offs:
        return start_addr
    
    last = offs[-1]
    return addr + last if final_add_only else read_ptr(addr + last)