import pymem
import time
from resolver import resolve_pointer_chain


def main():
    pm = pymem.Pymem("popcapgame1.exe")
    module_base = pymem.process.module_from_name(
        pm.process_handle, "popcapgame1.exe").lpBaseOfDll

    pointer_base = module_base + 0x003E3E70
    offsets = [0x18, 0x8, 0x20, 0x18, 0x0, 0x8, 0x5578]

    print(f"Module base: {hex(module_base)}")
    print(f"Pointer base: {hex(pointer_base)}")
    is_64 = pymem.process.is_64_bit(pm.process_handle)
    print(f"Game is 64-bit: {is_64}")
    read_ptr = pm.read_ulonglong if is_64 else pm.read_uint
    try:
        val0 = read_ptr(pointer_base)
        print(f"  [{hex(pointer_base)}] -> {hex(val0)}")
        if val0 != 0:
            val1 = read_ptr(val0 + offsets[0])
            print(f"  [{hex(val0 + offsets[0])}] -> {hex(val1)}")
    except Exception as e:
        print(f"Debug read failed: {e}")

    while True:
        try:
            final_address = resolve_pointer_chain(pm, pointer_base, offsets)
            value = pm.read_int(final_address)
            print("Suns:", value)
            pm.write_int(final_address, int(input("New suns: ")))
        except Exception as e:
            print(f"Waiting for game level... ({e})")
            time.sleep(2)


if __name__ == "__main__":
    main()
