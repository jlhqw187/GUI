import cv2
import numpy as np

image = cv2.imread(r'F:\xtad\utils\gui\striped_fra828_000397.jpg')

green_filter = np.zeros_like(image)
green_filter[:, :, 1] = 255  # 将绿色通道设置为255

# 将滤镜与原始图像叠加在一起
filtered_image = cv2.addWeighted(image, 0.7, green_filter, 0.3, 0)

# 显示或保存滤镜后的图像
cv2.imshow('Filtered Image', filtered_image)
cv2.imwrite('filtered_image.jpg', filtered_image)

# 等待用户按下任意键后关闭窗口
cv2.waitKey(0)
cv2.destroyAllWindows()
