import os
import sys
from PyQt5.QtGui import QPixmap,QCursor,QIcon
from PyQt5.QtCore import QTimer,Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,QMenu

basedir = ''
#根据系统运行位置确认basedir路径
if getattr(sys, 'frozen', None):
    basedir = sys._MEIPASS
else:
    basedir = os.path.dirname(__file__)

# 窗口挂件
class Pendant(QWidget):

    # 初始化
    def __init__(self):
        super().__init__()
        
        # 主要变量
        self.img_num = 1 # 图片数量
        self.dis_file = "0" # 图片文件夹
        self.img_path = 'images/{file}/{img}.png'.format(file=self.dis_file, img=str(self.img_num)) # 动态路径
        self.img_path = os.path.join(basedir, self.img_path) # 绝对路径
        self.img_count = len(os.listdir(os.path.join(basedir, 'images/{}'.format(self.dis_file))))
        # 初始化函数
        # self.create_w()
        self.init_pendant()
        
        self.pendant.mousePressEvent = self.mousePressEvent # 鼠标按下
        self.pendant.mouseMoveEvent = self.mouseMoveEvent # 鼠标拖动

        # 声明创建右键菜单
        self.pendant.setContextMenuPolicy(Qt.CustomContextMenu)
        self.pendant.customContextMenuRequested.connect(self.create_rightmenu)  # 连接到菜单显示函数

        
        self.timer = QTimer() # 设置一个计时器
        self.timer.timeout.connect(self.img_update)
        self.timer.start(48) # 100ms执行一次


    # 初始化挂件
    def init_pendant(self):
        self.pendant = QLabel() # 创建一个图像标签
        self.pendant.resize(300, 300) # 窗口尺寸
        self.pendant.move(1720, 760) # 窗口初始位置
        self.pendant.pos_first = self.pendant.pos()
        self.pendant.setWindowTitle('动物餐厅【CC专属】') # 窗口标题
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

        self.img_path = 'images/{file}/{img}.png'.format(file=self.dis_file, img=str(self.img_num))
        self.img_path = os.path.join(basedir, self.img_path) # 确认basedir路径
        # print(self.img_path)
        self.qpixmap = QPixmap(self.img_path)
        self.pendant.setPixmap(self.qpixmap)

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
        self.timer.start(time) # 多久执行一次
        self.dis_file = mode
        self.img_count = len(os.listdir(os.path.join(basedir, 'images/{}'.format(self.dis_file))))

    # 退出
    def quit(self):
        self.close()
        sys.exit()

    # 右键菜单
    def create_rightmenu(self):

        #菜单对象
        menu = QMenu(self)

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

        # 退出
        menu_quit = menu.addAction('晚安小点点')
        menu_quit.triggered.connect(lambda:self.quit())

        menu.popup(QCursor.pos()) # 声明当鼠标在groupBox控件上右击时，在鼠标位置显示右键菜单   ,exec_,popup两个都可以，


if __name__ == '__main__':

    app = QApplication(sys.argv) # 创建一个应用程序对象
    pendant = Pendant()
    sys.exit(app.exec_()) # 系统exit()方法确保应用程序干净的退出

# pyinstaller -F -i images/logo/icon.ico 桌面挂件.spec --noconsole