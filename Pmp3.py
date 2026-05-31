import time
import ctypes
import os
import sys

def set_title(text):  
    ctypes.windll.kernel32.SetConsoleTitleW(text)  

winmm = ctypes.windll.winmm

def play_async(mp3_path):
    alias = f"n{int(time.time() * 10000000)}"
    winmm.mciSendStringW(f'open "{mp3_path}" alias {alias}', None, 0, None)
    winmm.mciSendStringW(f'play {alias}', None, 0, None)

def warmup_winmm():
    """预热 winmm，避免第一次调用延迟"""
    alias = "warmup"
    winmm.mciSendStringW(f'open new type waveaudio alias {alias}', None, 0, None)
    winmm.mciSendStringW(f'close {alias}', None, 0, None)

def decode_and_play(encoded_file, mp3_dir):
    mp3_dir = os.path.abspath(mp3_dir)
    
    # 🔥 预热 winmm（关键）
    # warmup_winmm()
    
    with open(encoded_file, 'r') as f:
        lines = [l.strip() for l in f if l.strip()]
    
    total = len(lines)
    print(f'📂 {mp3_dir}')
    print(f'🎵 共 {total} 个音符\n')
 
    events = []
    current_delay = 0
    for line in lines:
        try:
            encoded_int = int(float(line))
            note_id = (encoded_int >> 17) & 0x7F
            delay = encoded_int & 0x1FFF
            current_delay += delay
            midi_note = note_id + 43 # 偏移
            events.append((current_delay, midi_note))
        except ValueError:
            pass
    
    start_wall = time.time()

    for i, (trigger_ms, midi_note) in enumerate(events):
        target = start_wall + trigger_ms / 1000.0
        
        while time.time() < target:
            time.sleep(0.001)
        
        mp3_path = f"{mp3_dir}/{midi_note}.mp3"
        if os.path.exists(mp3_path):
            play_async(mp3_path)
        
        progress = (i + 1) / total * 100
        # print(f'\r🎹 {i+1}/{total} {progress:.1f}% ▶{midi_note}', end='', flush=True)
        # 使用  print在控制台中会阻塞线程
        set_title(f'🎹 {i+1}/{total} {progress:.1f}% ▶{midi_note}')
    time.sleep(2)
    print('\n✅ 播放完成')

def main():
    if len(sys.argv) < 1:
        print("用法: python script.py <输入文件>")
        print("示例: python script.py input.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    # output_file = sys.argv[2]

    decode_and_play(input_file, r'Piano_mp3_MAP')

# 程序入口
if __name__ == "__main__":
    main()