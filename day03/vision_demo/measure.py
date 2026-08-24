"""尺寸测量：用标准块标定像素比例，再测量工件的长宽和孔直径。"""

from pathlib import Path

import cv2
import numpy as np

from common import cv_imread, cv_imwrite


BASE = Path(__file__).resolve().parent
REF_MM = 50.0          # 标准块实际边长 50mm


def find_contours(gray):
    """二值化后找轮廓，按面积从大到小返回。"""
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    return contours


def contour_rect(c):
    """轮廓的最小外接矩形，返回中心、宽、高、角度。"""
    rect = cv2.minAreaRect(c)
    (cx, cy), (w, h), angle = rect
    return (cx, cy), w, h, angle


def main():
    gray = cv2.cvtColor(cv_imread(BASE / "samples" / "good.png"), cv2.COLOR_BGR2GRAY)
    color = cv_imread(BASE / "samples" / "good.png")

    contours = find_contours(gray)

    # 1) 找标准块：中心 x > 850 的最大轮廓（右上角区域）
    ref = None
    for c in contours:
        (cx, cy), w, h, _ = contour_rect(c)
        if cx > 850 and cv2.contourArea(c) > 5000:
            ref = (c, (cx, cy), w, h)
            break
    if ref is None:
        raise SystemExit("没找到标准块")
    _, ref_center, ref_w, ref_h = ref
    px_per_mm = ((ref_w + ref_h) / 2) / REF_MM

    # 2) 找工件板：面积最大的轮廓（中心在画面中间）
    board = None
    for c in contours:
        area = cv2.contourArea(c)
        (cx, cy), w, h, _ = contour_rect(c)
        if 100 < cx < 1000 and 100 < cy < 700 and area > 100000:
            board = (c, (cx, cy), w, h)
            break
    if board is None:
        raise SystemExit("没找到工件板")
    _, board_center, board_w, board_h = board

    # 3) 找孔：板内部面积 2000-8000 的圆形轮廓
    holes = []
    for c in contours:
        area = cv2.contourArea(c)
        if 2000 < area < 8000:
            (x, y), radius = cv2.minEnclosingCircle(c)
            holes.append(((x, y), radius))

    # 4) 像素换算毫米
    board_w_mm, board_h_mm = sorted(
        [board_w / px_per_mm, board_h / px_per_mm], reverse=True
    )
    hole_diams = [2 * r / px_per_mm for _, r in holes]

    # 5) 画标注并保存
    out = color.copy()
    cv2.drawContours(out, [board[0]], -1, (255, 128, 0), 3)
    cv2.putText(out, f"Board: {board_w_mm:.1f} x {board_h_mm:.1f} mm",
                (int(board_center[0] - 120), int(board_center[1])),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 128, 0), 2)
    for (cx, cy), r in holes:
        cv2.circle(out, (int(cx), int(cy)), int(r), (0, 200, 255), 2)
    cv2.drawContours(out, [ref[0]], -1, (0, 200, 255), 3)
    cv2.putText(out, "Ref 50mm", (int(ref_center[0] - 40), int(ref_center[1])),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)
    cv_imwrite(BASE / "output" / "measure_result.png", out)

    print(f"标定比例：{px_per_mm:.2f} px/mm（标准块 50mm）")
    print(f"工件尺寸：{board_w_mm:.1f} mm x {board_h_mm:.1f} mm（理论 200 x 100）")
    print("孔直径：", ", ".join(f"{d:.1f} mm" for d in sorted(hole_diams)))
    print("结果图：output/measure_result.png")


if __name__ == "__main__":
    main()
