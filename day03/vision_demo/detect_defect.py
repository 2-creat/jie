"""缺陷检测：模板差分法，找出板上的划痕和污点。

思路：AOI 产线里最常见的做法是对比“标准件”和“待检件”。
两张图逐像素求差，差异大的地方就是疑似缺陷；再用面积过滤排除噪声。
"""

from pathlib import Path

import cv2
import numpy as np

from common import cv_imread, cv_imwrite


BASE = Path(__file__).resolve().parent


def main():
    color = cv_imread(BASE / "samples" / "defect.png")
    gray = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
    good_gray = cv2.cvtColor(cv_imread(BASE / "samples" / "good.png"), cv2.COLOR_BGR2GRAY)

    # 1) 提取工件板区域作为掩码，只在板内找缺陷
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    board = max(contours, key=cv2.contourArea)
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, [board], -1, 255, -1)

    # 2) 差分：标准件和待检件逐像素相减，差异越大越可能是缺陷
    diff = cv2.absdiff(good_gray, gray)
    diff = cv2.bitwise_and(diff, mask)

    # 3) 阈值 + 形态学清理：把零散噪声点去掉
    _, thresh = cv2.threshold(diff, 18, 255, cv2.THRESH_BINARY)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

    # 4) 按面积过滤：太小是噪声，太大是孔/边界
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    defects = []
    for c in contours:
        area = cv2.contourArea(c)
        if area < 60 or area > 12000:
            continue
        x, y, w, h = cv2.boundingRect(c)
        defects.append((x, y, w, h, area))

    # 5) 画红框标出缺陷
    out = color.copy()
    for x, y, w, h, area in defects:
        cv2.rectangle(out, (x, y), (x + w, y + h), (0, 0, 255), 3)
        cv2.putText(out, "DEFECT", (x, max(0, y - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv_imwrite(BASE / "output" / "defect_result.png", out)

    print(f"发现疑似缺陷 {len(defects)} 处")
    for x, y, w, h, area in defects:
        print(f"  位置 ({x}, {y}) 大小 {w}x{h}px，面积 {area}px")
    print("结果图：output/defect_result.png")


if __name__ == "__main__":
    main()
