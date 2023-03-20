from utime import sleep, sleep_ms
from machine import Pin, ADC, I2C
from sh1106 import SH1106_I2C

import random
import time
import gfx

# CREATE PLAYER 1
btnPlayer_1 = Pin(25, Pin.IN, Pin.PULL_UP)
xPlayer_1 = ADC(Pin(33))
yPlayer_1 = ADC(Pin(32))

xPlayer_1.atten(ADC.ATTN_11DB)
yPlayer_1.atten(ADC.ATTN_11DB)

xPlayer_1.width(ADC.WIDTH_12BIT)
yPlayer_1.width(ADC.WIDTH_12BIT)

# CREATE PLAYER 2
btnPlayer_2 = Pin(27, Pin.IN, Pin.PULL_UP)
xPlayer_2 = ADC(Pin(12))
yPlayer_2 = ADC(Pin(14))

xPlayer_2.atten(ADC.ATTN_11DB)
yPlayer_2.atten(ADC.ATTN_11DB)

xPlayer_2.width(ADC.WIDTH_12BIT)
yPlayer_2.width(ADC.WIDTH_12BIT)

# CREATE OLED
i2c = I2C(scl=Pin(22), sda=Pin(23)) 
oled = SH1106_I2C(128, 64, i2c, None, addr=0x3C)
graphics = gfx.GFX(128, 64, oled.pixel)
oled.sleep(False)

ball_x = 64
ball_y = 32

# Attributes Player 1
p1_x = 12
p1_y = [25,40]

# Attributes Player 2
p2_x = 116
p2_y = [25,40]

point_P1 = 0
point_P2 = 0

speed_player = 4

# Time in game
time = 0
player_win = 0

speed_x = 2
speed_y = 2

randomDirectionX = [1,-1]

direcction_x = randomDirectionX[random.randrange(0,2)]
direcction_y = random.randrange(-1,2)

# GLOBAL GAME
intro = True
startGame = True

while True:
    while intro:        
        
        # TITLE GAME
        graphics.fill_rect(0,0,25,20,1)
        graphics.fill_rect(0,10,10,25,1)
        graphics.fill_rect(10,3,12,13,0)

        graphics.fill_rect(30,0,25,35,1)
        graphics.fill_rect(38,5,13,25,0)

        graphics.fill_rect(63, 0, 30, 35,1)
        graphics.fill_triangle(75,0,85,0,85,20,0)
        graphics.fill_triangle(70,35, 80, 35, 70, 20,0)

        graphics.fill_rect(100,0,30,35,1)
        graphics.fill_rect(108,7,20,10,0)
        graphics.fill_rect(108,10,7,20,0)
        graphics.fill_rect(108,20,13,10,0)

        oled.show()

        sleep(2.5)

        # POSITION TITLE AND START LABEL
        xValueTitle = 0
        yValueStart = 45

        firstScreen = True

        while firstScreen:
                
            if btnPlayer_1.value() and btnPlayer_2.value():
                oled.text("PRESS TO START", 8, 45, 1)
                oled.show()
                sleep(0.4)    
                oled.text("PRESS TO START", 8, 45, 0)
                oled.show()
                sleep(0.4)    
            else:        
                oled.text("PRESS TO START", 8, 45, 1)
                oled.show()
                
                while firstScreen:
                    
                    if xValueTitle < 65:        
                        graphics.fill_rect(xValueTitle, 0, xValueTitle + 4, 35, 0)
                        oled.show()
                        xValueTitle += 1
                        
                    if xValueTitle >= 65:
                        graphics.line(0, yValueStart, 120, yValueStart, 0)
                        oled.show()
                        yValueStart += 1
                        
                        if yValueStart > 60:
                            firstScreen = False
                            intro = False
                            startGame = True

        print("Start the game")
        oled.fill(0)
        oled.show()

        sleep(1)
        
    while startGame:        
        #print("Position Ball: x:{}, y:{}".format(ball_x, ball_y))
        #print("Position P1: x: {}, y: {}".format(p1_x,p1_y))
        #print("Position P2: x: {}, y: {}".format(p2_x,p2_y))
        if point_P1 < 7 or point_P2 < 7:
            
            sleep(0.005)
            
            #Score board
            oled.text("{}:{}".format(point_P1, point_P2), 92, 0, 1)
            
            #Map
            graphics.line(0, 3, 90, 3, 1)
            graphics.line(0, 3, 0, 62, 1)
            graphics.line(0, 61, 128, 61, 1)
            graphics.line(127, 3, 127, 62, 1)
            graphics.line(117, 3, 127, 3, 1)
            
            #Ball
            graphics.fill_circle(ball_x, ball_y, 2, 1)
            
            #Line Player 1
            graphics.line(p1_x, p1_y[0], p1_x, p1_y[1], 1)
            
            #Line Player 2
            graphics.line(p2_x, p2_y[0], p2_x, p2_y[1], 1)
            
            yValuePlayer_1 = yPlayer_1.read()
            yValuePlayer_2 = yPlayer_2.read()
            
            oled.show()
            
            # Move Ball to Right
            if direcction_x == 1 and direcction_y == 0:
                if ball_x < 128 and ball_y < 64:
                    oled.show()
                    graphics.fill_circle(ball_x, ball_y, 2, 0)
                    ball_x = ball_x + (speed_x * direcction_x)
            
            # Move ball to Left
            if direcction_x == -1 and direcction_y == 0:
                if ball_x < 128 and ball_y < 64:
                    oled.show()
                    graphics.fill_circle(ball_x, ball_y, 2, 0)
                    ball_x = ball_x + (speed_x * direcction_x)
                
            # Move ball to 1, -1
            if direcction_x == 1 and direcction_y == -1:
                if ball_y > (4 + speed_y):
                    oled.show()
                    graphics.fill_circle(ball_x, ball_y, 2, 0)
                    ball_x = ball_x + (speed_x * direcction_x)
                    ball_y = ball_y + (speed_y * direcction_y)
                if ball_y <= (4 + speed_y):
                    direcction_x = 1
                    direcction_y = 1
           
            #Move ball to 1,1
            if direcction_x == 1 and direcction_y == 1:
                if ball_y < (60 - speed_y):
                    oled.show()
                    graphics.fill_circle(ball_x, ball_y, 2, 0)
                    ball_x = ball_x + (speed_x * direcction_x)
                    ball_y = ball_y + (speed_y * direcction_y)
                if ball_y >= (60 - speed_y):
                    direcction_x = 1
                    direcction_y = -1
                    
            #Move ball to -1,-1
            if direcction_x == -1 and direcction_y == -1:
                if ball_y > (4 + speed_y):
                    oled.show()
                    graphics.fill_circle(ball_x, ball_y, 2, 0)
                    ball_x = ball_x + (speed_x * direcction_x)
                    ball_y = ball_y + (speed_y * direcction_y)
                if ball_y <= (4 + speed_y):
                    direcction_x = -1
                    direcction_y = 1
            #Move ball to -1,1
            if direcction_x == -1 and direcction_y == 1:
                if ball_y < (60 - speed_y):
                    oled.show()
                    graphics.fill_circle(ball_x, ball_y, 2, 0)
                    ball_x = ball_x + (speed_x * direcction_x)
                    ball_y = ball_y + (speed_y * direcction_y)
                if ball_y >= (60 - speed_y):
                    direcction_x = -1
                    direcction_y = -1
                
            # Bounce player 1
            if (ball_x <= (p1_x + speed_x)) and ((p1_y[0]) <= (ball_y + 2) <= (p1_y[1] + 4)):
                if p1_y[0] <= (ball_y + 2) <= (p1_y[0] + 6):
                    direcction_x = 1
                    direcction_y = -1
                    
                if (p1_y[0] + 7) <= (ball_y + 2) <= (p1_y[0] + 10):
                    direcction_x = 1
                    direcction_y = 0
                    
                if (p1_y[0] + 11) <= (ball_y + 2) <= (p1_y[0] + 17):
                    direcction_x = 1
                    direcction_y = 1
                
                time += 1
                
                if time == 3:
                    speed_x += 2
                    speed_y += 2
                    speed_player += 2
                
                if time == 6:
                    speed_x += 2
                    speed_y += 2
                    
                if time == 10:
                    speed_x += 1
                    speed_y += 1
                
            # Bounce player 2
            if (ball_x >= (p2_x - speed_x)) and ((p2_y[0]) <= (ball_y + 2) <= (p2_y[1] + 4)):
                if p2_y[0] <= (ball_y + 2) <= (p2_y[0] + 6):
                    direcction_x = -1
                    direcction_y = -1
                    
                if (p2_y[0] + 7) <= (ball_y + 2) <= (p2_y[0] + 10):
                    direcction_x = -1
                    direcction_y = 0
                    
                if (p2_y[0] + 11) <= (ball_y + 2) <= (p2_y[0] + 17):
                    direcction_x = -1
                    direcction_y = 1
                    
                time += 1
                
                if time == 3:
                    speed_x += 2
                    speed_y += 2
                    speed_player += 2
                
                if time == 6:
                    speed_x += 2
                    speed_y += 2
                    
                if time == 10:
                    speed_x += 1
                    speed_y += 1
            
            # Point when ball_x < p1
            if ball_x <= 0:
                oled.text("{}:{}".format(point_P1, point_P2), 92, 0, 0)       
                # Reset game
                graphics.line(p1_x, p1_y[0], p1_x, p1_y[1], 0)
                graphics.line(p2_x, p2_y[0], p2_x, p2_y[1], 0)
                
                graphics.fill_circle(ball_x, ball_y, 2, 0)
                
                ball_x = 64
                ball_y = 32
                
                speed_player = 4
                time = 0
                
                speed_x = 2
                speed_y = 2
                
                p1_y = [25,39]
                p2_y = [25,39]
                
                direcction_x = randomDirectionX[random.randrange(0,2)]
                direcction_y = random.randrange(-1,2)
                
                point_P2 += 1
            
            # Point when ball_x > p2
            if ball_x >= 128:
                oled.text("{}:{}".format(point_P1, point_P2), 92, 0, 0)        
                # Reset game
                graphics.line(p1_x, p1_y[0], p1_x, p1_y[1], 0)
                graphics.line(p2_x, p2_y[0], p2_x, p2_y[1], 0)
                
                graphics.fill_circle(ball_x, ball_y, 2, 0)
                
                ball_x = 64
                ball_y = 32
                
                speed_x = 2
                speed_y = 2
                
                speed_player = 4
                time = 0
                
                p1_y = [25,39]
                p2_y = [25,39]
                
                direcction_x = randomDirectionX[random.randrange(0,2)]
                direcction_y = random.randrange(-1,2)
                
                point_P1 += 1
                
            #MOVE PLAYER 1
            if yValuePlayer_1 < 1200:
                if p1_y[0] > 8:            
                    graphics.line(p1_x, p1_y[0], p1_x, p1_y[1], 0)
                    p1_y[0] -= speed_player
                    p1_y[1] -= speed_player
            
            if yValuePlayer_1 > 2100:
                if p1_y[1] < 57:
                    graphics.line(p1_x, p1_y[0], p1_x, p1_y[1], 0)
                    p1_y[0] += speed_player
                    p1_y[1] += speed_player
                    
            # MOVE PLAYER 2
            if yValuePlayer_2 < 1200:
                if p2_y[0] > 8:            
                    graphics.line(p2_x, p2_y[0], p2_x, p2_y[1], 0)
                    p2_y[0] -= speed_player
                    p2_y[1] -= speed_player
            
            if yValuePlayer_2 > 2100:
                if p2_y[1] < 57:
                    graphics.line(p2_x, p2_y[0], p2_x, p2_y[1], 0)
                    p2_y[0] += speed_player
                    p2_y[1] += speed_player
                
        # Player 1 Win
        if point_P1 == 7:
            player_win = 1
            #Score board
            oled.text("{}:{}".format(point_P1, point_P2), 92, 0, 1)
            
            #Map
            graphics.line(0, 3, 90, 3, 1)
            graphics.line(0, 3, 0, 62, 1)
            graphics.line(0, 61, 128, 61, 1)
            graphics.line(127, 3, 127, 62, 1)
            graphics.line(117, 3, 127, 3, 1)
            
            #PLAYER 1
            graphics.line(p1_x, p1_y[0], p1_x, p1_y[1], 1)
            
            for i in range(200):            
                graphics.line(p2_x, p2_y[0], p2_x, p2_y[1], 1)
                oled.show()
                
                if i % 2 == 0:
                    graphics.line(p2_x, p2_y[0], p2_x, p2_y[1], 0)
                    graphics.line(p2_x - 4, p2_y[0], p2_x + 4, p2_y[1], 1)
                    oled.show()
                    graphics.line(p2_x - 4, p2_y[0], p2_x + 4, p2_y[1], 0)
                else:
                    graphics.line(p2_x, p2_y[0], p2_x, p2_y[1], 0)
                    graphics.line(p2_x + 4, p2_y[0], p2_x - 4, p2_y[1], 1)
                    oled.show()
                    graphics.line(p2_x + 4, p2_y[0], p2_x - 4, p2_y[1], 0)
            
            graphics.line(p2_x, p2_y[0], p2_x, p2_y[1], 0)
            
            oled.show()
            
            for i in range(30):
                graphics.circle(116, 35, i, 1)
                oled.show()
                graphics.circle(116, 35, i, 0)
            
            oled.fill(0)
            oled.show()
            
            sleep(2)
        
        # Player 2 Win
        if point_P2 == 7:
            player_win = 2
            #Score board
            oled.text("{}:{}".format(point_P1, point_P2), 92, 0, 1)
            
            #Map
            graphics.line(0, 3, 90, 3, 1)
            graphics.line(0, 3, 0, 62, 1)
            graphics.line(0, 61, 128, 61, 1)
            graphics.line(127, 3, 127, 62, 1)
            graphics.line(117, 3, 127, 3, 1)
            
            #PLAYER 2
            graphics.line(p2_x, p2_y[0], p2_x, p2_y[1], 1)
            
            for i in range(200):            
                graphics.line(p1_x, p1_y[0], p1_x, p1_y[1], 1)
                oled.show()
                
                if i % 2 == 0:
                    graphics.line(p1_x, p1_y[0], p1_x, p1_y[1], 0)
                    graphics.line(p1_x - 4, p1_y[0], p1_x + 4, p1_y[1], 1)
                    oled.show()
                    graphics.line(p1_x - 4, p1_y[0], p1_x + 4, p1_y[1], 0)
                else:
                    graphics.line(p1_x, p1_y[0], p1_x, p1_y[1], 0)
                    graphics.line(p1_x + 4, p1_y[0], p1_x - 4, p1_y[1], 1)
                    oled.show()
                    graphics.line(p1_x + 4, p1_y[0], p1_x - 4, p1_y[1], 0)
            
            graphics.line(p1_x, p1_y[0], p1_x, p1_y[1], 0)
            
            oled.show()
            
            for i in range(30):
                graphics.circle(12, 35, i, 1)
                oled.show()
                graphics.circle(12, 35, i, 0)
            
            oled.fill(0)
            oled.show()
            
            sleep(2)
        
        # PLAY AGAIN OPTIONS
        
        if player_win != 0:
            selectOption = False
            YES = False
            
            oled.text("PLAYER {} WINS".format(player_win), 12, 20, 1)
            oled.show()
            sleep(4)
            
            oled.text("PLAY AGAYN?", 20, 30, 1)
            oled.text("YES", 35, 50, 1)
            oled.text("NO", 75, 50, 1)
                
            while not selectOption:
                oled.show()
                xPlayer1Value = xPlayer_1.read()
                xPlayer2 = xPlayer_2.read()
                
                if xPlayer1Value > 2800:
                    graphics.fill_rect(33, 47, 28, 12, 1)
                    oled.text("YES", 35, 50, 0)
                    
                    graphics.fill_rect(73, 47, 20, 12, 0)
                    oled.text("NO", 75, 50, 1)
                    YES = True
                
                if xPlayer1Value < 1400:
                    graphics.fill_rect(73, 47, 20, 12, 1)
                    oled.text("NO", 75, 50, 0)
                    
                    graphics.fill_rect(33, 47, 28, 12, 0)
                    oled.text("YES", 35, 50, 1)
                    YES = False
                
                if (not btnPlayer_1.value() and YES):
                    startGame = True
                    intro = False
                    selectOption = True
                    
                    # Reset game
                    graphics.line(p1_x, p1_y[0], p1_x, p1_y[1], 0)
                    graphics.line(p2_x, p2_y[0], p2_x, p2_y[1], 0)
                    
                    graphics.fill_circle(ball_x, ball_y, 2, 0)
                    
                    point_P1 = 0
                    point_P2 = 0
                    
                    ball_x = 64
                    ball_y = 32
                    
                    speed_player = 4
                    time = 0
                    
                    speed_x = 2
                    speed_y = 2
                    
                    p1_y = [25,39]
                    p2_y = [25,39]
                    
                    player_win = 0
                    
                    direcction_x = randomDirectionX[random.randrange(0,2)]
                    direcction_y = random.randrange(-1,2)
                    
                    oled.fill(0)
                    oled.show()
                
                if (not btnPlayer_1.value() and not YES):
                    startGame = False
                    intro = True
                    selectOption = True
                    
                    # Reset game
                    graphics.line(p1_x, p1_y[0], p1_x, p1_y[1], 0)
                    graphics.line(p2_x, p2_y[0], p2_x, p2_y[1], 0)
                    
                    graphics.fill_circle(ball_x, ball_y, 2, 0)
                    
                    point_P1 = 0
                    point_P2 = 0
                    
                    ball_x = 64
                    ball_y = 32
                    
                    speed_player = 4
                    time = 0
                    
                    speed_x = 2
                    speed_y = 2
                    
                    p1_y = [25,39]
                    p2_y = [25,39]
                    
                    player_win = 0
                    
                    direcction_x = randomDirectionX[random.randrange(0,2)]
                    direcction_y = random.randrange(-1,2)
                    
                    oled.fill(0)
                    oled.show()
            
                
  