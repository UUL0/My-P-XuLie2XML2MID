import xml.etree.ElementTree as ET
import sys

def encode_note(midi_note, tone, delay_ms):
    note_id = midi_note - 43 # 偏移
    if delay_ms>8191:
        delay_ms=8191
    if delay_ms<0:
        delay_ms=0
    encoded_int = (note_id << 17) | (tone << 13) | (delay_ms)
    return float(encoded_int)

def XML转P序列(输入, 输出):
    tree = ET.parse(输入)
    root = tree.getroot()

    # 收集有效音符
    chapters = []
    for chapter in root.findall('chapter'):
        music_num = int(chapter.get('MusicNum'))
        duration_ms = int(chapter.get('Duration'))
        if 44 <= music_num <= 90:  # 只收集有效音符
            chapters.append((duration_ms, music_num))

    chapters.sort(key=lambda x: x[0])

    # 延时值 = 当前Duration - 上一个有效音符的Duration（绝对时间）
    encoded_notes = []
    prev_duration = 0

    for duration_ms, music_num in chapters:
        delay = duration_ms - prev_duration  # 绝对时间差
        val = encode_note(music_num, 4, delay)
        encoded_notes.append(val)
        prev_duration = duration_ms  # 只在有效音符时更新

    with open(输出, 'w') as f:
        for val in encoded_notes:
            f.write(f'{val}\n')

    print(f'✅ 已生成: ',输出)
    print(f'📊 有效音符数: {len(encoded_notes)}')

def main():
    if len(sys.argv) != 3:
        print("用法: python script.py <输入文件> <输出文件>")
        print("示例: python script.py input.txt output.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    XML转P序列(input_file,output_file)

# 程序入口
if __name__ == "__main__":
    main()