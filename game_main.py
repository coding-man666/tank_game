'''
1. 安装 pygame 引擎(一个用于开发游戏的包)
    命令行安装: pip install pygame
    
2. 明白需求(基于面向对象编程的分析)
    1) 有哪些类:
        a. 主逻辑类(入口类)
            开始游戏
            结束游戏
        b. 坦克类(包括: 公共坦克父类,我方坦克子类,敌方坦克子类)
            展示
            移动
            射击
        c. 子弹类
            展示
            移动
        d. 爆炸效果类
            展示爆炸效果
        e. 墙壁类
            属性: 是否可以通过
        f. 音效类
            播放音乐
            
3. 坦克大战项目框架的搭建
    涉及到的类，用代码简单的实现
4. 版本更迭及功能增减
    v1.5 ---> 创建游戏主窗口，填充黑色背景
    v1.8 ---> 点击关闭按钮，退出程序
              方向控制，子弹发射
    v1.89 ---> 实现游戏窗口左上角的文字提示，需要导入 font
    v2.0 ---> 加载我方坦克
    v2.2 ---> 新增坦克移动速度属性 speed(控制坦克移动的快慢)
              完善事件处理功能: 1. 根据事件改变坦克方向 2. 修改坦克的位置(left,top,且受到移动速度的影响)
    v2.3 ---> 优化功能:
                解决 bug: 坦克可以移出窗口边界
    v2.5 ---> 优化功能:
                1. 改变坦克的移动方式:
                    1.1 按下方向键，坦克持续移动
                    1.2 松开方向键，坦克停下来
    v2.8 ---> 新增敌方坦克:
                    1. 完善敌方坦克类
                    2. 创建敌方坦克，将敌方坦克展示到窗口中
    v3.0 ---> 1. 优化: 窗口左上角显示的剩余敌方坦克数量
              2. 实现敌方坦克的移动
                随机移动(在某一个方向移动一定距离之后，随机更改移动方向)
    v3.4 ---> 完善子弹类的封装
    v3.5 ---> 完善子弹的反射功能
                我方 tank 发射子弹 -> 产生一颗子弹
    v3.6 ---> 实现子弹的移动
    v3.8 ---> 优化:
                1. 子弹打中墙壁(窗口边界)的时候，直接消除而不是粘在墙上
                2. 解决我方坦克可以无限发射子弹的问题 --> 子弹要限量
    v3.9 ---> 新增功能: 让敌方坦克可以发射子弹
    v3.92 ---> 实现我方子弹与敌方坦克碰撞的相关功能(我方子弹消亡，敌方坦克消亡)
                    使用 pygame 提供的精灵类(pygame.sprite.Sprite)中的碰撞算法实现
                        --> 需要 Bullet,Tank 继承精灵类
                            --> 为了能够更灵活的添加方法，我们可以使用中间类 ( Bullet,Tank 继承 ->中间类 继承 -> 精灵类)
    v4.0 ---> 新增功能:
                1. 实现爆炸效果类
                2. 实现我方子弹击中敌方坦克，使敌方坦克爆炸
    v4.3 ---> 新增功能:
                1. 实现敌方子弹与我方坦克的碰撞
                2. 以及我方坦克爆炸效果的实现
    v4.8 ---> 新增功能:
                1. 我方坦克死亡之后，点击 R 键重生
    v5.2 ---> 新增功能:
                1. 实现墙壁类
                2. 将随机创建的墙壁对象，加入到窗口
                   创建墙壁对象，加入到墙壁列表中
    v5.3 ---> 修改 bug: 子弹会穿墙
                实现双方坦克的子弹都不能穿墙的设定
    v5.4 ---> 修改 bug: 坦克可以穿墙
    v5.6 ---> 新增功能:
                实现坦克之间的碰撞检测
                    1. 我方坦克主动碰撞到敌方坦克
                            我方坦克停下来 back()
                    2. 敌方坦克主动碰撞到我方坦克
                            敌方坦克停下来 back()
    v6.0 ---> 新增功能
                背景音效
'''
import random
import time
import pygame

# 重命名
_display = pygame.display
# 黑色
COLOR_BLACK = pygame.Color(0, 0, 0, 0)
# 红色
COLOR_RED = pygame.Color(255, 0, 0, 0)
# 游戏版本号
version = 'v2.2'
# 主逻辑类
class MainGame():
    # 游戏主窗口对象
    window = None
    # 窗口宽高
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 500
    # 创建我方坦克一辆
    MY_TANK = None
    # 存储敌方坦克的列表
    ENEMY_TANKS_LIST = []
    # 创建敌方坦克的数量
    enemy_tanks_count = 5
    # 存储我方坦克的子弹列表
    bullet_list = []
    # 敌方坦克的子弹列表
    enemy_bullet_list = []
    # 爆炸效果列表
    explode_list = []
    # 墙壁列表
    wall_list = []

    def __init__(self):
        pass

    # 开始游戏方法
    def start_game(self):
        # 窗口初始化
        _display.init()
        # 创建窗口加载窗口(借鉴官方文档)
        MainGame.window = _display.set_mode((MainGame.SCREEN_WIDTH,MainGame.SCREEN_HEIGHT)) # set_mode(tuple|list)
        # 创建我方坦克
        self.create_my_tank()
        # 创建敌方坦克
        self.create_enemy_tank()
        # 创建墙壁
        self.create_walls()
        # 设置游戏标题
        _display.set_caption('坦克大战 %s'%version)
        # 设置死循环，让窗口长时间显示
        while True:
            # 窗口填充黑色背景
            MainGame.window.fill(COLOR_BLACK)
            # 事件的获取
            self.get_envent()
            # 将绘制文字得到的小画布，粘贴到窗口中
            MainGame.window.blit(self.get_text_surface('剩余敌方坦克%d辆'%len(MainGame.ENEMY_TANKS_LIST)),(5,5))
            # 加入墙壁到窗口中
            self.blit_walls()
            if MainGame.MY_TANK and MainGame.MY_TANK.is_live:
                # 将我方坦克加入到窗口中
                MainGame.MY_TANK.display_tank()
                # 如果撞墙，则将我方坦克坐标还原
                MainGame.MY_TANK.tank_hit_wall()
                # 检测我方坦克是否撞到敌方坦克
                MainGame.MY_TANK.hit_enemy_tank()
            else:
                # 删除我方坦克，并重置为 None
                del MainGame.MY_TANK
                MainGame.MY_TANK = None
            # 加入敌方坦克到窗口中
            self.blit_enemy_tank()
            # 坦克根据停止的状态，发生移动或停止不动
            if MainGame.MY_TANK and not MainGame.MY_TANK.is_stop:
                MainGame.MY_TANK.move()
            # 将我方子弹渲染到窗口中
            self.blit_bullet()
            # 将敌方子弹渲染到窗口中
            self.blit_enemy_bullet()
            # 展示爆炸效果
            self.display_explodes()
            # 通过线程休眠，使坦克移动速度降低(也可以直接修改坦克的 speed 属性值)
            time.sleep(0.03) # 参数是几秒钟 使线程(死循环)休眠30毫秒再重新启动
            # 窗口的刷新
            _display.update()

    # 设置窗口左上角文字提示功能的方法
    def get_text_surface(self,text):
        # 初始化字体模块
        pygame.font.init()
        # 查看系统支持的所有字体
        # fontList = pygame.font.get_fonts()
        # print(fontList)
        # 选中一个合适的字体
        font = pygame.font.SysFont('方正粗黑宋简体',18)
        # 使用对应的字符完成相关内容的绘制
        # 方法返回一个画布对象
        text_surface = font.render(text,True,COLOR_RED)
        return text_surface

    # 创建我方坦克的方法
    def create_my_tank(self):
        MainGame.MY_TANK = MyTank(400, 400)
        # 创建音乐对象
        music = Music('audio/background.mp3')
        # 调用播放音乐的方法
        music.play()

    # 用于创建敌方坦克的方法
    def create_enemy_tank(self):
        # 让敌方坦克出生时，处于同一水平线上，但位置随机
        top = 100 # 固定的纵坐标
        for i in range(MainGame.enemy_tanks_count):
            speed = random.randint(3, 6)  # 随机的移动速度
            # 每次随机生成 left 值
            left = random.randint(1, 7)  # 随机数最大不超过8，将来要 * 100
            # 创建一个敌方坦克对象
            e_tank = EnemyTank(left * 100,top,speed)
            MainGame.ENEMY_TANKS_LIST.append(e_tank)

    # 用于将敌方坦克加入到窗口的方法
    def blit_enemy_tank(self):
        for e_tank in MainGame.ENEMY_TANKS_LIST:
            # 如果此坦克还存活
            if e_tank.is_live:
                e_tank.display_tank()
                # 敌方坦克移动
                e_tank.rand_move()
                # 检测敌方坦克是否撞墙
                e_tank.tank_hit_wall()
                if MainGame.MY_TANK:
                    # 检测是否撞到我方坦克
                    e_tank.hit_my_tank()
                # 调用敌方坦克的射击方法
                # 获得一颗敌方子弹
                e_bullet = e_tank.shot()
                # 如果获得的子弹不为 None
                if e_bullet:
                    # 将敌方坦克子弹存储到敌方子弹列表中
                    MainGame.enemy_bullet_list.append(e_bullet)
            else: # 如果此坦克已死亡
                MainGame.ENEMY_TANKS_LIST.remove(e_tank)

    # 将墙壁加入到窗口中的方法
    def blit_walls(self):
        for wall in MainGame.wall_list:
            # 如果墙壁仍然存在
            if wall.is_live:
                wall.display_wall()
            else:
                # 否则从列表中删除它
                MainGame.wall_list.remove(wall)

    # 将我方子弹加入到窗口中
    def blit_bullet(self):
        for bullet in MainGame.bullet_list:
            # 如果子弹存活，则显示子弹，并让其移动，否则，将该子弹从列表中删除
            if bullet.is_live:
                # 显示子弹
                bullet.display_bullet()
                # 子弹移动
                bullet.bullet_move()
                # 我方子弹进行碰撞检测
                bullet.hit_enemy_tank()
                # 检测我方子弹是否撞墙
                bullet.hit_walls()
            else:
                MainGame.bullet_list.remove(bullet)
    # 将敌方子弹加入到窗口中
    def blit_enemy_bullet(self):
        for bullet in MainGame.enemy_bullet_list:
            # 如果子弹存活，则显示子弹，并让其移动，否则，将该子弹从列表中删除
            if bullet.is_live:
                # 显示子弹
                bullet.display_bullet()
                # 子弹移动
                bullet.bullet_move()
                # 检测敌方子弹是否击中我方坦克
                if MainGame.MY_TANK and MainGame.MY_TANK.is_live:
                    bullet.hit_my_tank()
                # 检测敌方子弹是否撞墙
                bullet.hit_walls()
            else:
                MainGame.enemy_bullet_list.remove(bullet)

    # 创建墙壁的方法
    def create_walls(self):
        for i in range(6):
            wall = Wall(180 * i,250)
            MainGame.wall_list.append(wall)

    # 新增展示所有爆炸效果的方法
    def display_explodes(self):
        for explode in MainGame.explode_list:
            if explode.is_live:
                explode.display_explode()
            else:
                MainGame.explode_list.remove(explode)

    # 获取程序运行期间的所有事件(鼠标事件、键盘事件)
    def get_envent(self):
        # 1. 获取所有事件
        event_list = pygame.event.get()
        # 2. 对事件类型进行判断处理(1. 点击关闭按钮 2. 按下键盘上的某个按键)
        for event in event_list:
            # 判断 event.type 是否是 QUIT,如果是退出的话，直接调用程序结束的方法
            if event.type == pygame.QUIT:
                # 如果使用鼠标单击窗口的关闭按钮，则结束程序运行
                self.end_game()
            # 判断事件类型是否为按键按下事件，如果是，继续判断是哪一个按键，来进行相应的处理
            if event.type == pygame.KEYDOWN:
                # print(event.key)
                # 点击 R 键让我方坦克重生
                if event.key == pygame.K_r:
                    if not MainGame.MY_TANK:
                        self.create_my_tank()
                if MainGame.MY_TANK and MainGame.MY_TANK.is_live:
                    # 具体是按下哪一个键，分别进行处理
                    if event.key == pygame.K_LEFT:
                        print('坦克向左移动')
                        # 修改坦克方向
                        MainGame.MY_TANK.direction = 'L'
                        # 修改坦克移动的状态
                        MainGame.MY_TANK.is_stop = False
                    elif event.key == pygame.K_RIGHT:
                        print('坦克向右移动')
                        # 修改坦克方向
                        MainGame.MY_TANK.direction = 'R'
                        # 修改坦克移动的状态
                        MainGame.MY_TANK.is_stop = False
                    elif event.key == pygame.K_UP:
                        print('坦克向上移动')
                        # 修改坦克方向
                        MainGame.MY_TANK.direction = 'U'
                        # 修改坦克移动的状态
                        MainGame.MY_TANK.is_stop = False
                    elif event.key == pygame.K_DOWN:
                        print('坦克向下移动')
                        # 修改坦克方向
                        MainGame.MY_TANK.direction = 'D'
                        # 修改坦克移动的状态
                        MainGame.MY_TANK.is_stop = False
                    elif event.key == pygame.K_SPACE:
                        print('坦克发射子弹')
                        # 最多发射3颗子弹
                        if len(MainGame.bullet_list) < 3:
                            # 产生一颗子弹
                            m = Bullet(MainGame.MY_TANK)
                            # 将子弹加入到子弹列表
                            MainGame.bullet_list.append(m)
                            # 创建发射音效
                            music = Music('audio/hit.mp3')
                            music.play()
                        else:
                            print('子弹数量不足!!')

            # 监听按钮释放事件
            if event.type == pygame.KEYUP:
                if MainGame.MY_TANK and MainGame.MY_TANK.is_live:
                    # 只有松开方向键，才会停止坦克移动
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN or \
                            event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        # 改变坦克移动状态即可
                        MainGame.MY_TANK.is_stop = True
    # 结束游戏方法
    def end_game(self):
        print('游戏结束，欢迎再次游戏')
        # 终止 python 解释器的运行 结束程序
        exit(0)

# 被 Bullet,Tank 继承的中间类
class BaseItem(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

# 坦克父类
class Tank(BaseItem):
    def __init__(self,left,top): # left,top 分别指示坦克坐标的 x , y轴的值
        # 声明存储不同方向所对应的图片
        self.images = {
            # key 代表坦克朝向，value 代表加载到的图片
            'U': pygame.image.load('./images/my_tank_img_up.png'),
            'D': pygame.image.load('./images/my_tank_img_down.png'),
            'L': pygame.image.load('./images/my_tank_img_left.png'),
            'R': pygame.image.load('./images/my_tank_img_right.png')
        }
        # 坦克的默认方向是朝上的
        self.direction = 'U'
        # 根据坦克朝向取出对应的图片
        self.image = self.images[self.direction]
        # 坦克所在的区域， 返回 Rect 对象
        self.rect = self.image.get_rect()
        # 指定坦克的初始化位置 分别是 x,y 轴坐标的位置
        self.rect.left = left
        self.rect.top = top
        # 新增速度属性
        self.speed = 4
        # 新增属性，坦克的移动开关
        self.is_stop = True # 默认是停止状态
        # 新增属性表示当前敌方坦克是否存活
        self.is_live = True
        # 新增属性，用来记录坦克移动之前的坐标，方便撞墙后还原
        self.old_left = self.rect.left
        self.old_top = self.rect.top

    # 用于返回上一坐标点的方法
    def back(self):
        self.rect.left = self.old_left
        self.rect.top = self.old_top

    # 新增坦克碰撞墙壁检测的方法
    def tank_hit_wall(self):
        for wall in MainGame.wall_list:
            if pygame.sprite.collide_rect(wall,self):
                self.back()

    # 坦克的移动方法
    def move(self):
        # 先记录坦克移动之前的坐标，方便撞墙后还原
        self.old_left = self.rect.left
        self.old_top = self.rect.top
        # 根据坦克方向，改变坦克区域的位置
        if self.direction == 'L':
            # 如果区域的 left 值(x 坐标值) > 0，才能进行向左移动
            if self.rect.left > 0:
                self.rect.left -= self.speed
        if self.direction == 'R':
            if self.rect.left + self.rect.height < MainGame.SCREEN_WIDTH:
                self.rect.left += self.speed
        if self.direction == 'U':
            if self.rect.top > 0:
                self.rect.top -= self.speed
        if self.direction == 'D':
            if self.rect.top + self.rect.width < MainGame.SCREEN_HEIGHT:
                self.rect.top += self.speed
    # 坦克的射击方法
    def shot(self):
        return Bullet(self)
    # 展示坦克的方法
    def display_tank(self):
        # 重新设置坦克的图片
        self.image = self.images[self.direction]
        # 将坦克加入到窗口中
        MainGame.window.blit(self.image,self.rect)

# 我方坦克类
class MyTank(Tank):
    def __init__(self,left,top):
        super().__init__(left,top)
    # 新增我方坦克主动撞到敌方坦克的方法
    def hit_enemy_tank(self):
        for e_tank in MainGame.ENEMY_TANKS_LIST:
            if pygame.sprite.collide_rect(e_tank,self):
                self.back()
# 敌方坦克类
class EnemyTank(Tank):
    def __init__(self, left, top,speed):  # left,top 分别指示坦克坐标的 x , y轴的值,还有移动速度
        super(EnemyTank,self).__init__(left,top)
        # 声明存储不同方向所对应的图片
        self.images = {
            # key 代表坦克朝向，value 代表加载到的图片
            'U': pygame.image.load('./images/enemy_tank_up.png'),
            'D': pygame.image.load('./images/enemy_tank_down.png'),
            'L': pygame.image.load('./images/enemy_tank_left.png'),
            'R': pygame.image.load('./images/enemy_tank_right.png')
        }
        # 敌方坦克的默认方向是随机的
        self.direction = self.rand_direction()
        # 根据坦克朝向取出对应的图片
        self.image = self.images[self.direction]
        # 坦克所在的区域， 返回 Rect 对象
        self.rect = self.image.get_rect()
        # 指定坦克的初始化位置 分别是 x,y 轴坐标的位置
        self.rect.left = left
        self.rect.top = top
        # 新增速度属性
        self.speed = speed
        # 新增属性，坦克的移动开关
        self.is_stop = True  # 默认是停止状态
        # 新增步数属性，用来控制敌方坦克随机移动
        self.step = 30

    # 检测敌方坦克与我方坦克碰撞的方法
    def hit_my_tank(self):
        if pygame.sprite.collide_rect(self,MainGame.MY_TANK):
            self.back()

    # 随机设置敌方坦克朝向的方法
    def rand_direction(self):
        # 根据得到的随机整数，返回不同的方向值
        num = random.randint(1,4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'L'
        elif num == 4:
            return 'R'

    # 敌方坦克的显示方法，其内部使用父类的显示方法
    def display_enemy_tank(self):
        super().display_tank()
    # 随机移动方法
    def rand_move(self):
        # 如果走完指定步数
        if self.step <= 0:
            # 更改坦克方向
            self.direction = self.rand_direction()
            # 重置步数
            self.step = 30
        else:
            self.move()
            self.step -= 1

    # 重写父类的 shot() 方法
    # 用于生成子弹
    def shot(self):
        num = random.randint(1,100)
        if num <= 2:
            return Bullet(self)
# 子弹类
class Bullet(BaseItem):
    def __init__(self,tank):
        # 图片
        self.image = pygame.image.load('images/my_bullet.png')
        # 方向 等于坦克方向
        self.direction = tank.direction
        # 位置
        self.rect = self.image.get_rect()
        if self.direction == 'U':
            # 子弹的 x 坐标值
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            # 子弹的 y 坐标值
            self.rect.top = tank.rect.top - self.rect.height
        if self.direction == 'D':
            # 子弹的 x 坐标值
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width / 2
            # 子弹的 y 坐标值
            self.rect.top = tank.rect.top + tank.rect.height
        if self.direction == 'L':
            # 子弹的 x 坐标值
            self.rect.left = tank.rect.left - self.rect.width
            # 子弹的 y 坐标值
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        if self.direction == 'R':
            # 子弹的 x 坐标值
            self.rect.left = tank.rect.left + tank.rect.width - self.rect.width / 2
            # 子弹的 y 坐标值
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.width / 2
        # 速度
        self.speed = 7
        # 记录子弹存活状态的布尔变量(打中墙壁或敌方坦克 --> 消亡)
        self.is_live = True
    # 子弹的移动方法
    def bullet_move(self):
        # 判断子弹的方向，然后作相应的逻辑
        if self.direction == 'U':
            if self.rect.top > 0: # 子弹没有移动到墙壁的位置时
                self.rect.top -= self.speed
            else: # 子弹已经打中墙壁
                # 修改子弹的存活状态
                self.is_live = False
        if self.direction == 'D':
            if self.rect.top < MainGame.SCREEN_HEIGHT - self.rect.height:
                self.rect.top += self.speed
            else:
                # 修改子弹的存活状态
                self.is_live = False

        if self.direction == 'L':
            if self.rect.left > 0:
                self.rect.left -= self.speed
            else:
                # 修改子弹的存活状态
                self.is_live = False
        if self.direction == 'R':
            if self.rect.left < MainGame.SCREEN_WIDTH - self.rect.width:
                self.rect.left += self.speed
            else:
                # 修改子弹的存活状态
                self.is_live = False
    # 子弹的展示方法
    def display_bullet(self):
        MainGame.window.blit(self.image,self.rect)

    #新增我方子弹碰撞敌方坦克的方法
    def hit_enemy_tank(self):
        # 遍历敌方坦克
        for e_tank in MainGame.ENEMY_TANKS_LIST:
            # 如果当前遍历到的敌方坦克与当前我方子弹发生了矩形碰撞
            if pygame.sprite.collide_rect(e_tank,self):
                # 产生一个爆炸效果
                explode = Explode(e_tank)
                # 将爆炸效果加入到爆炸效果列表中
                MainGame.explode_list.append(explode)
                # 修改我方子弹和敌方坦克的状态
                self.is_live = False
                e_tank.is_live = False

    # 新增敌方子弹与我方坦克碰撞的方法
    def hit_my_tank(self):
        if pygame.sprite.collide_rect(self,MainGame.MY_TANK):
            # 产生爆炸效果，并加入到爆炸效果列表中
            explode = Explode(MainGame.MY_TANK)
            MainGame.explode_list.append(explode)
            # 修改敌方子弹状态
            self.is_live = False
            # 修改我方坦克状态
            MainGame.MY_TANK.is_live = False

    # 新增子弹与墙壁碰撞检测的方法
    def hit_walls(self):
        for wall in MainGame.wall_list:
            if pygame.sprite.collide_rect(wall,self):
                # 修改子弹的 is_live 属性
                self.is_live = False
                # 墙壁的生命值减1
                wall.hp -= 1
                # 如果生命值为0，则销毁墙壁
                if wall.hp <= 0:
                    wall.is_live = False


# 爆炸效果类
class Explode():
    # 爆炸效果对象根据被击中坦克的位置来产生
    def __init__(self,tank):
        # 爆炸发生的区域等同于坦克区域面积
        self.rect = tank.rect
        # 爆炸发生的进度值
        self.step = 0
        # 各阶段爆炸效果图
        self.images = [
            pygame.image.load('images/explode1.png'),
            pygame.image.load('images/explode1.png'),
            pygame.image.load('images/explode1.png'),
        ]
        # 取出一张图片
        self.image = self.images[self.step]
        # 当前爆炸效果是否还存在
        self.is_live = True

    # 展示爆炸效果
    def display_explode(self):
        # 防止列表索引越界
        if self.step < len(self.images):
            MainGame.window.blit(self.image,self.rect)
            # 开始准备获取下一张爆炸图
            self.image = self.images[self.step]
            self.step += 1
        else:
            # 爆炸效果消失
            self.is_live = False
            self.step = 0

# 墙壁类
class Wall():
    def __init__(self,left,top):
        self.image = pygame.image.load('images/wall.png')
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        # 此墙壁是否应该在窗口中展示
        self.is_live = True
        # 墙壁生命值
        self.hp = 3

    # 展示墙壁的方法
    def display_wall(self):
        MainGame.window.blit(self.image,self.rect)

# 音效类
class Music():
    def __init__(self,file_name):
        self.file_name = file_name
        # 初始化混响器
        pygame.mixer.init()
        pygame.mixer.music.load(self.file_name)
    # 开始播放音乐
    def play(self):
        pygame.mixer.music.play()

# 创建主逻辑类实例，调用开始游戏方法
MainGame().start_game()