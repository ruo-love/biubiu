import json
import datetime
from pathlib import Path
import subprocess
import os

def update_package_json():
    package_path = Path("package.json")
    if not package_path.exists():
        print("❌ package.json 不存在")
        return

    with package_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["updateTime"] = now

    with package_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ updateTime 更新为: {now}")

    # Git 设置
    subprocess.run(["git", "config", "--global", "user.name", "github-actions[bot]"])
    subprocess.run(["git", "config", "--global", "user.email", "github-actions[bot]@users.noreply.github.com"])

    # 使用 token 重新设置远程地址（必须使用 https + token）
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPOSITORY")  # e.g. "ruo-love/my-dream"
    remote_url = f"https://x-access-token:{token}@github.com/{repo}.git"
    subprocess.run(["git", "remote", "set-url", "origin", remote_url])

    subprocess.run(["git", "add", "package.json"])
    subprocess.run(["git", "commit", "-m", f"chore: update updateTime to {now}"])
    subprocess.run(["git", "push", "origin", "main"])

if __name__ == "__main__":
    update_package_json()
