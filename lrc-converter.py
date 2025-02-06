import os
import re
import sys

def vtt_to_lrc(vtt_content):
    lrc_content = []
    srt_blocks = re.split(r'\n\n+', vtt_content.strip())
    for block in srt_blocks:
        lines = block.split('\n')
        if len(lines) < 3:
            continue 
        
        # Extract the timestamp line
        timestamp_line = lines[1]
        start_time, _ = timestamp_line.split(' --> ')

        # Convert VTT timestamp to LRC format
        hhmmss_or_mmss, millisecond = start_time.split('.')
        millisecond = millisecond[:2]
        if (len(hhmmss_or_mmss) == 8):
            hour, minute, second = hhmmss_or_mmss.split(':')
            minute = (int(hour) * 60 + int(minute)) % 100
            start_time = f"{minute:02d}:{second}.{millisecond}"
        else:
            start_time = f"{hhmmss_or_mmss}.{millisecond}"
        
        # Extract the text lines
        text_lines = lines[2:]
        text = ' '.join(text_lines)
        
        # Format the LRC line
        lrc_line = f"[{start_time}]{text}"
        lrc_content.append(lrc_line)
    
    return '\n'.join(lrc_content)

def srt_to_lrc(srt_content):
    lrc_content = []
    srt_blocks = re.split(r'\n\n+', srt_content.strip())
    
    for block in srt_blocks:
        lines = block.split('\n')
        if len(lines) < 3:
            continue 
        
        # Extract the timestamp line
        timestamp_line = lines[1]
        start_time, _ = timestamp_line.split(' --> ')
        
        # Convert SRT timestamp to LRC format
        hhmmss, millisecond = start_time.split(',')
        hour, minute, second = hhmmss.split(':')
        minute = (int(hour) * 60 + int(minute)) % 100
        millisecond = millisecond[:2]
        start_time = f"{minute:02d}:{second}.{millisecond}"
        
        # Extract the text lines
        text_lines = lines[2:]
        text = ' '.join(text_lines)
        
        # Format the LRC line
        lrc_line = f"[{start_time}]{text}"
        lrc_content.append(lrc_line)
    
    return '\n'.join(lrc_content)

def convert(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.mp3.vtt'):
            vtt_path = os.path.join(directory, filename)
            lrc_path = os.path.join(directory, filename.replace('.mp3.vtt', '.lrc'))
            with open(vtt_path, 'r', encoding='utf-8') as vtt_file:
                vtt_content = vtt_file.read()
            lrc_content = vtt_to_lrc(vtt_content)
            with open(lrc_path, 'w', encoding='utf-8') as lrc_file:
                lrc_file.write(lrc_content)
            print(f"✓ Created {lrc_path}")
        elif filename.endswith('.vtt'):
            vtt_path = os.path.join(directory, filename)
            lrc_path = os.path.join(directory, filename.replace('.vtt', '.lrc'))
            with open(vtt_path, 'r', encoding='utf-8') as vtt_file:
                vtt_content = vtt_file.read()
            lrc_content = vtt_to_lrc(vtt_content)
            with open(lrc_path, 'w', encoding='utf-8') as lrc_file:
                lrc_file.write(lrc_content)
            print(f"✓ Created {lrc_path}")
        elif filename.endswith('.srt'):
            srt_path = os.path.join(directory, filename)
            lrc_path = os.path.join(directory, filename.replace('.srt', '.lrc'))
            with open(srt_path, 'r', encoding='utf-8') as srt_file:
                srt_content = srt_file.read()
            lrc_content = srt_to_lrc(srt_content)
            with open(lrc_path, 'w', encoding='utf-8') as lrc_file:
                lrc_file.write(lrc_content)
            print(f"✓ Created {lrc_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python lrc-converter.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    convert(directory)
