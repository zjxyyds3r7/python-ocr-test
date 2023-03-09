import cv2 as cv
import pandas as pd

from paddleocr import PaddleOCR
import logging

import util
logging.disable(logging.DEBUG)  # 关闭DEBUG日志的打印
logging.disable(logging.WARNING)  # 关闭WARNING日志的打印

ocr = PaddleOCR(use_angle_cls=True, lang="ch")

# 标题高度
title_high = 62
# 考评内容宽度
first_head_width = 82
# 指标宽度
second_head_width = 245

path = '.\\pic\\1.jpg'
m = cv.imread(path)
m = cv.resize(m, (m.shape[1] // 2, m.shape[0] // 2))
# 获取图片

x, y, w, h = util.getMaxRec(m)
m = m[y + title_high:h, x:w]
# 提取有效区域

high_ = 0
first_list = []
# 坐标 小于此坐标的first title

for i in range(h - y - title_high):
    k = m[i:i + 1, 0:first_head_width]
    kn = util.blackScale(k)
    if kn > 0.9 and i - high_ > 20:
        result = ocr.ocr(m[high_:i, 0:first_head_width], cls=True)
        if result:
            first_list.append([i, result[0][0][1][0]])
            high_ = i

sec = m[:, first_head_width: second_head_width]

res = ocr.ocr(sec, cls=True)

output = []

for i in res[0]:
    y_min, y_max = util.get_y(i[0])
    y_min, y_max = int(y_min), int(y_max)
    max_count = 0
    score = -1
    text = i[1][0]
    for j in range(10):
        find_pic = m[y_min:y_max, second_head_width + 15 + j * 45:second_head_width + 15 + j * 45 + 35]
        uct = util.countBlack(find_pic)
        if uct > max_count:
            max_count = uct
            score = 10 - j
    first_title = None
    for first in first_list:
        if first[0] > y_max:
            first_title = first[1]
            break
    output.append([first_title, text, score])

df = pd.DataFrame(output, columns=['考评内容', '指标', '考核评价'])
print(df)
df.to_excel('res.xls', index=False)
