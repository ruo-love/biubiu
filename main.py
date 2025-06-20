import datetime
from pathlib import Path
import subprocess
import os
import sys
import logging
from ai.ai import query_ai

# 配置日志
logging.basicConfig(
    filename='schedule.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    encoding='utf-8'
)

def append_to_readme():
    readme_path = Path("README.md")
    if not readme_path.exists():
        logging.warning("README.md 文件不存在，创建一个新的")
        readme_path.write_text("# 项目说明\n\n", encoding="utf-8")

    import pytz
    beijing_tz = pytz.timezone('Asia/Shanghai')
    now = datetime.datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M:%S")
    content_to_insert = query_ai()
    content_to_insert = f"\n\n#### 更新时间 {now}\n\n{content_to_insert}\n\n"

    # 先读取旧内容
    old_content = readme_path.read_text(encoding="utf-8")

    # 新内容放最前面，再加旧内容
    new_content = content_to_insert + old_content

    # 写回文件
    readme_path.write_text(new_content, encoding="utf-8")

    logging.info(f"已插入内容到 README.md 开头: {content_to_insert.strip()}")
def update_github():
    try:
        subprocess.run(["git", "config", "--global", "user.name", "github-actions[bot]"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "github-actions[bot]@users.noreply.github.com"], check=True)

        token = os.getenv("GITHUB_TOKEN")
        repo = os.getenv("GITHUB_REPOSITORY")
        if not token or not repo:
            logging.error("缺少 GITHUB_TOKEN 或 GITHUB_REPOSITORY 环境变量")
            sys.exit(1)

        remote_url = f"https://x-access-token:{token}@github.com/{repo}.git"
        subprocess.run(["git", "remote", "set-url", "origin", remote_url], check=True)

        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if not status.stdout.strip():
            logging.info("没有文件变更，无需提交")
            return

        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "chore: update README.md 更新时间"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        logging.info("已成功提交并推送到远程仓库")

    except subprocess.CalledProcessError as e:
        logging.error(f"Git 命令执行失败: {e}")
        sys.exit(1)

def run():
    try:
        append_to_readme()
        update_github()
    except Exception as e:
        logging.error(f"脚本运行异常: {e}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        run()  # 或你的主逻辑函数
    except Exception as e:
        import traceback
        print("❌ 程序执行失败：", e)
        traceback.print_exc()
        exit(1)
