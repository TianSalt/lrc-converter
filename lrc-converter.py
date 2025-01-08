import os
import re
import sys

def vtt_to_lrc(vtt_content):
    lrc_content = []
    lines = vtt_content.strip().split('\n')
    
    # Skip the first 2 lines which is "WEBVTT\n"
    lines = lines[2:]
    
    for i in range(0, len(lines), 3):
        if i + 1 >= len(lines):
            break
        
        # Extract the timestamp line
        timestamp_line = lines[i].strip()
        start_time, end_time = timestamp_line.split(' --> ')
        
        # Convert VTT timestamp to LRC format
        start_time = start_time[:8]  # Keep only HH:MM.SS
        
        # Extract the text line
        text_line = lines[i + 1].strip()
        
        # Format the LRC line
        lrc_line = f"[{start_time}]{text_line}"
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
        start_time, end_time = timestamp_line.split(' --> ')
        
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
        print(f"Converting {filename}...")
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
            print(f"Converting {filename}...")
            srt_path = os.path.join(directory, filename)
            lrc_path = os.path.join(directory, filename.replace('.srt', '.lrc'))
            
            with open(srt_path, 'r', encoding='utf-8') as srt_file:
                srt_content = srt_file.read()
            
            lrc_content = srt_to_lrc(srt_content)
            
            with open(lrc_path, 'w', encoding='utf-8') as lrc_file:
                lrc_file.write(lrc_content)
            
            print(f"✓ Created {lrc_path}")
        else:
            print(f"Error converting {filename}: Format not supported.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python lrc-converter.py <directory>")
        sys.exit(1)
    
    directory = sys.argv[1]
    convert(directory)
