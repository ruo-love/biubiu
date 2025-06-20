import json
import datetime
from pathlib import Path
import subprocess
import os
def append_to_readme():
    readme_path = Path("README.md")
    if not readme_path.exists():
        print("❌ README.md 文件不存在，创建一个新的")
        readme_path.write_text("# 项目说明\n\n", encoding="utf-8")

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content_to_append = f"\n- 更新时间：{now}\n"

    with readme_path.open("a", encoding="utf-8") as f:
        f.write(content_to_append)

    print(f"✅ 已追加内容到 README.md:\n{content_to_append}")

def update_github():
    # Git 设置
    subprocess.run(["git", "config", "--global", "user.name", "github-actions[bot]"])
    subprocess.run(["git", "config", "--global", "user.email", "github-actions[bot]@users.noreply.github.com"])

    # 使用 token 重新设置远程地址（必须使用 https + token）
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPOSITORY")  # e.g. "ruo-love/my-dream"
    remote_url = f"https://x-access-token:{token}@github.com/{repo}.git"
    subprocess.run(["git", "remote", "set-url", "origin", remote_url])

    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", f"chore: update updateTime to {now}"])
    subprocess.run(["git", "push", "origin", "main"])

def run():
    append_to_readme()
    update_github()
if __name__ == "__main__":
    run()
