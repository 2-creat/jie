"""Day 01: Python 查漏补缺自测。

跑法：python python_quiz.py
每道题会打印 PASS 或 FAIL，最后给分数。FAIL 的题就是需要补的知识点。
题目结合光电实验、中药材、就业数据场景，练完能直接用。
"""

import json
import math


# 1. 类型与运算：把一个字符串列表里的数字转成 int 再求和
def q1(numbers):
    return sum(int(n) for n in numbers)


# 2. 字典操作：统计每种药材出现的次数
def q2(items):
    counter = {}
    for item in items:
        counter[item] = counter.get(item, 0) + 1
    return counter


# 3. 列表推导：找出 1-50 里能被 3 整除的数
def q3():
    return [n for n in range(1, 51) if n % 3 == 0]


# 4. 函数与默认参数：按百分比给数据打 9 折
def q4(price, discount=0.9):
    return round(price * discount, 2)


# 5. 字符串处理：把 "XianShiYou" 转成全小写并去空格
def q5(text):
    return text.lower().replace(" ", "")


# 6. 文件与 JSON：读取 JSON 字符串并取出 "name"
def q6(raw):
    return json.loads(raw)["name"]


# 7. 异常处理：除以 0 时返回 "error"
def q7(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "error"


# 8. 列表排序：按元组第二个元素升序
def q8(pairs):
    return sorted(pairs, key=lambda p: p[1])


# 9. 集合去重：返回不重复的元素个数
def q9(values):
    return len(set(values))


# 10. 循环与枚举：把 ["光谱仪", "分光计", "平行光管"] 变成 "1-光谱仪 2-分光计 3-平行光管"
def q10(names):
    return " ".join(f"{i}-{name}" for i, name in enumerate(names, start=1))


def main():
    checks = [
        ("q1 数字求和", q1(["1", "2", "3", "4"]) == 10),
        ("q2 药材统计", q2(["五味子", "柴胡", "五味子"]) == {"五味子": 2, "柴胡": 1}),
        ("q3 3 的倍数", q3()[:5] == [3, 6, 9, 12, 15] and len(q3()) == 16),
        ("q4 九折", q4(100) == 90.0),
        ("q5 字符串", q5("Xi an Shi You ") == "xianshiyou"),
        ("q6 JSON", q6('{"name": "杨杰"}') == "杨杰"),
        ("q7 除零", q7(1, 0) == "error"),
        ("q8 排序", q8([("b", 2), ("a", 1)]) == [("a", 1), ("b", 2)]),
        ("q9 去重", q9([1, 1, 2, 3, 3, 3]) == 3),
        ("q10 枚举", q10(["光谱仪", "分光计", "平行光管"]) == "1-光谱仪 2-分光计 3-平行光管"),
    ]

    passed = 0
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
        if ok:
            passed += 1
    print(f"\n得分：{passed}/{len(checks)}")
    if passed == len(checks):
        print("全部通过，今天 Python 这部分过关。")
    else:
        print("有没通过的题：把对应函数看一遍，改对后再跑。")


if __name__ == "__main__":
    main()
