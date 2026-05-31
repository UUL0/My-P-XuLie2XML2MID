import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='对指定列的数值进行乘法运算')
    parser.add_argument('file', help='输入文件路径')
    parser.add_argument('-c', '--column', type=int, required=True, help='指定列（从1开始计数）')
    parser.add_argument('-s', '--separator', default=' ', help='分隔符，默认空格')
    parser.add_argument('-m', '--multiplier', type=float, required=True, help='乘数')
    parser.add_argument('-o', '--output', help='输出文件路径，默认打印到控制台')

    args = parser.parse_args()

    try:
        with open(args.file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"错误：找不到文件 {args.file}")
        sys.exit(1)

    col_idx = args.column - 1  # 转换为0-based索引
    results = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        parts = line.split(args.separator)
        if len(parts) <= col_idx:
            print(f"警告：行 '{line}' 列数不足，跳过")
            continue
        try:
            value = float(parts[col_idx])
            new_value = int(value * args.multiplier)
            parts[col_idx] = str(new_value)
            results.append(args.separator.join(parts))
        except ValueError:
            print(f"警告：行 '{line}' 第{args.column}列不是数值，跳过")
            results.append(line)

    output = '\n'.join(results)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"结果已写入 {args.output}")
    else:
        print(output)

if __name__ == '__main__':
    main()
