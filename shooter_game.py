import random
from time import time as timer
from pygame import (mixer, font, sprite, transform,
                    image, display, time, event, key,
                    K_SPACE, KEYDOWN, QUIT, K_LEFT, K_RIGHT)


# фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


# шрифты и надписи
font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.SysFont('Arial', 36)


# нам нужны такие картинки:
img_back = "galaxy.jpg"  # фон игры
img_hero = "rocket.png"  # герой
img_bullet = "bullet.png"  # пуля
img_enemy = "ufo.png"  # враг
img_asteroid = 'asteroid.png' # астероид


score = 0  # сбито кораблей
skipped = 0  # пропущено кораблей
max_skipped = 3  # проиграли, если пропустили столько
max_score = 20 # выигрлали, если убили столько
rel_gun = 0 # пулек в обоиме осталось
rel_time = False # время перезарядки надо или нет 
life = 2

class Sprite_1(sprite.Sprite):
    """ Класс-родитель для других спрайтов. """
    def __init__(self, player_image, player_x, player_y,
                 size_x, size_y, player_speed):
        # вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image),
                                     (size_x, size_y))
        self.speed = player_speed
        # каждый спрайт должен хранить свойство rect - прямоугольник,
        # в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    # метод, отрисовывающий героя на окне

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Rocket(Sprite_1):
    """ Класс Главного героя. """
    # метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    # метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx,
                        self.rect.top, 15, 20, -15)
        bullets.add(bullet)


class Enemy(Sprite_1):
    """ Класс спрайта-врага."""
    # движение врага
    def update(self):
        self.rect.y += self.speed
        global skipped
        # исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = random.randint(80, win_width - 80)
            self.rect.y = 0
            skipped = skipped + 1


class Asteroids(Sprite_1):
    """ Класс спрайта-врага."""
    # движение врага
    def update(self):
        self.rect.y += self.speed
        global skipped
        # исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = random.randint(80, win_width - 80)
            self.rect.y = 0


class Bullet(Sprite_1):
    """ Класс спрайта-пули. """
    # движение врага
    def update(self):
        self.rect.y += self.speed
        # исчезает, если дойдет до края экрана
        if self.rect.y < 0:
            self.kill()


# создаем окошко
win_width = 700  # Ширина
win_height = 500  # Высотва
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))


# создаем спрайты
ship = Rocket(img_hero, 5, win_height - 100, 80, 100, 10)


monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, random.randint(80, win_width - 80),-40, 80, 50, random.randint(1, 5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Asteroids(img_asteroid, random.randint(30, win_width - 30),-40, 80, 50, random.randint(1, 5))
    asteroids.add(asteroid)

bullets = sprite.Group()


# переменная "игра закончилась": как только там True,
# в основном цикле перестают работать спрайты
FALSE = False
# основной цикл игры:
GAME = True  # флаг сбрасывается кнопкой закрытия окна
while GAME:
    # событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            GAME = False
        # событие нажатия на пробел - спрайт стреляет
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if rel_gun < 5 and rel_time == False:
                    rel_gun += 1
                    fire_sound.play()
                    ship.fire()
                if rel_gun >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not FALSE:
        # обновляем фон
        window.blit(background, (0, 0))
        # пишем текст на экране
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Пропущено: " + str(skipped), 1,
                                 (255, 255, 255))
        window.blit(text_lose, (10, 50))
        # производим движения спрайтов
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        # обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('WAIT RELOADING', 1, (200, 0, 0))
                window.blit(reload, (260, 460))
            else:
                rel_gun = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)

        for c in collides:
            score += 1
            monster = Enemy(img_enemy, random.randint(80, win_width - 80),-40, 80, 50, random.randint(1, 5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life -= 1

        if life == 0 or skipped == max_skipped:
            FALSE = True
            window.blit(lose, (200, 200))

        if score == max_score:
            FALSE = True
            window.blit(win, (200, 200))        
        

        if life == 2:
            life_color = (150, 150, 0)
        
        if life == 1:
            life_color = (0, 125, 0)
        
        text_life = font2.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))
        
        display.update()
    # цикл срабатывает каждую 0.05 секунд
    time.delay(40)