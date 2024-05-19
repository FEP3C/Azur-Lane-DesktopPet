# Azur-Lane-DesktopPet

## 文件结构说明

```
Azur-Lane-DesktopPet/
│
├── /icons           # 托盘图标
├──/normal      # 待机状态下每隔一段时间触发动作
├──/special     # 特定情况下动作
│
├── LICENSE          # 项目的开源许可证文件
├── README.md        # 本项目介绍文件
├── touch.txt        # 角色触摸对话文本文件
├── dialog.txt       # 角色互动对话文本文件
└── xingzuo.py       # 主程序
```
# 使用
安装PyQt5
```Python
pip install PyQt5
```
运行"xingzuo.py"文件
```Python
python xingzuo.py
```
# 拓展
可通过替换文件并修改部分数据将其换成自己喜欢的角色
```
第151行
self.gif_number = random.randint(0,1)
self.movie = QMovie(self.pet1[self.gif_number])
......
if self.gif_number == 0:
    self.gifTimer.start(9000)   
elif self.gif_number == 1:
    self.gifTimer.start(7000)
```
其中需要修改随机数的范围和计时器时长，使替换后的gif文件能在播放完一次后结束
# 后续目标
搓一个控制面板，调整大小、动作模式等
可在屏幕上左右滑行
播放语音

# 许可证
本项目遵循[MIT License](LICENSE)，意在鼓励开源精神，促进技术交流与学习。

# 参考
参考博文https://blog.csdn.net/zujiasheng/article/details/124670676
