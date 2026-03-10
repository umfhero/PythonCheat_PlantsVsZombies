import pymem
from resolver import resolve_pointer_chain



def main():
    module_base = pymem.process.module_from_name(pm.process_handle, "popcapgame1.exe").lpBaseOfDll

    pointer_base = module_base + 0x0011BC8C
    offsets = [0x138, 0x40, 0x1758, 0x24, 0x15C, 0x16C, 0x5578]

    while True:
        try:
            final_address = resolve_pointer_chain(pm, pointer_base, offsets)
            value = pm.read_int(final_address)
            print("Suns:", value)
            pm.write_int(final_address, int(input("New suns: ")))
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()


