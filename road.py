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

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed=0, image_wight=0, image_height=0, hearts=1):
        super().__init__(player_image, player_x, player_y, player_speed, image_wight, image_height)
        self.hearts = hearts
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 740:
            self.rect.y = -70
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
    car1 = Enemy('car1.png', randint(30, 380), randint(-110, -70), 1, 65, 90)
    car2 = Enemy('car2.png', randint(30, 380), randint(-110, -70), 1, 45, 90)
    car3 = Enemy('car3.png', randint(30, 380), randint(-110, -70), 1, 45, 90)
    car4 = Enemy('car4.png', randint(30, 380), randint(-110, -70), 1, 45, 90)
    car5 = Enemy('car5.png', randint(30, 380), randint(-110, -70), 1, 65, 90)
    cars.add(car1, car2, car3, car4, car5)


x = 450
y = 650
window = display.set_mode((x, y))
display.set_caption('Погоня')
background = transform.scale(image.load('road.jpg'), (x, y))
window.blit(background, (0,0))

hero = Player('hero.png', 190, 550, 2, 65, 90, 3)

sprite8 = GameSprite('heart1.png', 1, 5, 0, 55, 35)
sprite9 = GameSprite('heart1.png', 41, 5, 0, 55, 35)
sprite10 = GameSprite('heart1.png', 81, 5, 0, 55, 35)

cars = sprite.Group()
enemy()

list_hearts = [sprite8, sprite9, sprite10]
clock = time.Clock()
game = True
while game:
    window.blit(background, (0,0))
    hero.reset()
    hero.move()
    cars.draw(window)
    cars.update()

    for i in range(hero.hearts):
        list_hearts[i].reset()  
    
    hits = sprite.spritecollide(hero, cars, True)
    for hit in hits:
        hero.hearts -= 1
        car6 = Enemy('car6.png', randint(30, 380), randint(-110, -70), 4, 65, 90)
        cars.add(car6)
        if car6 in cars:
            car7 = Enemy('car7.png', randint(30, 380), randint(-110, -70), 4, 65, 90)
            cars.add(car7)
        if car7 in cars:
            car8 = Enemy('car8.png', randint(30, 380), randint(-110, -70), 4, 65, 90)
            cars.add(car8)

    
    for e in event.get():
        if e.type == QUIT:
            game = False
    display.update()
    clock.tick(105)
