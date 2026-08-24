"""生成两张合成工件图，用来演示尺寸测量和缺陷检测。

工件是 200mm x 100mm 的金属板，带 4 个直径 30mm 的孔；
右上角放一个 50mm 见方的标准块，用于像素->毫米标定。
defect.png 在板上多了一条划痕和一个污点。
"""

from pathlib import Path

import cv2
import numpy as np

from common import cv_imwrite


SAMPLES = Path(__file__).resolve().parent / "samples"
SAMPLES.mkdir(exist_ok=True)

# 比例：1mm = 3px，这样工件 200x100mm 在图上就是 600x300px
PX_PER_MM = 3
IMG_W, IMG_H = 1200, 800


def make_board(background=(90, 96, 104), board=(205, 210, 216), defect=False):
    """画一张工件图。OpenCV 颜色顺序是 BGR。"""
    img = np.full((IMG_H, IMG_W, 3), background, dtype=np.uint8)
    rng = np.random.default_rng(42)

    # 金属板：左上角 (250, 150)，600x300px
    cv2.rectangle(img, (250, 150), (850, 450), board, -1)

    # 4 个孔：直径 30mm = 90px
    holes = [(370, 220), (730, 220), (370, 380), (730, 380)]
    for cx, cy in holes:
        cv2.circle(img, (cx, cy), 45, background, -1)

    # 右上角标准块：50mm x 50mm = 150x150px
    cv2.rectangle(img, (900, 130), (1050, 280), (235, 238, 240), -1)

    # 缺陷：一条斜划痕 + 一个污点
    if defect:
        cv2.line(img, (420, 190), (700, 300), (55, 60, 66), 7)
        cv2.circle(img, (560, 400), 16, (48, 52, 58), -1)

    # 加一点高斯噪声，更像真实相机拍出来的图
    noise = rng.normal(0, 5, img.shape).astype(np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    return img


def main():
    good = make_board(defect=False)
    defect = make_board(defect=True)
    cv_imwrite(SAMPLES / "good.png", good)
    cv_imwrite(SAMPLES / "defect.png", defect)
    print("已生成样本：")
    print("  samples/good.png   （正常工件）")
    print("  samples/defect.png （带划痕和污点的工件）")


if __name__ == "__main__":
    main()
