import os
import sys
import random
from PyQt5.QtGui import QIcon,QMovie,QCursor
from PyQt5.QtCore import Qt,QSize,QTimer,QUrl
from PyQt5.QtWidgets import QWidget,QAction,QMenu,QSystemTrayIcon,QLabel,QDesktopWidget,qApp,QApplication
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
 
class DesktopPet(QWidget):
    def __init__(self, parent=None, **kwargs):
        super(DesktopPet, self).__init__(parent)
        # 窗体初始化
        self.init()
        # 托盘化初始
        self.initPall()
        # 宠物静态gif图加载
        self.initPetImage()
        # 宠物正常待机，实现随机切换动作
        self.petNormalAction()
 
 
    # 窗体初始化
    def init(self):
         # 初始化
         # 设置窗口属性:窗口无标题栏且固定在最前面
         # FrameWindowHint:无边框窗口
         # WindowStaysOnTopHint: 窗口总显示在最上面
         # SubWindow: 新窗口部件是一个子窗口，而无论窗口部件是否有父窗口部件
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
         # setAutoFillBackground(True)表示的是自动填充背景,False为透明背景
        self.setAutoFillBackground(False)
         # 窗口透明，窗体空间不透明
        self.setAttribute(Qt.WA_TranslucentBackground, True)
         # 重绘组件、刷新
        self.repaint()
 
     # 托盘化设置初始化
    def initPall(self):
         # 导入准备在托盘化显示上使用的图标
        icons = os.path.join('./icon/icon_pall.png')
        icons_1 = os.path.join('./icon/skill_1.jpg')
        icons_2 = os.path.join('./icon/skill_2.jpg')
         # 设置右键显示最小化的菜单项
         # 菜单项退出，点击后调用quit函数，并设置这个点击选项的图片
        quit_action = QAction('退出', self, triggered=self.quit)   
        quit_action.setIcon(QIcon(icons_1))
         # 菜单项显示，点击后调用showing函数，并设置‘显示’项的图片
        showing = QAction(u'显示', self, triggered=self.showwin)
        showing.setIcon(QIcon(icons_2))
         # 新建一个菜单项控件
        self.tray_icon_menu = QMenu(self)
         # 在菜单栏添加一个无子菜单的菜单项‘退出’
        self.tray_icon_menu.addAction(quit_action)
         # 在菜单栏添加一个无子菜单的菜单项‘显示’
        self.tray_icon_menu.addAction(showing)
        # QSystemTrayIcon类为应用程序在系统托盘中提供一个图标
        self.tray_icon = QSystemTrayIcon(self)
        # 设置托盘化图标
        self.tray_icon.setIcon(QIcon(icons))
        # 设置托盘化菜单项
        self.tray_icon.setContextMenu(self.tray_icon_menu)
        # 展示
        self.tray_icon.show()
 
    # 宠物静态gif图加载
    def initPetImage(self):
        # 对话框定义
        self.talkLabel = QLabel(self)
        # 定义显示图片部分
        self.image = QLabel(self)
        # QMovie是一个可以存放动态视频的类，一般是配合QLabel使用的,可以用来存放GIF动态图
        self.movie = QMovie("./special/normal.gif")
        # 设置标签大小
        self.movie.setScaledSize(QSize(200, 200))
        # 将Qmovie在定义的image中显示
        self.image.setMovie(self.movie)
        self.movie.start()
        self.resize(1024, 1024)
        # 调用自定义的randomPosition，会使得宠物出现位置随机
        self.randomPosition()
        # 展示
        self.show()
        # 将宠物正常待机状态的动图放入pet1中
        self.pet1 = []
        for i in os.listdir("./normal/"):
            self.pet1.append("./normal/" + i)
        # 将宠物正常待机状态的对话放入pet2中
        self.dialog = []
        # 读取目录下dialog文件
        with open("./text/dialog.txt", "r",encoding='UTF-8') as f:
            text = f.read()
            # 以; 即换行符为分隔符，分割放进dialog中
            self.dialog = text.split(";")
        #读取触摸文本文件
        self.touch = []
        with open("./text/touch.txt", "r",encoding='UTF-8') as f:
            text = f.read()
            self.touch = text.split(";")
 
    # 宠物正常待机动作
    def petNormalAction(self):
        # 每隔一段时间做个动作
        # 定时器设置
        self.timer = QTimer()
        # 宠物状态设置为动作
        self.timer.timeout.connect(lambda:self.randomAct(3))
        # 动作时间切换设置
        self.timer.start(30000)#30秒
        # 每隔一段时间切换对话
        self.talkTimer = QTimer()
        self.talkTimer.timeout.connect(lambda:self.talk(3))
        self.talkTimer.start(5000)#50秒
        # 对话状态设置为常态
        # 宠物对话框
        self.talkTimer.timeout.connect(lambda:self.audio(0,dialogChoose= random.randint(0,4)))

    # 随机动作切换
    def randomAct(self,model):        
        # model记录宠物状态，宠物状态为0时，代表正常待机
        if model == 0:
            self.movie = QMovie("./special/normal.gif")
            self.movie.setScaledSize(QSize(200, 200))
            self.image.setMovie(self.movie)
            self.movie.start()
        elif model == 1: #触摸
            # 读取特殊状态图片路径
            self.movie = QMovie("./special/touch.gif")
            # 宠物大小
            self.movie.setScaledSize(QSize(200, 200))
            # 将动画添加到label中
            self.image.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()
            self.touchTimer = QTimer()
            self.touchTimer.start(600)
            self.touchTimer.timeout.connect(lambda:self.randomAct(0))
            self.touchTimer.timeout.connect(self.touchTimer.stop)
        elif model == 2: #拖拽
            self.movie = QMovie("./special/tuozhuai.gif")
            self.movie.setScaledSize(QSize(200, 200))
            self.image.setMovie(self.movie)
            self.movie.start()
        elif model == 3: #随机动作
            # 随机选择装载在pet1里面的gif图进行展示，实现随机切换
            self.gifChoose = random.randint(0,1)
            self.movie = QMovie(self.pet1[self.gifChoose])
            # 宠物大小
            self.movie.setScaledSize(QSize(200, 200))
            # 将动画添加到label中
            self.image.setMovie(self.movie)
            # 开始播放动画
            self.movie.start()
            self.gifTimer = QTimer()
            if self.gifChoose == 0:
                self.gifTimer.start(9000)   
            elif self.gifChoose == 1:
                self.gifTimer.start(7000)
            self.gifTimer.timeout.connect(lambda:self.randomAct(0))
            self.gifTimer.timeout.connect(self.gifTimer.stop)

    # 宠物对话框行为处理
    def talk(self,model,dialogChoose = 0,touchChoose = 0):
        if model == 0: 
            # model为0则选取加载在dialog中的语句
            self.talkLabel.setText(self.dialog[dialogChoose])
            #设置语音模式
            #播放语音
            #消除字幕
            self.talkTimer = QTimer()
            if dialogChoose == 0:
                self.talkTimer.start(17000)
            elif dialogChoose == 1:
                self.talkTimer.start(15000)
            elif dialogChoose == 2:
                self.talkTimer.start(10000)
            elif dialogChoose == 3:
                self.talkTimer.start(19000)
            elif dialogChoose == 4:
                self.talkTimer.start(28000)
            #self.talkTimer.timeout.connect(lambda:self.talk(3))
            #self.talkTimer.timeout.connect(self.talkTimer.stop)
        elif model == 1:
            #model为1选取触摸语句
            self.talkLabel.setText(self.touch[touchChoose])
            #播放语音 触摸
            # 消除字幕
            self.talkTimer = QTimer()
            if touchChoose == 0:
                self.talkTimer.start(5000)#5秒
            elif touchChoose == 1:
                self.talkTimer.start(2000)
            elif touchChoose == 2:
                self.talkTimer.start(6000)
            elif touchChoose == 3:
                self.talkTimer.start(13000)
        
        elif model == 3: #消除字幕
            self.talkLabel.setText("")
         # 设置样式
        
        self.talkLabel.setStyleSheet(
            "font: bold;"
            "font:25px '微软雅黑';"
            "color:#00BFFF;"
            "background:transparent"
            "url(:/)"
        )
        
        # 根据内容自适应大小
        self.talkTimer.timeout.connect(lambda:self.talk(3))
        self.talkTimer.timeout.connect(self.talkTimer.stop)
        self.talkLabel.adjustSize()
    #语音模块
    def audio(self,model,dialogChoose = 0,touchChoose = 0):
        self.player = QMediaPlayer()
        if model == 0: #dialog语音
            self.talk(0,dialogChoose= dialogChoose)
            if dialogChoose == 0:
                self.audioPlay = QMediaContent(QUrl.fromLocalFile('./Audio/dialog/main_1.wav'))
            elif dialogChoose == 1:
                self.audioPlay = QMediaContent(QUrl.fromLocalFile('./Audio/dialog/main_2.wav'))
            elif dialogChoose == 2:
                self.audioPlay = QMediaContent(QUrl.fromLocalFile('./Audio/dialog/main_3.wav'))
            elif dialogChoose == 3:
                self.audioPlay = QMediaContent(QUrl.fromLocalFile('./Audio/dialog/main_4_ex1100.wav'))
            elif dialogChoose == 4:
                self.audioPlay = QMediaContent(QUrl.fromLocalFile('./Audio/dialog/main_5_ex1100.wav'))
        elif model == 1: #触摸
            self.talk(1,touchChoose= touchChoose)
            if touchChoose == 0:
                self.audioPlay = QMediaContent(QUrl.fromLocalFile('./Audio/touch/touch_1.wav'))
            #取得音频文件
            elif touchChoose == 1:
                self.audioPlay = QMediaContent(QUrl.fromLocalFile('./Audio/touch/touch_1_ex1100.wav'))
            elif touchChoose == 2:
                self.audioPlay = QMediaContent(QUrl.fromLocalFile('./Audio/touch/touch_2.wav'))
            elif touchChoose == 3:
                self.audioPlay = QMediaContent(QUrl.fromLocalFile('./Audio/touch/touch_2_ex1100.wav'))
        #播放
        self.player.setMedia(self.audioPlay)
        self.player.play()
    # 退出操作，关闭程序
    def quit(self):
        self.close()
        sys.exit()
 
    # 显示宠物
    def showwin(self):
        # setWindowOpacity（）设置窗体的透明度，通过调整窗体透明度实现宠物的展示和隐藏
        self.setWindowOpacity(1)
 
    # 宠物随机位置
    def randomPosition(self):
        screen_geo = QDesktopWidget().screenGeometry()
        pet_geo = self.geometry()
        width = (screen_geo.width() - pet_geo.width()) * random.random()
        height = (screen_geo.height() - pet_geo.height()) * random.random()
        self.move(int(width), int(height))
 
    # 鼠标左键按下时, 宠物将和鼠标位置绑定
    def mousePressEvent(self, event):        
        if event.button() == Qt.LeftButton:
            self.start_pos = event.globalPos()
            self.is_follow_mouse = True
            self.timer.stop()
            self.talkTimer.stop()
        # globalPos() 事件触发点相对于桌面的位置
        # pos() 程序相对于桌面左上角的位置，实际是窗口的左上角坐标
        self.mouse_drag_pos = event.globalPos() - self.pos()
        event.accept()
        # 拖动时鼠标图形的设置
        self.setCursor(QCursor(Qt.OpenHandCursor))
 
    def mouseMoveEvent(self, event):
        try:
            if Qt.LeftButton and self.is_follow_mouse:
                self.move(event.globalPos() - self.mouse_drag_pos)
            #宠物状态设置为2，播放拖拽动画
                self.randomAct(2)
        except AttributeError:
            event.accept()
        finally:
            event.accept()
        
        
 
    # 鼠标释放调用，取消绑定
    def mouseReleaseEvent(self, event):
        self.is_follow_mouse = False
        # 鼠标图形设置为箭头
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.timer.start()#重启计时
        self.talkTimer.start()
        try:
            #判断点击 播放触摸动画和语音
            if self.start_pos == event.globalPos():
                self.audio(1,touchChoose = random.randint(0,3))
                self.randomAct(1)
            #拖拽 恢复
            else:
                self.randomAct(0)
        except AttributeError:
            self.randomAct(0)
    # 鼠标移进时调用
    def enterEvent(self, event):
        # 设置鼠标形状 Qt.ClosedHandCursor   非指向手
        self.setCursor(Qt.ClosedHandCursor)
 
    # 宠物右键点击交互
    def contextMenuEvent(self, event):
        # 定义菜单
        menu = QMenu(self)
        # 定义菜单项
        quitAction = menu.addAction("退出")
        hide = menu.addAction("隐藏")
        # 使用exec_()方法显示菜单。从鼠标右键事件对象中获得当前坐标。mapToGlobal()方法把当前组件的相对坐标转换为窗口（window）的绝对坐标。
        action = menu.exec_(self.mapToGlobal(event.pos()))
        # 点击事件为退出
        if action == quitAction:
            qApp.quit()
        # 点击事件为隐藏
        if action == hide:
            # 通过设置透明度方式隐藏宠物
            self.setWindowOpacity(0)
 
 
if __name__ == '__main__':
    # 创建了一个QApplication对象，对象名为app，带两个参数argc,argv
    # 所有的PyQt5应用必须创建一个应用（Application）对象。sys.argv参数是一个来自命令行的参数列表。
    app = QApplication(sys.argv)
    # 窗口组件初始化
    pet = DesktopPet()
    # 1. 进入时间循环；
    # 2. wait，直到响应app可能的输入；
    # 3. QT接收和处理用户及系统交代的事件（消息），并传递到各个窗口；
    # 4. 程序遇到exit()退出时，机会返回exec()的值。
    sys.exit(app.exec_())



