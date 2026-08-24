"""一键运行：生成样本 -> 尺寸测量 -> 缺陷检测。"""

import subprocess
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parent


def run(name):
    print(f"\n===== {name} =====")
    subprocess.run([sys.executable, str(BASE / name)], check=True)


def main():
    run("make_samples.py")
    run("measure.py")
    run("detect_defect.py")
    print("\n全部完成！结果在 output/ 目录。")


if __name__ == "__main__":
    main()
