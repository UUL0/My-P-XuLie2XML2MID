from mido import MidiFile, MidiTrack, Message, MetaMessage
import sys

def decode_note(float_val):
    """浮点数 → 整数 → 提取音符信息"""
    encoded_int = int(float_val)
    note_id = (encoded_int >> 17) & 0x7F
    tone = (encoded_int >> 13) & 0xF
    delay = encoded_int & 0x1FFF
    midi_note = note_id + 43
    return midi_note, tone, delay

def encoded_to_mid(encoded_file, output_mid):
    with open(encoded_file, 'r') as f:
        lines = f.readlines()
    
    notes = []
    for line in lines:
        val = float(line.strip())
        midi_note, tone, delay = decode_note(val)
        notes.append((midi_note, tone, delay))
    
    # 创建 MIDI（1 tick = 0.5ms，即 120 BPM）
    TmpT = 500000
    PbeaT = 480

    mid = MidiFile(ticks_per_beat=PbeaT)
    track = MidiTrack()
    mid.tracks.append(track)
    
    # MIDI 头
    track.append(MetaMessage('set_tempo', tempo=TmpT))  # 120 BPM
    track.append(MetaMessage('time_signature', numerator=4, denominator=4))
    
    # 生成音符（累加延时 = 绝对时间）
    current_tick = 0
    for i, (midi_note, tone, delay) in enumerate(notes):
        current_tick += delay

        # 音符开
        track.append(Message('note_on', note=midi_note, velocity=100, time=0))
        
        # 音符关
        if i + 1 < len(notes):
            next_ticks = int((notes[i + 1][2] * 1000) / (TmpT / PbeaT)) # 下一个延时值转为tick
            track.append(Message('note_off', note=midi_note, velocity=0, time=next_ticks))
        else:
            track.append(Message('note_off', note=midi_note, velocity=0, time=480))  # 240ms
    
    mid.save(output_mid)
    print(f'✅ 已生成: {output_mid}')
    print(f'📊 音符数: {len(notes)}')
    print(f'⏱️  时长: {current_tick} ms')



def main():
    if len(sys.argv) != 3:
        print("用法: python script.py <输入文件> <输出文件>")
        print("示例: python script.py input.txt output.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    encoded_to_mid(input_file, output_file)

# 程序入口
if __name__ == "__main__":
    main()