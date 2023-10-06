from random import *
from pygame import *
font.init()
mixer.init()
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed=0, image_wight=0, image_height=0):
        super().__init__()
        self.image_wight = image_wight
        self.image_height = image_height
        self.image = transform.scale(image.load(player_image), (image_wight, image_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.fire = True
        self.fps = 40
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        self.fps -= 1
        if self.fps <= 0:
            self.fire = True



class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed=0, image_wight=0, image_height=0, hearts=3):
        super().__init__(player_image, player_x, player_y, player_speed, image_wight, image_height)
        self.hearts = hearts
    def move(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < x-70:
            self.rect.x += self.speed
    def bird1(self):
        self.rect.x += self.speed
    def bird2(self):
        self.rect.x -= self.speed


class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed=0, image_wight=0, image_height=0, hearts=1):
        super().__init__(player_image, player_x, player_y, player_speed, image_wight, image_height)
        self.hearts = hearts
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 740:
            self.rect.y = -70
            global skip
            skip += 1
            self.rect.x = randint(30, 380)

class Button():
    def __init__(self, x, y, wight, height, color):
        self.rect = Rect(x, y, wight, height)
        self.color = color
        self.x = x
        self.y = y

    def draw_rect(self, border_color=0, new_color=0):
        if border_color == 0:
            border_color = self.color
        if new_color == 0:
            new_color = self.color
        draw.rect(window, self.color, self.rect)
        draw.rect(window, border_color, self.rect, 5)
    
    def create_text(self, size):
        self.font = font.SysFont('Arial', size)

    def draw_text(self, text_color, text, xofset, yofset):
        question = self.font.render(text, True, text_color)
        window.blit(question, (self.x+xofset, self.y+yofset))

def enemy():
    global cars
    for car in cars:
        car.kill()
    car1 = Enemy('car1.png', randint(30, 380), randint(-110, -70), 3, 65, 90)
    car2 = Enemy('car8.png', randint(30, 380), randint(-110, -70), 3, 50, 90)
    car3 = Enemy('car3.png', randint(30, 380), randint(-110, -70), 3, 45, 90)
    car4 = Enemy('car4.png', randint(30, 380), randint(-110, -70), 3, 45, 90)
    car5 = Enemy('car5.png', randint(30, 380), randint(-110, -70), 3, 65, 90)
    cars.add(car1, car2, car3, car4, car5)

def lose():
    lose = font1.render('YOU LOSE!', True, (255, 0, 0))
    window.blit(lose, (160, 150))
    global end
    end = False
    


x = 450
y = 650
window = display.set_mode((x, y))
display.set_caption('Погоня')
background = transform.scale(image.load('road.jpg'), (x, y))
window.blit(background, (0,0))

hero = Player('hero.png', 190, 550, 2, 65, 90, 3)

heart1 = GameSprite('heart1.png', -10, 5, 0, 55, 35)
heart2 = GameSprite('heart1.png', 25, 5, 0, 55, 35)
heart3 = GameSprite('heart1.png', 60, 5, 0, 55, 35)

bird1 = Player('bird1.png', randint(-90, -50), 80, 1, 50, 50)
bird2 = Player('bird2.png', randint(515, 550), 160, 1, 50, 50)

cars = sprite.Group()
enemy()


start = Button(150, 300, 150, 65, (255, 255, 255))
start.draw_rect((0, 0, 0))
start.create_text(40)
start.draw_text((0, 0, 0), 'START', 30, 20)

restart = Button(150, 300, 150, 65, (255, 255, 255))



skip = 0
font1 = font.SysFont('Arial', 35)
list_hearts = [heart1, heart2, heart3]
clock = time.Clock()
end = False
game = True
while game:
    if end:
        window.blit(background, (0,0))
        hero.reset()
        hero.move()
        cars.draw(window)
        cars.update()
        bird1.reset()
        bird1.bird1()
        bird2.reset()
        bird2.bird2()

        for i in range(hero.hearts):
            list_hearts[i].reset() 

        count = font1.render('Счёт:'+str(skip), True, (0, 0, 0))
        window.blit(count, (5,40))
        
        hits = sprite.spritecollide(hero, cars, True)
        for hit in hits:
            hero.hearts -= 1
            new_car = Enemy('car6.png', randint(30, 380), randint(-110, -70), 3, 60, 90)
            cars.add(new_car)

        if bird1.rect.x >= 500:
            bird1.rect.x = randint(-90, -50)
        
        if bird2.rect.x <= -50:
            bird2.rect.x = randint(515, 550)

        
        if hero.hearts <= 0:
            lose()
            restart.draw_rect((0, 0, 0))
            restart.create_text(40)
            restart.draw_text((0, 0, 0), 'RESTART', 12, 20)

        if skip >= 100:
            win = font1.render('YOU WIN!', True, (0, 255, 0))
            window.blit(win, (165, 150))
            end = False
            restart.draw_rect((0, 0, 0))
            restart.create_text(40)
            restart.draw_text((0, 0, 0), 'RESTART', 12, 20)
            

        
    for e in event.get():
        if e.type == MOUSEBUTTONDOWN and e.button == 1:
            x_button, y_button = e.pos
            if start.rect.collidepoint(x_button, y_button):
                end = True
            if restart.rect.collidepoint(x_button, y_button):
                skip = 0
                hero.hearts = 3
                bird1.rect.x = randint(-90, -50)
                bird2.rect.x = randint(515, 550)
                for car in cars:
                    car.rect.y = randint(-110, -70)
                enemy()
                cars.draw(window)
                cars.update()
                end = True
        if e.type == QUIT:
            game = False
    display.update()
    clock.tick(105)
