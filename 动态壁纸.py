import pygame
import random
import win32api
import win32con
import win32gui


def show_snow():
    screen = pygame.display.set_mode((1920, 1080)) # For borderless, use pygame.NOFRAME
    done = False
    fuchsia = (255, 0, 128)  # Transparency color

    # 创建一个窗口并且设置为透明
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE| win32con.SWP_NOOWNERZORDER|win32con.SWP_SHOWWINDOW) 


    SIZE = (1920, 1080)
    # 雪花列表
    snow_list = []
    
    # 初始化雪花：[x坐标, y坐标, x轴速度, y轴速度]
    for i in range(50):
        x = random.randrange(0, SIZE[0])
        y = random.randrange(0, SIZE[1])
        sx = random.randint(-2, 2)
        sy = random.randint(2, 5)
        snow_list.append([x, y, sx, sy])
    
    while not done:
        # 消息事件循环，判断退出
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        screen.fill(fuchsia)
        # 雪花列表循环
        for i in range(len(snow_list)):
            # 绘制雪花，颜色、位置、大小
            pygame.draw.circle(screen, (255, 255, 255), snow_list[i][:2], snow_list[i][3]-1)
    
            # 移动雪花位置（下一次循环起效）
            snow_list[i][0] += snow_list[i][2]
            snow_list[i][1] += snow_list[i][3]
    
            # 如果雪花落出屏幕，重设位置
            if snow_list[i][1] > SIZE[1]:
                snow_list[i][1] = random.randrange(-50, -10)
                snow_list[i][0] = random.randrange(0, SIZE[0])
    
        # 刷新屏幕
        pygame.display.flip()
        pygame.time.Clock().tick(60)
show_snow()
# 退出 
# pygame.quit()