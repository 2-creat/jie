"""公共工具：让 OpenCV 在中文路径下也能正常读写图片。"""

import cv2
import numpy as np


def cv_imread(path):
    """读取图片（兼容中文路径）。"""
    path = str(path)
    data = np.fromfile(path, dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"读不到图片：{path}")
    return img


def cv_imwrite(path, img):
    """保存图片（兼容中文路径）。"""
    path = str(path)
    ext = "." + path.rsplit(".", 1)[-1]
    ok, buf = cv2.imencode(ext, img)
    if not ok:
        raise IOError(f"保存图片失败：{path}")
    buf.tofile(path)
