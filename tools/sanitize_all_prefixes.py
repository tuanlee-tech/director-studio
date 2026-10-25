import json, re

KNOWN_PREFIXES = [
    'ChartMotion', 'SplitComparison', 'AlertBox', 'FocusCard', 'CounterNumber',
    'LoopDiagram', 'TreeGrowth', 'IntroCard', 'BarChart', 'PieChart',
    'TimelineSlider', 'Infographic', 'CalendarAnimation', 'StackFee',
    'DrainWater', 'MonthCalendar', 'CreditScoreMeter', 'BadgeGraphic',
    'ComparisonTable', 'ProgressBar', 'MilestoneUnlocked', 'StepFlow',
    'StepHeader', 'AppUnlink', 'TargetHighlight', 'BadgeUnlock',
    'SalarySplit', 'BudgetEnvelope', 'CountdownMonths', 'AssetTree', 'MotionGraphic'
]

pattern = re.compile(rf"^({'|'.join(KNOWN_PREFIXES)})(\s+[^\:]+)?:?\s*", re.IGNORECASE)

def strip_prefix(t):
    if not t:
        return ''
    cleaned = pattern.sub('', t).strip()
    cleaned = re.sub(r'^(Tiêu đề\s*[\:\'\"]*|\"|\')', '', cleaned).strip()
    cleaned = re.sub(r'[\'\"]$', '', cleaned).strip()
    return cleaned

for path in [
    'channels/tien-thuc-chien/videos/thoat-bay-no-the-tin-dung/assets/remotion-composition.json',
    'studio/remotion/current_props.json'
]:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if 'tracks' in data and 'visual_sequences' in data['tracks']:
        for seq in data['tracks']['visual_sequences']:
            if 'props' in seq and 'title' in seq['props']:
                seq['props']['title'] = strip_prefix(seq['props']['title'])
            if 'description' in seq:
                seq['description'] = strip_prefix(seq['description'])

    if 'sequences' in data:
        for seq in data['sequences']:
            if 'gfx_props' in seq and 'title' in seq['gfx_props']:
                seq['gfx_props']['title'] = strip_prefix(seq['gfx_props']['title'])
            if 'beat' in seq:
                seq['beat'] = strip_prefix(seq['beat'])

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("Successfully sanitized all prefixes!")
