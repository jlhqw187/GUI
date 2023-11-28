import cv2
import os

# 获取图片文件夹中的所有图片文件列表
image_folder = 'demo'
image_files = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder) if filename.endswith('.jpg')]

# 初始化当前图片的索引
current_image_index = 0

# 创建窗口并显示第一张图片
window_name = 'Image Viewer'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.imshow(window_name, cv2.imread(image_files[current_image_index]))

while True:
    key = cv2.waitKey(0)
    
    if key == ord('n'):  # 如果按下 'n' 键，处理下一张图片
        current_image_index = (current_image_index + 1) % len(image_files)
        cv2.imshow(window_name, cv2.imread(image_files[current_image_index]))
    elif key == 27:  # 如果按下 ESC 键，退出循环
        break
    # 检测窗口是否已经关闭，如果已关闭，则退出循环
    if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
        break
    
# 关闭窗口
cv2.destroyAllWindows()
