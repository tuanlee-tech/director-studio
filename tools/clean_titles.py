import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('all_scenes_summary.txt', encoding='utf-8') as f:
    lines = f.readlines()

def clean_title(t):
    cleaned = re.sub(r'^[A-Za-z0-9_]+(\s+[^\:]+)?:\s*', '', t).strip()
    cleaned = re.sub(r'^(Tiêu đề\s*[\:\'\"]*|\"|\')', '', cleaned).strip()
    cleaned = re.sub(r'[\'\"]$', '', cleaned).strip()
    return cleaned

for line in lines[:30]:
    parts = line.strip().split(' | ')
    if len(parts) >= 4:
        title = parts[3].replace('Title: ', '')
        if title:
            print(f'RAW:   {title}')
            print(f'CLEAN: {clean_title(title)}\n')
