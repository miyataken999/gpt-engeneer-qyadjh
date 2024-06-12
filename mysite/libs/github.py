import os
import subprocess
import requests
import string
import random
import shutil

def github(token:any):
    # GitHubユーザー名とトークンを環境変数として定義
    GITHUB_USERNAME = "miyataken999"
    GITHUB_TOKEN = token

    # ランダムな文字列を生成する関数
    def generate_random_string(length=6):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))

    # リポジトリ名にランダムな文字列を追加
    REPO_NAME_BASE = "gpt-engeneer"
    REPO_NAME = f"{REPO_NAME_BASE}-{generate_random_string()}"

    # .gitignore ファイルに github.sh と github.py を追加
    with open(".gitignore", "a") as gitignore_file:
        gitignore_file.write("github.sh\n")
        gitignore_file.write("github.py\n")

    # 既存の .git フォルダーを削除
    if os.path.isdir(".git"):
        shutil.rmtree(".git")

    # GitHub APIを使ってリモートリポジトリを作成
    response = requests.post(
        "https://api.github.com/user/repos",
        auth=(GITHUB_USERNAME, GITHUB_TOKEN),
        json={"name": REPO_NAME}
    )

    if response.status_code == 201:
        print(f"Successfully created repository {REPO_NAME}")
    else:
        print(f"Failed to create repository: {response.json()}")
        exit(1)

    # リモートリポジトリのURL (HTTPS形式)
    REPO_URL = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
    REPO_WEB_URL = f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}"  # リポジトリのWeb URL

    # コマンドを実行するヘルパー関数
    def run_command(command):
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        if result.returncode != 0:
            print(f"Command failed: {command}\n{result.stderr}")
            exit(1)
        else:
            print(result.stdout)

    ## ローカルリポジトリを初期化してコミット
    run_command("git init")
    run_command("git add /home/user/app/controllers/*")
    run_command('git commit -m "Initial commit"')

    # git filter-branchの警告を無視する設定
    os.environ['FILTER_BRANCH_SQUELCH_WARNING'] = '1'

    # コミット履歴から機密情報を削除（必要に応じて修正）
    run_command("git filter-branch --force --index-filter "
                '"git rm --cached --ignore-unmatch github.sh" '
                "--prune-empty --tag-name-filter cat -- --all")

    # 既存のリモートリポジトリを削除（存在する場合のみ）
    result = subprocess.run("git remote", shell=True, text=True, capture_output=True)
    if "origin" in result.stdout:
        run_command("git remote remove origin")

    # 新しいリモートリポジトリを追加して強制プッシュ
    run_command(f"git remote add origin {REPO_URL}")
    run_command("git branch -M main")
    run_command("git push -f origin main")

    print(f"Successfully pushed to GitHub repository {REPO_NAME}")
    print(f"Repository URL: {REPO_WEB_URL}")
    return REPO_WEB_URL
