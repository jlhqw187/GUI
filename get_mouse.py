import cv2

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"左键单击坐标：({x}, {y})")


image = cv2.imread(r'F:\xtad\utils\gui\fra828_000397.jpg')

cv2.namedWindow('Image')
cv2.setMouseCallback('Image', mouse_callback)

while True:
    # 显示图像
    cv2.imshow('Image', image)

    # 检测键盘输入，如果是ESC键则退出循环
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
