"""真实照片版：用一枚硬币做标定，测量照片里工件的尺寸。

拍摄要求：
  1. 深色背景上放 1 件要测的工件 + 1 枚一元硬币
  2. 手机垂直俯拍，硬币和工件不要重叠
  3. 光线均匀，不要开闪光灯

用法：
  python measure_real.py --image "D:/photo.jpg" --ref-mm 25

默认按一元硬币直径 25mm 标定；如果是五角硬币，直径 20.5mm。
"""

import argparse
import math
from pathlib import Path

import cv2
import numpy as np

from common import cv_imread, cv_imwrite


def find_contours(gray):
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return [c for c in contours if cv2.contourArea(c) > 2000]


def circularity(c):
    """圆度：越接近 1 越圆。4πA / P²"""
    area = cv2.contourArea(c)
    peri = cv2.arcLength(c, True)
    if peri == 0:
        return 0
    return 4 * math.pi * area / (peri * peri)


def main():
    parser = argparse.ArgumentParser(description="真实照片尺寸测量")
    parser.add_argument("--image", required=True, help="照片路径")
    parser.add_argument("--ref-mm", type=float, default=25.0, help="参考硬币直径，一元=25mm")
    args = parser.parse_args()

    image_path = Path(args.image)
    color = cv_imread(image_path)
    gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
    contours = find_contours(gray)
    if len(contours) < 2:
        raise SystemExit("没找到足够的轮廓，检查背景反差和光线")

    # 1) 参考硬币：圆度足够高、面积最大（避免把工件上的小圆孔当硬币）
    circles = [c for c in contours if circularity(c) > 0.8]
    if not circles:
        raise SystemExit("没找到圆度足够的参考硬币，检查硬币是否完整、光线是否均匀")
    coin = max(circles, key=cv2.contourArea)
    (cx, cy), radius = cv2.minEnclosingCircle(coin)
    coin_diam_px = radius * 2
    px_per_mm = coin_diam_px / args.ref_mm

    # 2) 工件：除硬币外面积最大的轮廓
    board = None
    for c in contours:
        if c is coin:
            continue
        if board is None or cv2.contourArea(c) > cv2.contourArea(board):
            board = c
    if board is None:
        raise SystemExit("没找到工件轮廓")

    rect = cv2.minAreaRect(board)
    (bx, by), (bw, bh), angle = rect
    w_mm, h_mm = sorted([bw / px_per_mm, bh / px_per_mm], reverse=True)

    # 3) 画标注并保存
    out = color.copy()
    cv2.drawContours(out, [coin], -1, (0, 200, 255), 3)
    cv2.putText(out, "Ref coin", (int(cx) - 40, int(cy) - int(radius) - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)
    cv2.drawContours(out, [board], -1, (255, 128, 0), 3)
    cv2.putText(out, f"{w_mm:.1f} x {h_mm:.1f} mm",
                (int(bx) - 80, int(by)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 128, 0), 2)

    save_dir = image_path.parent
    out_path = save_dir / (image_path.stem + "_measured.png")
    cv_imwrite(out_path, out)

    print(f"标定：{px_per_mm:.2f} px/mm（参考直径 {args.ref_mm}mm）")
    print(f"工件尺寸：{w_mm:.1f} x {h_mm:.1f} mm")
    print(f"结果图：{out_path}")


if __name__ == "__main__":
    main()
