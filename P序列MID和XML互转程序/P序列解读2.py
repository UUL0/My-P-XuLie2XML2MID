import sys

def decode_p_sequence(line):
    value = int(float(line.strip())) & 0xFFFFFF
    
    note   = (value >> 17) & 0x7F      # bit 23~17
    tune   = (value >> 13) & 0xF       # bit 16~13
    time_ms = value & 0x1FFF           # bit 12~0
    
    return note, tune, time_ms

def main():
    if len(sys.argv) != 3:
        print("用法: python decode.py <输入文件> <输出文件>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as fin, open(sys.argv[2], 'w') as fout:
        for line in fin:
            if line.strip():
                note, tune, time_ms = decode_p_sequence(line)
                fout.write(f"{note} {tune} {time_ms}\n")

if __name__ == "__main__":
    main()
