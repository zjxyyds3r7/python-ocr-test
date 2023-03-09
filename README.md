# python-ocr-test
基于python opencv paddle的图片转表格
作者:zjx vx:zjxyyds0307
1. 用的包: paddleocr opencv 安装方法百度csdn
2. 主要思路:  
   1. 提取有效区域(main line28)
   2. 对first title预处理(main line39) 提取到first_list中
   3. 提取second title区域存为sec (main line42)
   4. 对sec部分进行ocr并获取坐标 通过坐标判定属于哪一个first title(main line61)
   5. 将结果存到output数组中 转化为pd的df 存为xls (main line67)
3. 提取用户划了哪个分数:  
   采用计算区域内黑色像素点的数量 取最大值