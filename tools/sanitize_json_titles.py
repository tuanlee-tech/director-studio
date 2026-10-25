import json, re

def clean_title(t):
    if not t:
        return ''
    cleaned = re.sub(r'^[A-Za-z0-9_]+(\s+[^\:]+)?:\s*', '', t).strip()
    cleaned = re.sub(r'^(Tiêu đề\s*[\:\'\"]*|\"|\')', '', cleaned).strip()
    cleaned = re.sub(r'[\'\"]$', '', cleaned).strip()
    return cleaned

for path in [
    'channels/tien-thuc-chien/videos/thoat-bay-no-the-tin-dung/assets/remotion-composition.json',
    'studio/remotion/current_props.json'
]:
    with open(path, encoding='utf-8') as f:
        data = json.load(f)

    # In remotion-composition.json: tracks.visual_sequences
    if 'tracks' in data and 'visual_sequences' in data['tracks']:
        for seq in data['tracks']['visual_sequences']:
            if 'props' in seq and 'title' in seq['props']:
                seq['props']['title'] = clean_title(seq['props']['title'])

    # In current_props.json: sequences
    if 'sequences' in data:
        for seq in data['sequences']:
            if 'gfx_props' in seq and 'title' in seq['gfx_props']:
                seq['gfx_props']['title'] = clean_title(seq['gfx_props']['title'])
            if 'beat' in seq:
                seq['beat'] = clean_title(seq['beat'])

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'Sanitized titles in {path}')
