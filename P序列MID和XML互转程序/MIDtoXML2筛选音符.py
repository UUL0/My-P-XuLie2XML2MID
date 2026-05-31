import mido
from mido import MidiFile
import sys

def mid_to_xml(mid_path, output_path):
    mid = MidiFile(mid_path)
    tempo = 500000  # 默认tempo：500000微秒/拍 = 120BPM

    notes = []
    abs_tick = 0

    tpb = mid.ticks_per_beat # 
    
    # 微秒/拍msg.tempo，bpm
    # mid.ticks_per_beat每拍的tick数，意思是说每bpm时间多少个tick，例如120bpm=500毫秒=500000微秒一拍
    # msg.time tick，则每tick时间=(tempo/ticks_per_beat)微秒
    # tick换算为毫秒=（(tempo/ticks_per_beat）* tick)/1000
    # 毫秒换算为tick，基准节拍=120bpm=500000微秒/拍，每拍的ticks_per_beat=480，tick=(毫秒*1000)/（tempo/ticks_per_beat）
    # 或tick2second或second2tick 
    

    for track in mid.tracks:
        abs_tick = 0  # 每个轨道独立
        on_time = [-1] * 128      # A数组：note_on 的时间
        on_velocity = [-1] * 128   # B数组：note_on 的力度

        for msg in track:
            abs_tick += msg.time
            dms = int(((tempo/tpb)*abs_tick)/1000)
        
            if msg.type == 'set_tempo':
                tempo = msg.tempo
            elif msg.type == 'note_on' and msg.velocity > 0:
                # notes.append({'tick': dms, 'note': msg.note})
                note_idx = msg.note
                on_time[note_idx] = dms          # 存入时间
                on_velocity[note_idx] = msg.velocity  # 存入力度

            elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                note_idx = msg.note
                if on_time[note_idx] >= 0:  #  确保有对应的 note_on
                    duration = dms - on_time[note_idx]  # 实际时长
                    velocity = on_velocity[note_idx]     #  实际力度

                    #  筛选：时长<N ms 且 力度n~N→ 跳过
                    if duration < 25 or 1 <= velocity <= 5:
                        pass  # ❌ 不加入
                    else:
                        notes.append({
                            'tick': on_time[note_idx],
                            'note': note_idx,
                            'velocity': velocity,
                            'duration': duration
                        })
                
                    on_time[note_idx] = -1  #  重置，准备下一个音符
                    on_velocity[note_idx] = -1

    # 按时间排序
    notes.sort(key=lambda x: x['tick'])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write('<root version="1">\n')
        for i, note in enumerate(notes, 1):
            f.write(f'  <chapter id="{i}" MusicNum="{note["note"]}" Duration="{note["tick"]}" TileMode="100" Space="0"/>\n')
        f.write('</root>')

# 使用：
# mid_to_xml('your_file.mid', 'output.xml')
def main():
    if len(sys.argv) != 3:
        print("用法: python script.py <输入文件> <输出文件>")
        sys.exit(1)
    mid_to_xml(sys.argv[1], sys.argv[2])

if __name__ == "__main__":
    main()	