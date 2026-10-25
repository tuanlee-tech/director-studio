import json, re, sys, os
sys.stdout.reconfigure(encoding='utf-8')

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

def check_rules(channel="tien-thuc-chien", video="thoat-bay-no-the-tin-dung"):
    errors = []

    comp_path = f"channels/{channel}/videos/{video}/assets/remotion-composition.json"
    props_path = "studio/remotion/current_props.json"
    dg_path = f"channels/{channel}/template/components/DynamicGraphic.tsx"

    print(f"=== AUDITING REMOTION MANDATORY RULES FOR {channel}/{video} ===")

    # Check 1: Check prefix leaks in remotion-composition.json
    if os.path.exists(comp_path):
        with open(comp_path, "r", encoding="utf-8") as f:
            cdata = json.load(f)
        for seq in cdata.get("tracks", {}).get("visual_sequences", []):
            sid = seq.get("scene_id", "")
            title = seq.get("props", {}).get("title", "")
            desc = seq.get("description", "")
            if pattern.search(title):
                errors.append(f"[RULE 2 VIOLATION] Scene {sid} in composition has component prefix in title: '{title}'")
            if pattern.search(desc):
                errors.append(f"[RULE 2 VIOLATION] Scene {sid} in composition has component prefix in description: '{desc}'")

    # Check 2: Check prefix leaks in current_props.json
    if os.path.exists(props_path):
        with open(props_path, "r", encoding="utf-8") as f:
            pdata = json.load(f)
        for seq in pdata.get("sequences", []):
            sid = seq.get("scene", "")
            title = seq.get("gfx_props", {}).get("title", "")
            beat = seq.get("beat", "")
            if pattern.search(title):
                errors.append(f"[RULE 2 VIOLATION] Scene {sid} in props has component prefix in title: '{title}'")
            if pattern.search(beat):
                errors.append(f"[RULE 2 VIOLATION] Scene {sid} in props has component prefix in beat: '{beat}'")

    # Check 3: Check GFX fallback coverage in DynamicGraphic.tsx
    if os.path.exists(dg_path) and os.path.exists(comp_path):
        with open(dg_path, "r", encoding="utf-8") as f:
            dg_code = f.read()

        with open(comp_path, "r", encoding="utf-8") as f:
            cdata = json.load(f)

        gfx_scenes = [
            s.get("scene_id")
            for s in cdata.get("tracks", {}).get("visual_sequences", [])
            if s.get("type") == "GFX"
        ]

        unhandled_gfx = []
        for sid in gfx_scenes:
            if f'sc === "{sid}"' not in dg_code and f'"{sid}"' not in dg_code:
                unhandled_gfx.append(sid)

        if unhandled_gfx:
            errors.append(
                f"[RULE 1 VIOLATION] The following {len(unhandled_gfx)} GFX scenes have NO dedicated visual graphic and fall back to plain text: {unhandled_gfx}"
            )
        else:
            print(f"[OK] All {len(gfx_scenes)} GFX scenes have dedicated visual graphics handlers!")

    # Summary
    if errors:
        print("\n[FAIL] AUDIT FAILED! The following mandatory rule violations were found:")
        for err in errors:
            print("  -", err)
        return False
    else:
        print("\n[PASS] AUDIT PASSED! 100% compliant with Remotion Motion Rules.")
        return True

if __name__ == "__main__":
    success = check_rules()
    sys.exit(0 if success else 1)
