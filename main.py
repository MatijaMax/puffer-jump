import pgzrun
import random

class Puffer:
    def __init__(self, images, pos):
        self.sprites = images 
        self.index = 0  
        self.actor = Actor(self.sprites[self.index], pos)
        self.speed = 5
        self.timer = 0 
        self.is_puffed = False
        self.cooldown_timer = 0
        self.cooldown_duration = 60

    def update(self):
        self.move()
        self.animate()
        self.power()

        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1

    def move(self):
        if keyboard.left:
            self.actor.x -= self.speed
        if keyboard.right:
            self.actor.x += self.speed
        if keyboard.up:
            self.actor.y -= self.speed
        if keyboard.down:
            self.actor.y += self.speed

    def power(self):
        if keyboard.space and not self.is_puffed and self.cooldown_timer == 0:
            self.actor.image = 'power'
            self.is_puffed = True
            self.cooldown_timer = self.cooldown_duration

        if self.is_puffed:
            self.cooldown_timer -= 1
            if self.cooldown_timer <= self.cooldown_duration - 30:
                self.is_puffed = False
                self.actor.image = self.sprites[self.index]
        

    def animate(self):
        self.timer += 1
        if not self.is_puffed and self.timer % 5 == 0:  
            self.index = (self.index + 1) % len(self.sprites)
            self.actor.image = self.sprites[self.index]

    def draw(self):
        self.actor.draw()

class Redfish:
    def __init__(self, images, is_right):
        self.sprites = images 
        self.index = 0  
        self.actor = Actor(self.sprites[self.index])
        self.speed = 3
        self.timer = 0 
        if is_right:
            self.direction = "right"
        else:
            self.direction = "left"

        if self.direction == "left":
            self.position_redfish_left()
        else:
            self.position_redfish_right()

    def update(self):
        self.move()
        self.animate()

    def move(self):
        if self.direction == "left":
            self.actor.x -= self.speed  
            if self.actor.x < -100:  
                self.position_redfish_left()
        else:
            self.actor.x += self.speed 
            if self.actor.x > WIDTH + 100:  
                self.position_redfish_right()

    def position_redfish_right(self):
        self.actor.y = random.randint(40, HEIGHT - 40)
        self.actor.x = -100

    def position_redfish_left(self):
        self.actor.y = random.randint(40, HEIGHT - 40)
        self.actor.x = WIDTH + 100

    def animate(self):
        self.timer += 1
        if self.timer % 5 == 0:  
            self.index = (self.index + 1) % len(self.sprites)
            self.actor.image = self.sprites[self.index]

    def draw(self):
        self.actor.draw()

class Titan:
    def __init__(self, images):
        self.sprites = images 
        self.index = 0  
        self.actor = Actor(self.sprites[self.index])
        self.timer = 0 
        self.direction = random.choice(["left", "right"])

        if self.direction == "left":
            self.position_titan_left()
        else:
            self.position_titan_right()

    def update(self):
        self.move()
        self.animate()

    def move(self):
        if self.direction == "left":
            self.actor.x -= 7
            if self.actor.x < -100:  
                self.position_titan_right()
        else:
            self.actor.x += 7
            if self.actor.x > WIDTH + 100:  
                self.position_titan_left()

    def position_titan_right(self):
        self.actor.y = random.randint(40, HEIGHT - 40)
        self.actor.x = -100
        self.direction = "right"

    def position_titan_left(self):
        self.actor.y = random.randint(40, HEIGHT - 40)
        self.actor.x = WIDTH + 100
        self.direction = "left"

    def animate(self):
        self.timer += 1
        if self.timer % 5 == 0:
            if self.direction == "right":  
                self.index = 0 if self.index == 1 else 1
            else:
                self.index = 2 if self.index == 3 else 3
            self.actor.image = self.sprites[self.index]

    def draw(self):
        self.actor.draw()        

# PUFFER FRENZY :) (inspired by feeeding frenzy)
WIDTH = 640 
HEIGHT = 353
sounds.background.play(loops=-1) 
play_button = Rect(280, 150, 140, 40)
exit_button = Rect(280, 200, 140, 40)
mute_button = Rect(280, 250, 140, 40)
game_running = False
music_muted = False
is_puffed = False


def start_game():
    global puffer, redfish_list, score, titan
    puffer_sprites = ['puffer', 'bigpuffer']
    redfish_left_sprites = ['redfish_left', 'redfish_left_big']
    redfish_right_sprites = ['redfish_right', 'redfish_right_big']
    titan_sprites = ['titan', 'titan_big', 'titan_left', 'titan_left_big']
    puffer = Puffer(puffer_sprites, (WIDTH//2, HEIGHT//2))
    titan = Titan(titan_sprites)
    redfish_list = []
    for i in range(0,3):
        redfish = Redfish(redfish_left_sprites, False)
        redfish_list.append(redfish)
    for i in range(0,2):
        redfish = Redfish(redfish_right_sprites, True)
        redfish_list.append(redfish)
    score = 0 

def stop_game():
    global game_running
    game_running = False
    puffer.actor.x, puffer.actor.y = WIDTH//2, HEIGHT//2
    for redfish in redfish_list:
        redfish.actor.x = -100 
    titan.actor.x = -100

def check_collision():
    global score    
    global game_running
    for redfish in redfish_list:
        if puffer.actor.colliderect(redfish.actor): 
            if puffer.is_puffed:
                score += 1 
                sounds.hurt.play()
                redfish.position_redfish_left() if redfish.direction == "left" else redfish.position_redfish_right()  # Reset position
            else:
                sounds.chomp.play()
                game_running = False
        if puffer.actor.colliderect(titan.actor):
            sounds.chomp.play()
            game_running = False

def update():
    global score
    global game_running

    if game_running:
        puffer.update()
        for redfish in redfish_list:
            redfish.update()
        titan.update()
        check_collision()

def draw_score():
    screen.draw.text("Score: " + str(score), (45, 30))

def on_mouse_down(pos):
    global game_running, music_muted
    if play_button.collidepoint(pos) and not game_running:
        game_running = True
        start_game()
    elif exit_button.collidepoint(pos):
        exit()
    elif mute_button.collidepoint(pos):
        if music_muted:
            sounds.background.play(loops=-1)
            music_muted = False
        else:
            sounds.background.stop()
            music_muted = True

def draw():
    screen.clear()
    if game_running:
        screen.blit('background', (0, 0))
        puffer.draw()
        titan.draw()
        for i in range(0,5):    
            redfish_list[i].draw()
        draw_score()
    else:
        screen.blit('play', (0, 0))
        screen.draw.text("Puffer Frenzy", center=(WIDTH // 2 - 5, 50), fontsize=50, color="white", background="black")
        screen.draw.text("Play", play_button.topleft, fontsize=40, color="white", background="black")
        screen.draw.text("Unmute" if music_muted else "Mute", mute_button.topleft, fontsize=40, color="white", background="black")
        screen.draw.text("Exit", exit_button.topleft, fontsize=40, color="white", background="black")
        
pgzrun.go()