import sys

def encode_p_sequence(note, tune, time_ms):
    value = (note << 17) | (tune << 13) | (time_ms & 0x1FFF)
    return float(value)

def main():
    if len(sys.argv) != 3:
        print("用法: python encode.py <输入文件> <输出文件>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as fin, open(sys.argv[2], 'w') as fout:
        for line in fin:
            if line.strip():
                parts = line.strip().split()
                if len(parts) == 3:
                    note = int(parts[0])
                    tune = int(parts[1])
                    time_ms = int(parts[2])
                    value = encode_p_sequence(note, tune, time_ms)
                    fout.write(f"{value}\n")

if __name__ == "__main__":
    main()
