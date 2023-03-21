import os
import gc
import sys
import time
import random
import pygame
import ctypes
import inspect
import win32gui
import win32con
import win32api
import threading
from PyQt5.QtGui import QPixmap,QCursor,QIcon,QPainter,QPen
from PyQt5.QtCore import QTimer,Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,QMenu

# 自定义线程
class MyThreadFunc(object):
    '''
    手动终止线程的方法
    '''
    def __init__(self, func):
        self.myThread = threading.Thread(target=func)

    def start(self):
        print('线程启动')
        self.myThread.start()

    def stop(self):
        print('线程终止')
        try:
            for i in range(5):
                self._async_raise(self.myThread.ident, SystemExit)
                # time.sleep(1)
        except Exception as e:
            print(e)

    def _async_raise(self, tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

basedir = ''
#根据系统运行位置确认basedir路径
if getattr(sys, 'frozen', None):
    basedir = sys._MEIPASS
else:
    basedir = os.path.dirname(__file__)

# 雪花
class Snow():

    # 初始化
    def __init__(self):
        super().__init__()
        pygame.init()
        self.infoObject = pygame.display.Info()
        self.size = (self.infoObject.current_w, self.infoObject.current_h)
        # self.size = (self.infoObject.current_w, self.infoObject.current_h)
        self.done = False 
        self.snow_num = 50

        self.active = False
        self.music_active = False 
        self.music_track = False
        self.snow_thread = False 
        self.snow_music_thread = False 
        self.fuchsia = (255, 0, 128)  # Transparency color
        # 雪花列表
        # self.screen = pygame.display.set_mode((1920, 1080)) # For borderless, use pygame.NOFRAME
        
    def init_snow_list(self):
        self.snow_list = []
        # 初始化雪花：[x坐标, y坐标, x轴速度, y轴速度]
        for i in range(self.snow_num):
            x = random.randrange(0, self.size[0])
            y = random.randrange(-self.size[1], -400)
            sx = random.randint(-2, 1)
            sy = random.randint(2, 4)
            self.snow_list.append([x, y, sx, sy])
    # 音乐
    def music(self,active = True):
        self.music_active = active
        if active:
            pygame.mixer.init()
            self.music_track = pygame.mixer.music.load(os.path.join(basedir, 'music/music.mp3'))
            pygame.mixer.music.play(loops=1)
        else:
            pygame.mixer.music.fadeout(300) # 停止
    
    # 渲染雪花
    def update_snow(self):
        self.screen.fill(self.fuchsia)
        # 雪花列表循环
        for i in range(len(self.snow_list)):
            # 绘制雪花，颜色、位置、大小
            pygame.draw.circle(self.screen, (255, 255, 255), self.snow_list[i][:2], self.snow_list[i][3]-1)
    
            # 移动雪花位置（下一次循环起效）
            self.snow_list[i][0] += self.snow_list[i][2]
            self.snow_list[i][1] += self.snow_list[i][3]
    
            # 如果雪花落出屏幕，重设位置
            if self.snow_list[i][1] > self.size[1]:
                self.snow_list[i][0] = random.randrange(0, self.size[0])
                self.snow_list[i][1] = random.randrange(-50, -10)
                # 如果预设雪花变大就多加一点
                # print(len(self.snow_list))
                if len(self.snow_list) < 100 and i % 10==0:
                    x = random.randrange(0, self.size[0])
                    y = random.randrange(-50, -10)
                    sx = random.randint(-1, 3)
                    sy = random.randint(2, 5)
                    # print([x, y, sx, sy])
                    self.snow_list.append([x, y, sx, sy])

    # 显示雪花
    def show_snow(self,active):
        gc.collect()
        self.active = active
        def _show_snow():

            self.screen = pygame.display.set_mode((self.size[0],self.size[1])) # For borderless, use pygame.NOFRAME
            # 创建一个窗口并且设置为透明
            hwnd = pygame.display.get_wm_info()["window"]
            # print(hwnd)
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
            win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*self.fuchsia), 0, win32con.LWA_COLORKEY)
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0,0,0,0, win32con.SWP_NOMOVE | win32con.SWP_NOACTIVATE| win32con.SWP_NOOWNERZORDER|win32con.SWP_SHOWWINDOW)
            # win32gui.ShowWindow(hwnd,win32con.SW_SHOW) # 把句柄传给showwindow实现显示隐藏效果
            while not self.done:
                # 消息事件循环，判断退出
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.music(False) # 关闭音乐
                        self.done = True
                        self.active = False
                        break
                # 按钮关闭
                if self.active == False:
                    self.music(False) # 关闭音乐
                    self.done = True
                    break
                self.update_snow()
                # 刷新屏幕
                pygame.display.flip()
                pygame.time.Clock().tick(60)
        
        if self.active :
            self.init_snow_list()
            pygame.quit()
            self.done = False
            self.snow_thread = MyThreadFunc(_show_snow)
            self.snow_thread.start()
            self.music(True)
        
# 游戏相关功能
class Game():
    # 初始化
    def __init__(self):
        super().__init__()

        self.game_handle = win32con.NULL  # 动物餐厅父级窗口
        self.game_body = win32con.NULL  # 动物餐厅主体窗口
        self.mode = 'end' # 程序启动模式
        self.stop_active = False # 是否暂停(鼠标在游戏内暂停)
        self.work_thread = False # 工作线程

        self.stop_timer = QTimer()  # 是否暂停（计时器）
        self.stop_timer.timeout.connect(lambda:self.stop())

        self.start_timer = QTimer()  # 是否暂停（计时器）
        self.start_timer.timeout.connect(lambda:self.can_ting())

        self.zx_timer = QTimer()  # 执行脚本（计时器）
        self.zx_timer.timeout.connect(lambda:self.z_x())
    
    # 工作
    def do_work(self,mode = 'end'):
        print('内存引用数量',len(gc.get_objects()))
        # 相同模式不处理
        if self.mode == mode:return
        self.mode = mode
        # 清理所有计时器
        self.stop_timer.stop()
        self.start_timer.stop()
        self.zx_timer.stop()
        # 停止?
        if mode == 'end':
            self.work_thread and self.work_thread.stop()
            return self.m_down([230, 500], True)
        # 开启
        self.get_body()
        # 脚本运行
        if mode == 'start':
            self.can_ting()
            self.start_timer.start(5000) # 5000ms执行一次
            # 游戏暂停
            self.stop_timer.start(10) # 10ms执行一次
        if mode == 'zx':
            self.z_x()
            self.zx_timer.start(40000) # 40000ms执行一次

    # 获取body窗口
    def get_body(self):
        # 从顶层窗口向下搜索主窗口，无法搜索子窗口
        self.game_handle = win32gui.FindWindow(None, "动物餐厅")
        # print('handle',handle)
        if  self.game_handle == 0: return
        # 搜索子窗口
        hwndChildList = []
        win32gui.EnumChildWindows(self.game_handle, lambda hwnd, param: param.append(hwnd), hwndChildList)
        self.game_body = win32gui.FindWindowEx(hwndChildList[0], 0, None, None)
        # 指定句柄设置为前台，也就是激活
        win32gui.SetForegroundWindow(self.game_body)
        # print("body:", self.game_body)

    # 鼠标按下
    def m_down(self,pos, up=True,press_time=0):
        if self.stop_active == True: return
        if press_time != 0:
            self.stop_active == True
        # print(pos)
        tmp = win32api.MAKELONG(pos[0], pos[1])
        # 发送一个消息(目标窗口的句柄,要发送的消息,第一个消息参数,第二个消息参数)
        win32gui.SendMessage(self.game_body, win32con.WM_ACTIVATE, win32con.WA_CLICKACTIVE, 0)  # 激活窗口
        win32gui.SendMessage(self.game_body, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, tmp)  # 鼠标左键按下
        # 是否松开左键
        if up == True:
            # print(press_time)
            if press_time != 0:
                time.sleep(press_time)
                self.stop_active == False
            win32gui.SendMessage(self.game_body, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, tmp)  # 鼠标左键松开
            
    # 暂停 鼠标如果在body内就暂停
    def stop(self):
        if self.mode != 'start':return
        pos = win32api.GetCursorPos()  # 获取鼠标当前位置
        # print(pos)
        hwndPointNow = win32gui.WindowFromPoint(pos)  # 获取鼠标当前窗口句柄
        # 如果在body里面就停止脚本
        # print(self.start_active)
        active = hwndPointNow == self.game_body
        # 如果鼠标处于游戏窗口内 并且之前未暂停
        if active and active != self.stop_active:
            self.m_down([230, 500], True)
        if active:
            self.stop_active = True
        else:
            self.stop_active = False
    
    # 餐厅
    def can_ting(self):
        def _can_ting():
            # 捡垃圾
            time.sleep(0.01)
            self.m_down([random.randint(270,300),random.randint(270,300)], True)
            self.m_down([random.randint(270,300),random.randint(270,300)], True)
            self.m_down([random.randint(100,300),random.randint(570,700)], True)
            self.m_down([random.randint(100,300),random.randint(570,700)], True)
            self.m_down([random.randint(100,300),random.randint(570,700)], True)
            self.m_down([random.randint(100,300),random.randint(570,700)], True)
            self.m_down([random.randint(100,300),random.randint(570,700)], True)

            # 防沉迷
            time.sleep(0.01)
            self.m_down([230, 490], True)

            # 点餐
            time.sleep(0.01)
            self.m_down([130, 380], True)  # 点餐1
            self.m_down([230, 380], True)  # 点餐2
            self.m_down([330, 380], True)  # 点餐3
            self.m_down([130, 500], True)  # 点餐4
            self.m_down([230, 500], True)  # 点餐5
            self.m_down([330, 500], True)  # 点餐6

            # 歌手
            time.sleep(0.01)
            self.m_down([340, 210], True)
            self.m_down([340, 210], True)
            self.m_down([340, 210], True)
            self.m_down([340, 210], True)
            self.m_down([340, 210], True)
            self.m_down([340, 210], True)
            self.m_down([340, 210], True)
            self.m_down([340, 210], True)
            self.m_down([340, 210], True)
            self.m_down([340, 210], True)
            self.m_down([340, 210], True)
            self.m_down([340, 210], True)
            self.m_down([340, 210], True)
            self.m_down([340, 210], True)
            self.m_down([340, 210], True)
            self.m_down([340, 210], True)
            self.m_down([340, 210], True)
            self.m_down([340, 210], True)
            self.m_down([340, 210], True)
            self.m_down([340, 210], True)

            # 宣传
            time.sleep(0.01)
            self.m_down([400, 730], False)
        
        self.work_thread and self.work_thread.stop()
        self.work_thread = MyThreadFunc(_can_ting)
        self.work_thread.start()

    # 涨薪的方法
    def z_x(self):
        def _z_x():
            self.m_down([330, 500], True) # 确定奖励按钮
            time.sleep(1)
            self.m_down([300, 560], True) # 涨薪
            time.sleep(1)
            self.m_down([230, 490], True) # 防沉迷
            self.m_down([230, 490], True) # 防沉迷
            self.m_down([230, 490], True) # 防沉迷
            self.m_down([230, 490], True) # 防沉迷
            self.m_down([230, 490], True) # 防沉迷
            time.sleep(1)
            self.m_down([175, 635], True) # 看广告
            time.sleep(0.2)
            self.m_down([150, 490], True) # 不使用广告券
            time.sleep(35)
            self.m_down([420, 30], True) # 退出广告
        print(self.work_thread)
        self.work_thread and self.work_thread.stop()
        self.work_thread = MyThreadFunc(_z_x)
        self.work_thread.start()

    # 按压
    def press(self,time):
        def _press():
            self.get_body()
            self.m_down([230, 300], True,time)
        self.thread_press = threading.Thread(target=_press)
        self.thread_press.start()

# 窗口挂件
class Pendant(QWidget):

    # 初始化
    def __init__(self):
        super().__init__()
        
        # 主要变量
        self.img_num = 1 # 图片位数
        self.dis_file = "0" # 图片文件夹
        self.img_path = 'images/{file}/{img}.png'.format(file=self.dis_file, img=str(self.img_num)) # 动态路径
        self.img_path = os.path.join(basedir, self.img_path) # 绝对路径
        self.img_count = len(os.listdir(os.path.join(basedir, 'images/{}'.format(self.dis_file)))) # 图片总个数

        self.init_pendant() # 初始化窗口
        self.pendant.mousePressEvent = self.mousePressEvent # 鼠标按下
        self.pendant.mouseMoveEvent = self.mouseMoveEvent # 鼠标拖动

        # 挂载其他功能类
        self.snow = Snow()
        self.game = Game()

        # self.snow.show_snow(True) # 默认开启雪花
        # self.snow.music(True) # 默认开启音乐

        #声明创建右键菜单
        self.pendant.setContextMenuPolicy(Qt.CustomContextMenu)
        self.pendant.customContextMenuRequested.connect(self.create_rightmenu)  # 连接到菜单显示函数

        # 图片更新
        self.timer = QTimer() # 设置一个计时器
        self.timer.timeout.connect(self.img_update)
        self.timer.start(48) # 100ms执行一次

    # 初始化挂件
    def init_pendant(self):
        self.pendant = QLabel() # 创建一个图像标签
        # print(self.pendant)
        self.pendant.resize(300, 300) # 窗口尺寸
        desktop = QApplication.desktop() # 桌面大小
        # print(desktop.width(),'--',desktop.height())
        self.pendant.move(desktop.width()-300, desktop.height()-300) # 窗口初始位置
        self.pendant.pos_first = self.pendant.pos()
        self.pendant.setWindowTitle('动物餐厅【小廖专属】') # 窗口标题
        self.pendant.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow) # 去掉窗口标题栏和按钮并置顶
        self.pendant.setAttribute(Qt.WA_TranslucentBackground, True) # 设置窗口透明
        self.pendant.setAutoFillBackground(False) # 不填充背景
        self.pendant.setCursor(QCursor(Qt.ClosedHandCursor)) # 设置鼠标小手指
        self.pendant.show() # 显示窗口
    
    # 图片更新
    def img_update(self):
        # print(self.img_num)
        if self.img_num < self.img_count-1:
            self.img_num += 1
        else:
            self.img_num = 0
        img_path = 'images/{file}/{img}.png'.format(file=self.dis_file, img=str(self.img_num))
        img_path = os.path.join(basedir, img_path) # 确认basedir路径
        img = QPixmap(img_path)
        self.pendant.setPixmap(img) # 更新图片
    
    # 鼠标首次按下事件
    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.pendant.pos_first = QMouseEvent.globalPos() - self.pendant.pos() # 记录鼠标在窗口的位置
            QMouseEvent.accept()

    # 监听鼠标拖动宠物
    def mouseMoveEvent(self, QMouseEvent):
        # 按住左键拖动
        if Qt.LeftButton:
            # 计算并修改新的位置
            new_pos = QMouseEvent.globalPos() - self.pendant.pos_first
            self.pendant.move(new_pos)
            QMouseEvent.accept()

    # 设置图片模式
    def set_mode(self,mode,time = 48):
        del self.dis_file
        gc.collect()
        self.timer.start(time) # 多久执行一次
        self.dis_file = mode
        self.img_count = len(os.listdir(os.path.join(basedir, 'images/{}'.format(self.dis_file))))

    # 开始工作
    def do_work(self,mode='end'):
        gc.collect()
        self.game.do_work(mode)
        mode == 'start' and self.set_mode('1',48)
        mode == 'end' and self.set_mode('0',48)
        mode == 'zx' and self.set_mode('4',100)

    # 退出
    def quit(self):
        
        self.snow.show_snow(False)
        self.pendant.close()
        sys.exit()

    # 右键菜单
    def create_rightmenu(self):

        #菜单对象
        menu = QMenu(self)

        # 启动
        menu_start = menu.addAction('上班干活啦')
        menu_start.setCheckable(True)
        menu_start.setChecked(self.game.mode=='start')
        menu_start.triggered.connect(lambda:self.do_work('start'))

        # 涨薪
        menu_end = menu.addAction('帮我涨个薪')
        menu_end.setCheckable(True)
        menu_end.setChecked(self.game.mode=='zx')
        menu_end.triggered.connect(lambda:self.do_work('zx'))

        # 结束
        menu_end = menu.addAction('下班睡觉觉')
        menu_end.setCheckable(True)
        menu_end.setChecked(self.game.mode=='end')
        menu_end.triggered.connect(lambda:self.do_work('end'))

        # 按压
        menu_press = menu.addMenu("我爱转圈圈")
        # 子菜单
        menu_press1 =  menu_press.addAction('多跳1格嘛')
        menu_press1.triggered.connect(lambda:self.game.press(0.36))
        menu_press1.setIcon(QIcon(os.path.join(basedir, 'images/num/1.png')))

        menu_press2 =  menu_press.addAction('多跳2格嘛')
        menu_press2.triggered.connect(lambda:self.game.press(0.38))
        menu_press2.setIcon(QIcon(os.path.join(basedir, 'images/num/2.png')))

        menu_press3 =  menu_press.addAction('多跳3格嘛')
        menu_press3.triggered.connect(lambda:self.game.press(0.40))
        menu_press3.setIcon(QIcon(os.path.join(basedir, 'images/num/3.png')))

        menu_press4 =  menu_press.addAction('多跳4格嘛')
        menu_press4.triggered.connect(lambda:self.game.press(0.42))
        menu_press4.setIcon(QIcon(os.path.join(basedir, 'images/num/4.png')))

        menu_press5 =  menu_press.addAction('多跳5格嘛')
        menu_press5.triggered.connect(lambda:self.game.press(0.44))
        menu_press5.setIcon(QIcon(os.path.join(basedir, 'images/num/5.png')))

        menu_press6 =  menu_press.addAction('多跳6格嘛')
        menu_press6.triggered.connect(lambda:self.game.press(0.46))
        menu_press6.setIcon(QIcon(os.path.join(basedir, 'images/num/6.png')))

        menu_press7 =  menu_press.addAction('多跳7格嘛')
        menu_press7.triggered.connect(lambda:self.game.press(0.48))
        menu_press7.setIcon(QIcon(os.path.join(basedir, 'images/num/7.png')))

        menu_press8 =  menu_press.addAction('多跳8格嘛')
        menu_press8.triggered.connect(lambda:self.game.press(0.50))
        menu_press8.setIcon(QIcon(os.path.join(basedir, 'images/num/8.png')))

        # 修改主题
        menu_set = menu.addMenu("换个好心情")
        # 子菜单
        menu_set0 =  menu_set.addAction('圣诞老人姜饼人')
        menu_set0.setCheckable(True)
        menu_set0.setChecked(self.dis_file=='0')
        menu_set0.triggered.connect(lambda:self.set_mode('0',48))
        menu_set0.setIcon(QIcon(os.path.join(basedir, 'images/0/0.png')))

        menu_set1 =  menu_set.addAction('圣诞老人送礼物')
        menu_set1.setCheckable(True)
        menu_set1.setChecked(self.dis_file=='1')
        menu_set1.triggered.connect(lambda:self.set_mode('1',48))
        menu_set1.setIcon(QIcon(os.path.join(basedir, 'images/1/0.png')))

        menu_set2 =  menu_set.addAction('圣诞树又闪又跳')
        menu_set2.setCheckable(True)
        menu_set2.setChecked(self.dis_file=='2')
        menu_set2.triggered.connect(lambda:self.set_mode('2',30))
        menu_set2.setIcon(QIcon(os.path.join(basedir, 'images/2/0.png')))

        menu_set3 =  menu_set.addAction('我想拥有一个家')
        menu_set3.setCheckable(True)
        menu_set3.setChecked(self.dis_file=='3')
        menu_set3.triggered.connect(lambda:self.set_mode('3',48))
        menu_set3.setIcon(QIcon(os.path.join(basedir, 'images/3/0.png')))

        menu_set4 =  menu_set.addAction('小小企鹅飞呀飞')
        menu_set4.setCheckable(True)
        menu_set4.setChecked(self.dis_file=='4')
        menu_set4.triggered.connect(lambda:self.set_mode('4',100))
        menu_set4.setIcon(QIcon(os.path.join(basedir, 'images/4/0.png')))

        menu_set5 =  menu_set.addAction('圣诞大礼包到啦')
        menu_set5.setCheckable(True)
        menu_set5.setChecked(self.dis_file=='5')
        menu_set5.triggered.connect(lambda:self.set_mode('5',48))
        menu_set5.setIcon(QIcon(os.path.join(basedir, 'images/5/0.png')))

        menu_set6 =  menu_set.addAction('我的雪人晃啊晃')
        menu_set6.setCheckable(True)
        menu_set6.setChecked(self.dis_file=='6')
        menu_set6.triggered.connect(lambda:self.set_mode('6',48))
        menu_set6.setIcon(QIcon(os.path.join(basedir, 'images/6/0.png')))

        menu_set7 =  menu_set.addAction('你的雪人摇啊摇')
        menu_set7.setCheckable(True)
        menu_set7.setChecked(self.dis_file=='7')
        menu_set7.triggered.connect(lambda:self.set_mode('7',48))
        menu_set7.setIcon(QIcon(os.path.join(basedir, 'images/7/0.png')))

        menu_set8 =  menu_set.addAction('我是雪人好快乐')
        menu_set8.setCheckable(True)
        menu_set8.setChecked(self.dis_file=='8')
        menu_set8.triggered.connect(lambda:self.set_mode('8',48))
        menu_set8.setIcon(QIcon(os.path.join(basedir, 'images/8/0.png')))

        menu_set9 =  menu_set.addAction('雪人宝宝胖嘟嘟')
        menu_set9.setCheckable(True)
        menu_set9.setChecked(self.dis_file=='9')
        menu_set9.triggered.connect(lambda:self.set_mode('9',36))
        menu_set9.setIcon(QIcon(os.path.join(basedir, 'images/9/0.png')))

        menu_set10 =  menu_set.addAction('圣诞节我不孤单')
        menu_set10.setCheckable(True)
        menu_set10.setChecked(self.dis_file=='10')
        menu_set10.triggered.connect(lambda:self.set_mode('10',48))
        menu_set10.setIcon(QIcon(os.path.join(basedir, 'images/10/0.png')))

        menu_set11 =  menu_set.addAction('棒棒糖都是我的')
        menu_set11.setCheckable(True)
        menu_set11.setChecked(self.dis_file=='11')
        menu_set11.triggered.connect(lambda:self.set_mode('11',48))
        menu_set11.setIcon(QIcon(os.path.join(basedir, 'images/11/0.png')))

        menu_set12 =  menu_set.addAction('圣诞伙伴欢乐多')
        menu_set12.setCheckable(True)
        menu_set12.setChecked(self.dis_file=='12')
        menu_set12.triggered.connect(lambda:self.set_mode('12',48))
        menu_set12.setIcon(QIcon(os.path.join(basedir, 'images/12/0.png')))

        menu_set13 =  menu_set.addAction('我要是DJ就好啦')
        menu_set13.setCheckable(True)
        menu_set13.setChecked(self.dis_file=='13')
        menu_set13.triggered.connect(lambda:self.set_mode('13',24))
        menu_set13.setIcon(QIcon(os.path.join(basedir, 'images/13/0.png')))

        menu_set14 =  menu_set.addAction('咚嗒嗒咚咚哒哒')
        menu_set14.setCheckable(True)
        menu_set14.setChecked(self.dis_file=='14')
        menu_set14.triggered.connect(lambda:self.set_mode('14',16))
        menu_set14.setIcon(QIcon(os.path.join(basedir, 'images/14/0.png')))

        menu_set15 =  menu_set.addAction('让我们一起摇摆')
        menu_set15.setCheckable(True)
        menu_set15.setChecked(self.dis_file=='15')
        menu_set15.triggered.connect(lambda:self.set_mode('15',36))
        menu_set15.setIcon(QIcon(os.path.join(basedir, 'images/15/0.png')))

        menu_set16 =  menu_set.addAction('给你一个大苹果')
        menu_set16.setCheckable(True)
        menu_set16.setChecked(self.dis_file=='16')
        menu_set16.triggered.connect(lambda:self.set_mode('16',32))
        menu_set16.setIcon(QIcon(os.path.join(basedir, 'images/16/0.png')))

        menu_set17 =  menu_set.addAction('圣诞必须快乐呀')
        menu_set17.setCheckable(True)
        menu_set17.setChecked(self.dis_file=='17')
        menu_set17.triggered.connect(lambda:self.set_mode('17',32))
        menu_set17.setIcon(QIcon(os.path.join(basedir, 'images/17/0.png')))

        # 雪花
        menu_snow = menu.addAction('雪花飘啊飘')
        menu_snow.setCheckable(True)
        menu_snow.setChecked(self.snow.active)
        menu_snow.triggered.connect(lambda:self.snow.show_snow(not self.snow.active))

        # 音乐
        menu_snow_music = menu.addAction('来点儿音乐')
        menu_snow_music.setCheckable(True)
        menu_snow_music.setChecked(self.snow.music_active)
        menu_snow_music.triggered.connect(lambda:self.snow.music(not self.snow.music_active))

        # 退出
        menu_quit = menu.addAction('晚安小点点')
        menu_quit.triggered.connect(lambda:self.quit())

        menu.popup(QCursor.pos()) # 声明当鼠标在groupBox控件上右击时，在鼠标位置显示右键菜单   ,exec_,popup两个都可以，

if __name__ == '__main__':

    app = QApplication(sys.argv) # 创建一个应用程序对象
    pendant = Pendant()

    sys.exit(app.exec_()) # 系统exit()方法确保应用程序干净的退出

# pyinstaller -F -i images/logo/icon.ico 动物餐厅辅助2.0.spec --noconsole