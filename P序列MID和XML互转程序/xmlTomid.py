from mido import MidiFile, MidiTrack, Message, MetaMessage
import xml.etree.ElementTree as ET
import sys

# 解析XML
def XML转MID(输入,输出):
    tree = ET.parse(输入)
    root = tree.getroot()

    # 创建MIDI
    # 1 tick = 1 ms, ticks_per_beat = 480
    # tempo = 500000 μs/beat → 1 beat = 480 ms → 125 BPM

    TmpT = 500000
    PbeaT = 480
    
    mid = MidiFile(ticks_per_beat=PbeaT)
    track = MidiTrack()
    mid.tracks.append(track)
    # track.clear()  # 清空自动添加的末轨元事件

    track.append(MetaMessage('set_tempo', tempo=TmpT))
    track.append(MetaMessage('time_signature', numerator=4, denominator=4))

    # 收集所有音符（按Duration排序）
    notes = []
    for chapter in root.findall('chapter'):
        music_num = int(chapter.get('MusicNum'))
        duration_ms = int(chapter.get('Duration'))
        notes.append((duration_ms, music_num))

    notes.sort(key=lambda x: x[0])

    # 生成MIDI事件
    prev_time = 0
    for i, (time_ms, music_num) in enumerate(notes):
        delta = time_ms - prev_time
        # 音符持续到下一个音符（延音踏板效果）
        if i + 1 < len(notes):
            duration = notes[i+1][0] - time_ms
        else:
            duration = 240  # 最后一个音符持续240ms

        dtk = int((delta*1000)/(TmpT/PbeaT))
        dtkd = int((duration*1000)/(TmpT/PbeaT))

        # Message：time是tick
        track.append(Message('note_on', note=music_num, velocity=100, time=0))
        track.append(Message('note_off', note=music_num, velocity=0, time=dtkd))
    
        prev_time = time_ms

    # track.append(MetaMessage('end_of_track'))  # 只保留结束标记
    mid.save(输出)

    print(f'✅ 已生成: fur_elise_from_xml.mid')
    print(f'📊 总时长: {notes[-1][0]} ms = {notes[-1][0]/1000:.1f} 秒')
    print(f'🎵 音符数: {len(notes)}')

def main():
    if len(sys.argv) != 3:
        print("用法: python script.py <输入文件> <输出文件>")
        print("示例: python script.py input.txt output.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    XML转MID(input_file,output_file)

# 程序入口
if __name__ == "__main__":
    main()