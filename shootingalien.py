import pygame
import sys
import random

pygame.init()
FPS = pygame.time.Clock()
# set color
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
yellow = (255,255,0)
white = (255,255,255)
black = (0,0,0)
gray = (155,200,155)
gray_nhat = (222,220,200)

title_font = pygame.font.SysFont('monospace',36,True,True)
arial_font = pygame.font.SysFont('Arial',12)
tiny_font = pygame.font.SysFont('monospace',15)

text_lose = title_font.render('YOU LOSE!',True,white)
text_win = title_font.render('YOU WIN!',True,white)

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('SHOOTING ALIEN 1')

def change_var_to_true_or_false(var):
    if var == True:
        return False
    elif var == False:
        return True

def indentify_bullet_out_screen(y):
    if y < 0:
        return True
    elif y > screen_height:
        return True
    return False

def indentify_the_collide_oject_rect(x,y,x_oject,y_oject,len_x_oject,len_y_oject):   #baseic collide in rect object
    if x > x_oject and x < (x_oject + len_x_oject) and y > y_oject and y < (y_oject + len_y_oject):
        return True
    return False

def indentify_the_collide_circle_oject(x,y,radius,x_oject,y_oject,radius_oject):
    if (x + radius) > (x_oject - radius_oject) and (x - radius) < (x_oject + radius_oject) and (y + radius) > (y_oject - radius_oject) and (y - radius) < (y_oject + radius_oject):
        return True
    return False

class alienspace:
    def __init__(self,x,y,speed=5):
        self.scr = screen
        self.speed = speed
        self.lever = 1
        self.size_bullet_alien = 2
        self.list_alien = []
        self.alien_fly = True
        self.appear_alien = True        
        self.hit_bullet = False         # hit by player's bullet
        self.alien_fire = True
        self.image_alien = pygame.image.load('pic/alienspace.png')
        self.new_size = (50,50)
        self.new_image_alien = pygame.transform.scale(self.image_alien,self.new_size)
        # boss alien
        self.alien_boss_x = 350
        self.alien_boss_y = 150
        self.speed_boss = 2
        self.blood_alien = 1000
        self.alien_boss_size = (150,150)
        self.list_fire_ball = []
        self.size_fire_boss_alien = 10
        self.alien_boss_appear = False
        self.image_alien_boss = pygame.transform.scale(self.image_alien,self.alien_boss_size)
        self.alien_boss_move = True
        self.alien_boss_hit_bullet = False
        self.boss_alien_die = False

        self.more_alien = False
    
    def create_alien(self):
        larange1 = (screen_width-30)/6
        larange2 = (screen_width-30)/5
        if self.lever == 1:  # 2 hàng
            for i in range(0,9):
                if i <= 4:
                    self.list_alien.append([(i+1)*larange1,100])
                else:
                    self.list_alien.append([(i-4)*larange2,200])
        elif self.lever == 2: # 3 hàng
            self.list_alien.clear() # xóa các alien cũ
            for i in range(0,14):
                if i <= 4:
                    self.list_alien.append([(i+1)*larange1,100])
                elif i <= 8:
                    self.list_alien.append([(i-4)*larange2,150])
                else:
                    self.list_alien.append([(i-8)*larange1,200])
        elif self.lever == 3:
            self.list_alien.clear()

    def draw_alien(self):
        for i in self.list_alien:
            self.scr.blit(self.new_image_alien,((i[0])-(self.new_size[0]/2),i[1]-(self.new_size[1]/2)))

    def move_alien_space(self):
        for i in self.list_alien:
            i[0] += self.speed
            if i[0] < 11 or i[0] > screen_width - 11:
                self.speed = -self.speed
            if i[0]  < -10 or i[0] > screen_width - 10:
                self.list_alien[self.list_alien.index(i)][0] = random.randint(50,750)

    def add_alien(self):    # thêm 1 alien
        if self.lever == 1 and len(self.list_alien) <= 3:    
            self.list_alien.append([random.randint(50,750),100])
        elif self.lever == 2 and len(self.list_alien) <= 6:
            self.list_alien.append([random.randint(50,750),random.choice([100,200])])
        elif self.lever == 3:
            self.list_alien.append([random.randint(50,750),random.choice([100,150,200])])
#
    def draw_alien_boss(self):
        self.scr.blit(self.image_alien_boss,(self.alien_boss_x-(self.alien_boss_size[0]/2),self.alien_boss_y-(self.alien_boss_size[1]/2)))
    
    def draw_blood_alien(self):
        pygame.draw.rect(self.scr,yellow,((self.alien_boss_x-50)-0.5,(self.alien_boss_y-(self.alien_boss_size[1]/2)-10)-0.5,(1000/10)+2,7),1,1)
        pygame.draw.rect(self.scr,red,((self.alien_boss_x-50),(self.alien_boss_y-(self.alien_boss_size[1]/2)-10),self.blood_alien/10,5))

    def move_alien_boss(self):
        self.alien_boss_x += self.speed_boss
        if self.alien_boss_x < 100 or self.alien_boss_x > 500:
            self.speed_boss = -self.speed_boss

    def boss_fire(self):
        self.list_fire_ball.append([self.alien_boss_x,self.alien_boss_y])
            
    def draw_bullet_boss(self):
        for i in self.list_fire_ball:
            i[1] += 5
            pygame.draw.circle(self.scr,red,(i[0],i[1]),self.size_fire_boss_alien)

    def fire_bullet_move(self):
        for i in self.list_fire_ball:
            i[1] += 5
            if i[1] == screen_height*(2/3):
                self.list_fire_ball.remove(i)

    def boss_hit(self):
        if self.alien_boss_hit_bullet == True:
            self.blood_alien -= 10

        if self.blood_alien <= 0:
            self.alien_boss_move = False
            self.alien_boss_appear = False
            self.boss_alien_die = True
            self.list_fire_ball.clear()

    def update_lever(self):
        if self.lever == 1 and score_player.score >= 10:
            self.lever += 1
            self.more_alien = True
            return True
        elif self.lever == 2 and score_player.score >= 20:
            self.lever += 1
            self.more_alien = True
            return True
        return False

class Space:
    def __init__(self,x=screen_width/2,y=screen_height-50,space_speed=10):
        self.x = x
        self.y = y
        self.space_speed = space_speed
        self.scr = screen
        self.image = pygame.image.load('pic/thespace.png')
        self.new_size = (50,50)
        self.new_image = pygame.transform.scale(self.image,self.new_size)
        self.hide_space = False
        self.space_fly = True
        self.space_move_left = False
        self.space_move_right = False

    def draw(self):    
        if self.hide_space == False:
            self.scr.blit(self.new_image,(self.x-(self.new_size[0])/2,self.y-(self.new_size[1]/2)))
    
    def space_move(self):
        if self.space_move_left == True and self.space_fly == True:
            self.x -= self.space_speed
        elif self.space_move_right == True and self.space_fly == True:
            self.x += self.space_speed
        if self.x < 5 or self.x > screen_width-5:
            if self.x > screen_width-5:
                self.x = screen_width-5
            if self.x < 5:
                self.x = 5

class Bullet:
    def __init__(self,vector=10,color=white):
        self.vector = vector
        self.color_bullet = color
        self.bullet_fly = True
        self.bullet_collide = False
        self.list_bullet = []
    
    def draw_bullet(self): 
        for i in self.list_bullet:
            pygame.draw.circle(screen,self.color_bullet,i,2)

    def bullet_move(self):
        if self.bullet_fly == True:
            for i in range(len(self.list_bullet)):
                self.list_bullet[i][1] -= self.vector

    def create_bullet(self,x_bullet,y_bullet):
        self.list_bullet.append([x_bullet,y_bullet])
        self.list_bullet.sort()

    def delete_bullet(self):
        for i in (self.list_bullet):
            if indentify_bullet_out_screen(i[-1]) == True:
                self.list_bullet.remove(i)

    def bullet_bomb_when_collide_with_oject(self,x,y):  # thêm hiệu ứng
        self.list_bullet.remove([x,y])

    def bullet_was_fire(self):
        if len(self.list_bullet) == 0:
            self.bullet_fly == False
            return self.bullet_fly
        return True

class Button:
    def __init__(self,x_button,y_button,len_x_button,len_y_button,button_name,font_color=blue,color_button = gray,color_in_press_button = yellow):
        self.x_button = x_button            # tọa độ nút theo x, tính từ trái qua
        self.y_button = y_button            # tọa độ nút theo y, tính từ trên
        self.len_x_button = len_x_button    # độ dài theo x của nút
        self.len_y_button = len_y_button    # độ dài thei y của nút
        self.color_button = color_button    # màu nút
        self.color_in_press_button = color_in_press_button  # màu nút khi di chuột vào
        self.button_font = arial_font       # font chữ trên nút
        self.font_color = font_color        # màu của chữ trên nút
        self.button_name = button_name      # tên nút
        self.character_in_button = self.button_font.render(self.button_name,True,blue)  # fomat cho tên nút(màu sắc, đậm nhạt)
        self.press_button = False           # tình trạng ấn nút, mặc định chưa
        self.in_button = False              # nút được di vào
    
    def draw_button(self):
        if self.in_button == False:
            pygame.draw.rect(screen,self.color_button,(self.x_button,self.y_button,self.len_x_button,self.len_y_button))
        elif self.in_button == True:
            pygame.draw.rect(screen,self.color_in_press_button,(self.x_button,self.y_button,self.len_x_button,self.len_y_button))
        screen.blit(self.character_in_button,(self.x_button+8,self.y_button+8))

    def indentify_in_button(self):
        x,y = pygame.mouse.get_pos()
        if indentify_the_collide_oject_rect(x,y,self.x_button,self.y_button,self.len_x_button,self.len_y_button):
            self.in_button = True
        else:
            self.in_button = False
    # xác định nhấn nút
    def indentify_pressing(self):   # trả về True hoặc False
        x,y = pygame.mouse.get_pos()    # lấy giá trị của con trỏ chuột
        if event.type == pygame.MOUSEBUTTONDOWN and indentify_the_collide_oject_rect(x,y,self.x_button,self.y_button,self.len_x_button,self.len_y_button):# khi người chơi ấn chuột và tạo độ chuột trong phạm vi nút
            return True
        return False
# lớp điểm người chơi
class Score:
    def __init__(self,score):
        self.score = score
        self.font = tiny_font
        self.add_score = 1 
        self.count_hit = False
        self.text = self.font.render('Score : {}'.format(self.score),True,white)
    # in điểm ra màn hình
    def print_score(self):
        screen.blit(self.text,(700,10))
    # tăng điểm cho người chơi
    def update_score(self):
        if self.count_hit == True:
            self.score += 1
            self.text = self.font.render('Score : {}'.format(self.score),True,white)    # thay đổi giá trị để đưa ra màn hình
            self.count_hit = change_var_to_true_or_false(self.count_hit)
            return  # cộng điểm xong thoát khỏi hàm
    # reset lại điểm, dùng khi chơi lại(ấn nút RESTART)
    def restart_score(self):
        self.score = 0
        self.text = self.font.render(f'Score : {self.score}',True,white)
    # thắng trò chơi
    def win_game(self,event_end_game):
        if self.score >= 30 and event_end_game == True:
            return True
        return False
# lớp mạng của người chơi
class Heart:
    def __init__(self): # khai báo các biến của lớp
        self.num_heart = 3  # sô mạng, mặc định là 3
        self.font = tiny_font
        self.text = self.font.render(f'Amor : {self.num_heart}',True,white)
    
    def blit_life(self):
        self.text = self.font.render(f'Amor : {self.num_heart}',True,white)
        screen.blit(self.text,(700,30))

    def lost_heart(self):
        self.num_heart -= 1

    def re_heart(self):
        self.num_heart = 3

    def lose(self): # trả về True hoặc False
        if self.num_heart == 0:
            return True
        return False

player = Space()                            # tạo đối tượng tàu(ngừoi chơi)
ailien1 = alienspace(50,80,5)               # tạo bầy alien
dan = Bullet()                              # tạo đạn của người chơi(mặc định đạn màu trắng)
dan_alien = Bullet(-10,red)                 # tạo đạn cho bọn alien(màu đạn đỏ, tốc độ âm vì thả từ trên xuống(class Bullet mặc định là trừ đi speed ))
button1 = Button(700,540,60,30,'RESTART')   # tạo nút restart
score_player = Score(0)                     # tạo đối tượng của người chơi
mang = Heart()                              # tạo đối tượng mạng của người chơi

speed_bullet_of_alien = 2000    # thồi gian bắn đạn của alien 
time_to_creata_alien = 3000     # thồi gian tạo alien

count_the_time_to_fire_of_alien = pygame.USEREVENT + 1  # đặt tên cho sự kiện(alien bắn)
re_create_alien = pygame.USEREVENT + 1                  # đặt tên cho sự kiện(tạo lại alien)
# sự kiện hồi máu cho boss alien 
# //
pygame.time.set_timer(count_the_time_to_fire_of_alien,speed_bullet_of_alien)    # tạo sự kiện alien bắn xảy ra sau 1 thời gian
pygame.time.set_timer(re_create_alien,time_to_creata_alien)                     # tạo sự kiện alien được tạo lại sau 1 thời gian

rungame = True  # biến game chạy
delay = False   # biến dừng game
lose_game = False

# hàm tạo alien chỉ gọi 1 lần """   cần sửa  """
ailien1.create_alien()      # tạo alien vì nếu đưa vào vòng lặp chương trình thì các alien đươc tạo lại liên tục
# vòng ;ặp chính của trò chơi
while rungame:
    FPS.tick(20)    # đưa tốc độ khung hình về 20
    for event in pygame.event.get():    # vòng lặp sự kiện được ghi lại
        if event.type == pygame.QUIT:
            rungame = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:  # người chơi nhấn 1 phím xuống
            if event.key == pygame.K_LEFT and delay != True:
                player.space_move_left = True   # tàu di chuyển qua trái về True
            # nhấn mũi tên qua phải trên bàn phím và biến dừng sai
            if event.key == pygame.K_RIGHT and delay != True:
                player.space_move_right = True  # tàu di chuyển qua phải về True
            # người chơi nhấn cách và biến dừng sai
            if event.key == pygame.K_SPACE and delay != True:
                dan.create_bullet(player.x,player.y)    # tạo đạn
            # người chơi nhấn tab và biến dừng sai
            if event.key == pygame.K_TAB and delay != True: # 
                # ailien1.appear_alien = change_var_to_true_or_false(ailien1.appear_alien)    # chuyển biến xuất hiện của alien
                pass    # thêm chức năng
            # người chơi nhấn ctrl bên trái bàn phím và dừng sai
            if event.key == pygame.K_LCTRL and delay != True:
                # ailien1.alien_fly = change_var_to_true_or_false(ailien1.alien_fly)  # chuyển đôi sự di chuyển/đứng yên của alien
                pass    # thêm chức năng
            # người chơi nhấn cách và biến dừng sai         # bug tăng lever lên 3 để triệu hồi boss alien
            if event.key == pygame.K_LALT and delay != True:
                # ailien1.alien_boss_appear = change_var_to_true_or_false(ailien1.alien_boss_appear)
                pass
            if event.key == pygame.K_CAPSLOCK and delay != True:
                ailien1.alien_boss_move = change_var_to_true_or_false(ailien1.alien_boss_move)
        # kiểm tra khi người chơi thả tay khỏi 1 phím nào đó
        elif event.type == pygame.KEYUP and delay != True:
            if event.key == pygame.K_LEFT:  # người chơi thả nút mũi tên trái
                player.space_move_left = change_var_to_true_or_false(player.space_move_left)    # di chuyển qua trái về False
            elif event.key == pygame.K_RIGHT:# người chơi thả nút di chuyển phải
                player.space_move_right = change_var_to_true_or_false(player.space_move_right)  # di chuyển qua phải về False
        # sự kiện tạo đạn cho alien và alien phải xuất hiện, biến dừng sai, list ailien chưa hết và biến alien bắn đạn là đúng
        if event.type == count_the_time_to_fire_of_alien and ailien1.appear_alien == True and delay != True and len(ailien1.list_alien) != 0 and ailien1.alien_fire == True:
            dan_alien.create_bullet(ailien1.list_alien[random.randint(0,len(ailien1.list_alien)-1)][0],ailien1.list_alien[random.randint(0,len(ailien1.list_alien)-1)][1]) # tạo alien ngẫu nhiên trong phạm vi màn hình
        # sự kiện tạo alien sau 2s và alien phâí xuất hiện, biến dừng sai và alien phải trúng đạn(vì khi khởi động chương trình người chơi chưa bắn thì chưa thể tạo ailen)
        if event.type == re_create_alien and ailien1.appear_alien == True and delay != True and ailien1.hit_bullet == True:
            ailien1.add_alien()     # tạo thêm alien 
        # sự kiện đươc thực hiện sau 3s và boss alien phải xuất hiện, biến dừng sai và boss chưa hết hp
        if event.type == count_the_time_to_fire_of_alien and ailien1.alien_boss_appear == True and delay != True and ailien1.blood_alien >0:
            ailien1.boss_fire()     # gọi hàm boss alien bắn đạn
    # duyệt các đạn của người chơi
    for i in dan.list_bullet: # đạn từ người chơi bắn vào alien
        for j in ailien1.list_alien:        # duyệt tất cả các alien đang có trên màn hình
            if indentify_the_collide_circle_oject(i[0],i[1],2,j[0],j[1],25) == True and ailien1.appear_alien == True and player.hide_space != True:    # kiểm tra chạm giửa đạn ngưởi chơi và các alien
                score_player.count_hit = True   # trả về biến cộng điểm cho người chơi
                score_player.update_score()     # cộng điểm cho người chơi
                ailien1.hit_bullet = True       # trả về biến alien bị trúng đạn
                # dan.list_bullet.remove(dan.list_bullet[dan.list_bullet.index(i)])         # dòng thử thay thế cho việc xóa đạn bắn trúng alien
                dan.list_bullet.remove(i)       # xóa đạn bắn trúng alien                   ### CÓ bug ###
                ailien1.list_alien.remove(j)    # xóa alien bị trúng đạn
                break   # thoát khôi vòng lặp hiện tại
    for i in dan.list_bullet:
        # kiểm tra đạn có dính boss alien không
        if indentify_the_collide_circle_oject(i[0],i[1],2,ailien1.alien_boss_x,ailien1.alien_boss_y,50) == True and ailien1.alien_boss_appear == True:   # điều kiện bắt buộc: boss alien phải xuất hiện 
            ailien1.alien_boss_hit_bullet = True    # trả về True cho biến boss alien trúng đạn
            ailien1.boss_hit()              # gọi hàm boss ailen bị trúng đạn
            dan.list_bullet.remove(i)       # xóa đạn nếu trúng boss                    ### bug ###
        ailien1.alien_boss_hit_bullet = change_var_to_true_or_false(ailien1.alien_boss_hit_bullet)  # chuyển biến boss alien bị trúng đạn về False khi duyệt xong 
    # duyệt các phần tử đạn của boss alien
    for i in ailien1.list_fire_ball:
        if indentify_bullet_out_screen(i[1]) == True:   # kiểm tra bằng hàm nếu ra khỏi màn hình
            ailien1.list_fire_ball.remove(i)# xóa đạn nếu ra khỏi mạn hình
        # kiểm tra đạn có va chạm với người chơi không
        if indentify_the_collide_circle_oject(i[0],i[1],ailien1.size_fire_boss_alien ,player.x,player.y,10) == True and player.hide_space != True:
            mang.num_heart = 0              # gán số mạng về 0, quy định dính đạn boss là die
            ailien1.list_fire_ball.remove(i)# xóa đạn của boss alien

    if len(dan_alien.list_bullet ) != 0:    # đạn từ alien bắn player
        for i in dan_alien.list_bullet:     # duyệt các phần tử trong danh sách đạn của alien
            if indentify_the_collide_circle_oject(i[0],i[1],ailien1.size_bullet_alien,player.x,player.y,10) and player.hide_space != True:    # kiểm tra va chạm của từng đạn với người chơi
                dan_alien.bullet_bomb_when_collide_with_oject(i[0],i[1])   # xóa đạn nếu chạm vào người chơi
                mang.lost_heart()           # mất 1 tim
    
    screen.fill(black)  # phủ lại nền để xóa các hình trước 
    # lấy thời giam kể từ khi khởi động chương trình
    time_until_end = pygame.time.get_ticks()
    text_time_until_end = tiny_font.render('Time: {} s'.format(round(time_until_end/1000),2),True,white)
    screen.blit(text_time_until_end,(10,5))
    # tốc độ khung hình tại thời điểm đó
    fps_game = FPS.get_fps()
    text_fps_until_end = tiny_font.render('fps now is: {} '.format(round(fps_game,2)),True,white)
    screen.blit(text_fps_until_end,(10,20))
    # thời gian hiện ảnh 
    get_fps = FPS.get_time()
    text_time_for_fps = tiny_font.render('time for pic: {} ms/pic'.format(get_fps),True,white)
    # screen.blit(text_time_for_fps,(10,70)) kh

    if mang.lose() == True: # khi mạng về 0  
        delay = True        # biến dừng trò chơi đúng
    elif score_player.win_game(ailien1.boss_alien_die) == True:
        delay = True

    if delay == True:
        screen.fill(black)              # phủ màn hình đen 
        dan.list_bullet.clear()         # xóa tất cả đạn của người chơi ngay lập tức
        dan_alien.list_bullet.clear()   # xóa tất cả đạn của alien ngay lập tức
        ailien1.list_alien.clear()      # xóa mọi alien đang có
        ailien1.appear_alien = False    # alien không xuất hiện
        ailien1.alien_boss_appear = False   # boss ailen ẩn
        ailien1.alien_boss_move = False     # boss alien ngừng di chuyển
        player.hide_space = True        # dấu tàu người chơi
        player.space_fly = False
        # thông báo người chơi thua
        if mang.lose() == True:
            screen.blit(text_lose,(280,200))
        elif score_player.win_game(ailien1.boss_alien_die):
            screen.blit(text_win,(280,200))
#--------------------------------------- vô dụng
        # sự kiện khi ấn phím để reset hoặc quit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_r:   # người chơi nhấn r ## chưa chạy ##
                delay = change_var_to_true_or_false(delay)
                player.hide_space = change_var_to_true_or_false(player.hide_space)
                ailien1.appear_alien = change_var_to_true_or_false(ailien1.appear_alien)
                score_player.restart_score()
                mang.re_heart()         # reset điểm
#---------------------------------------
        button1.draw_button()           # vẽ nút restart
        if button1.indentify_pressing() == True:
            pygame.time.delay(1000)
            mang.re_heart()             # reset lại mạng người chơi
            mang.num_heart = 3          # gán lại số mạng người chơi về 3
            delay = False               # chhuyển delay về False

            player.hide_space = change_var_to_true_or_false(player.hide_space)          # ấn space về False
            player.space_fly = change_var_to_true_or_false(player.space_fly)
            player.space_move_left = False
            player.space_move_right = False

            score_player.restart_score()                                                # reset điểm người chơi

            ailien1.lever = 1                                                           # lever alien về mức 1
            ailien1.appear_alien = change_var_to_true_or_false(ailien1.appear_alien)    # xuất hiện alien về True
            ailien1.hit_bullet = change_var_to_true_or_false(ailien1.hit_bullet)        # alien trúng đạn về False
            ailien1.boss_alien_die = False
            ailien1.blood_alien = 1000
            ailien1.create_alien()

    player.space_move() # vẽ tàu (người chơi)

    button1.indentify_in_button()

    if ailien1.update_lever() == True and delay != True and ailien1.more_alien == True:
        ailien1.create_alien()
        if ailien1.lever == 3:
            ailien1.alien_boss_appear = True
            ailien1.alien_boss_move = True

    if ailien1.appear_alien == True:
        ailien1.draw_alien()
        if ailien1.alien_fly == True:
            ailien1.move_alien_space()
    
    if ailien1.alien_boss_appear == True and ailien1.boss_alien_die != True:
        ailien1.draw_bullet_boss()
        ailien1.draw_alien_boss()
        ailien1.draw_blood_alien()
        if ailien1.alien_boss_move == True:
            ailien1.move_alien_boss()

    dan.bullet_move()
    dan.draw_bullet()
    dan.delete_bullet()
    
    dan_alien.bullet_move()
    dan_alien.draw_bullet()
    dan_alien.delete_bullet()
    
    score_player.print_score()

    mang.blit_life()

    player.draw()

    pygame.display.update()
pygame.quit()

