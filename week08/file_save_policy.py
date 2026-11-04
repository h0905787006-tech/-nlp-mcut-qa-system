"""安全檔案儲存：同名檔案須明確選擇覆蓋、末尾追加或略過。"""
from pathlib import Path
import json

def choose_action(path):
    path = Path(path)
    if not path.exists():
        return "o"
    print(f"\n[同名檔案] 已存在：{path.resolve()}")
    while True:
        try:
            choice = input("選擇 [O] 覆蓋 / [A] 末尾追加 / [S] 跳過：").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\n[安全保護] 無法取得確認，已略過寫入。")
            return "s"
        if choice in {"o", "a", "s"}:
            return choice
        print("請輸入 O、A 或 S，不會自動覆蓋。")

def save_text(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    action = choose_action(path)
    if action == "s":
        print(f"[Skip] {path.name}")
        return False
    if action == "a" and path.exists():
        old = path.read_text(encoding="utf-8")
        content = old + ("" if not old or old.endswith("\n") else "\n") + str(content)
    path.write_text(str(content), encoding="utf-8")
    print(f"[Saved] {path}")
    return True

def save_json(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    action = choose_action(path)
    if action == "s":
        print(f"[Skip] {path.name}")
        return False
    data = content
    if action == "a" and path.exists():
        try:
            old = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            print(f"[Error] 舊 JSON 無效，已跳過：{exc}")
            return False
        if isinstance(old, list) and isinstance(content, list):
            data = old + content
        elif isinstance(old, dict) and isinstance(content, dict):
            previous = old.pop("_previous_runs", [])
            data = {**content, "_previous_runs": [*previous, old]}
        else:
            print("[Error] 新舊 JSON 結構不同，已跳過追加。")
            return False
    path.write_text(json.dumps(data, ensure_ascii=False, indent=4), encoding="utf-8")
    print(f"[Saved] {path}")
    return True
