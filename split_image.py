import cv2
import numpy as np
import os
import argparse

def mouse_callback(event, x, y, flags, param, ):
    if event == cv2.EVENT_LBUTTONDOWN:
        # print(f"左键单击坐标：({x}, {y})")
        count = striped_mask[y, x, 0]
        if(count):
            clicked[count] = True
            # print(clicked)
            i, j = count2ij[count][0], count2ij[count][1]
            left = j * block_width
            upper = i * block_height
            right = (j + 1) * block_width
            lower = (i + 1) * block_height
            if i == 2 and lower != height:
                lower = height
            if j == 2 and right != width: 
                right = width
            roi = origin_striped[upper + 10*(i):lower+ 10*(i), left+ 10*(j):right+ 10*(j)]
            # 创建绿色滤镜（全绿色，透明度为0.5）
            green_filter = np.zeros_like(roi)
            green_filter[:, :, 1] = 255  # 将绿色通道设置为255
            alpha = 0.5  # 透明度

            # 将滤镜与原始图像区域混合
            filtered_roi = cv2.addWeighted(roi, 1 - alpha, green_filter, alpha, 0)

            # 将处理后的区域放回原始图像
            striped_image[upper + 10*(i):lower+ 10*(i), left+ 10*(j):right+ 10*(j)] = filtered_roi
            cv2.imshow(window_name, striped_image)
    if event == cv2.EVENT_RBUTTONDOWN:
        count = striped_mask[y, x, 0]
        if(count):
            clicked[count] = False
            # print(clicked)
            i, j = count2ij[count][0], count2ij[count][1]
            left = j * block_width
            upper = i * block_height
            right = (j + 1) * block_width
            lower = (i + 1) * block_height
            if i == 2 and lower != height:
                lower = height
            if j == 2 and right != width: 
                right = width
            # roi = origin_striped[upper + 10*(i):lower+ 10*(i), left+ 10*(j):right+ 10*(j)]
            # 创建绿色滤镜（全绿色，透明度为0.5）
            # green_filter = np.zeros_like(roi)
            # green_filter[:, :, 1] = 255  # 将绿色通道设置为255
            # alpha = 0.5  # 透明度

            # 将滤镜与原始图像区域混合
            # filtered_roi = cv2.addWeighted(roi, 1 - alpha, green_filter, alpha, 0)

            # 将处理后的区域放回原始图像
            striped_image[upper + 10*(i):lower+ 10*(i), left+ 10*(j):right+ 10*(j)] = origin_striped[upper + 10*(i):lower+ 10*(i), left+ 10*(j):right+ 10*(j)]
            cv2.imshow(window_name, striped_image)

# args = sys.argv
parser = argparse.ArgumentParser(description='示例命令行解析器')
parser.add_argument('-images', required=True, help='指定图像文件夹的路径')
opt = parser.parse_args()

count2ij = {}
count2xy = {}
image_folder = opt.images
image_files = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder) if filename.endswith('.jpg')]
current_image_index = 0

for i in range(1, 10):
    # full_folder_path = os.path.join(os.path.dirname(image_folder), f'{i}_full')
    # empty_folder_path = os.path.join(os.path.dirname(image_folder), f'{i}_empty')
    full_folder_path = image_folder + '_class' + f'/{i}_full'
    empty_folder_path = image_folder + '_class' + f'/{i}_empty'
    os.makedirs(full_folder_path, exist_ok=True)
    os.makedirs(empty_folder_path, exist_ok=True)




# clicked = np.zeros((10), dtype=bool)
# count = 1

window_name = "origin_window"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.setMouseCallback(window_name, mouse_callback)
# cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.resizeWindow(window_name, 800, 600) 

while True:
    clicked = np.zeros((10), dtype=bool)
    count = 1
    image_name = os.path.basename(image_files[current_image_index]).split('.')[0]
    image = cv2.imread(image_files[current_image_index])
    cv2.setWindowTitle(window_name, image_name + f"                   {current_image_index+1}/{len(image_files)}")

    if os.path.exists(image_folder + '_class/1_full/' + image_name + '_1.jpg') or os.path.exists(image_folder + '_class/1_empty/' + image_name + '_1.jpg'):
        existed = True
    else:
        existed = False
    
    height, width, _ = image.shape
    block_width = width // 3
    block_height = height // 3
    block_shape = (9, block_height, block_width, 3)
    # split_block = np.zeros(block_shape, dtype=np.uint8)

    striped_image_shape = (height + 20, width + 20, 3)
    striped_image = np.ones(striped_image_shape, dtype=np.uint8) * 255
    striped_mask = np.zeros(striped_image_shape, dtype=np.uint8)


    for i in range(3):
        for j in range(3):
            # 定义每个小块的左上角和右下角坐标
            left = j * block_width
            upper = i * block_height
            right = (j + 1) * block_width
            lower = (i + 1) * block_height
            # print(left, upper, right, lower)
            if i == 2 and lower != height:
                lower = height
            if j == 2 and right != width: 
                right = width
            count2xy[count] = (left, upper, right, lower)
            block = image[upper:lower, left:right]
            striped_image[upper + 10*(i):lower+ 10*(i), left+ 10*(j):right+ 10*(j)] = block
            striped_mask[upper + 10*(i):lower+ 10*(i), left+ 10*(j):right+ 10*(j)] = count
            count2ij[count] = (i, j)
            
            # split_block[i * 3 + j] = block

            # normal image
            # cv2.imwrite(os.path.join(f'F:/xtad/utils/gui/{count}', f'{image_name}_{count}.jpg'), block)
            # cv2.imshow(f"{image_path}_{count}", block)
            # cv2.imwrite(os.path.join(f'F:/xtad/utils/gui/{count}', f'{image_name}_{count}.jpg'), split_block[i * 3 + j])
            # cv2.imshow("1", split_block[i * 3 + j])
            
            count += 1
            # cv2.waitKey(0)
    origin_striped = striped_image.copy()
    count = 1 

    if existed:
        for tmp in range(1, 10):
            clicked[tmp] = os.path.exists(image_folder + f'_class/{tmp}_full/' + image_name + f'_{tmp}.jpg')
            if clicked[tmp]:
                i, j = count2ij[tmp][0], count2ij[tmp][1]
                left = j * block_width
                upper = i * block_height
                right = (j + 1) * block_width
                lower = (i + 1) * block_height
                if i == 2 and lower != height:
                    lower = height
                if j == 2 and right != width: 
                    right = width
                roi = origin_striped[upper + 10*(i):lower+ 10*(i), left+ 10*(j):right+ 10*(j)]
                # 创建绿色滤镜（全绿色，透明度为0.5）
                green_filter = np.zeros_like(roi)
                green_filter[:, :, 1] = 255  # 将绿色通道设置为255
                alpha = 0.5  # 透明度

                # 将滤镜与原始图像区域混合
                filtered_roi = cv2.addWeighted(roi, 1 - alpha, green_filter, alpha, 0)

                # 将处理后的区域放回原始图像
                striped_image[upper + 10*(i):lower+ 10*(i), left+ 10*(j):right+ 10*(j)] = filtered_roi
                




    cv2.imshow(window_name, striped_image)
    # print(clicked)

    key = cv2.waitKey(0)
    if key == ord(' '):
        # cv2.destroyWindow(window_name)
        # cv2.setWindowTitle(window_name, image_name)
        current_image_index = (current_image_index + 1) % len(image_files)
        if existed:
            for i in range(1, 10):
                if os.path.exists(image_folder + '_class' + f'/{i}_full/'+image_name+f"_{i}"+".jpg"):
                    os.remove(image_folder + '_class' + f'/{i}_full/'+image_name+f"_{i}"+".jpg")
                else:
                    os.remove(image_folder + '_class' + f'/{i}_empty/'+image_name+f"_{i}"+".jpg")
        for i in range(1, 10):
            # clip = image[count2xy[count][1]:count2xy[count][3], count2xy[count][0]:count2xy[count][2]]
            clip = image[count2xy[i][1]:count2xy[i][3], count2xy[i][0]:count2xy[i][2]]

            if clicked[i]:
                cv2.imwrite(image_folder + '_class' + f'/{i}_full/'+image_name+f"_{i}"+".jpg", clip)
            else:
                cv2.imwrite(image_folder + '_class' + f'/{i}_empty/'+image_name+f"_{i}"+".jpg", clip)
        # clicked = np.zeros((10), dtype=bool)
    elif key == ord('d'):
        # cv2.destroyWindow(window_name)
        current_image_index = (current_image_index + 1) % len(image_files)

    elif key == ord('a'):
        # cv2.destroyWindow(window_name)
        current_image_index = current_image_index - 1
        if current_image_index == -1:
            current_image_index = len(image_files) - 1
        # for i in range(1, 10):
        #     clip = image[count2xy[count][1]:count2xy[count][3], count2xy[count][0]:count2xy[count][2]]
        #     if clicked[i]:
        #         cv2.imwrite(os.path.dirname(image_folder)+f'/{i}_full/'+image_name+f"_{i}"+".jpg", clip)
        #     else:
        #         cv2.imwrite(os.path.dirname(image_folder)+f'/{i}_empty/'+image_name+f"_{i}"+".jpg", clip)
        # clicked = np.zeros((10), dtype=bool)
    # 检测键盘输入，如果是ESC键则退出循环
    elif key == 27:
        break

        # 检测窗口是否已经关闭，如果已关闭，则退出循环
    elif cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
        break

cv2.destroyAllWindows()
