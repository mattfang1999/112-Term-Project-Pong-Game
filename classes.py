
import pygame
import math 
import scenes
import random 
import audio


BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

screen_size = (600, 400)

speech = audio.Speech()


class Image(pygame.sprite.Sprite):
    
    def __init__(self, screen_size, width, height, filename, color=(255,0,0)):
        super().__init__()
        
        self.screen_size = screen_size
        self.angle = 0
       
        self.original_image = pygame.image.load(filename).convert()
        self.colorkey = self.original_image.get_at((0,0))
        
        self.original_image = pygame.transform.scale(self.original_image, (width, height))
       
        self.image = self.original_image
        self.image.set_colorkey(self.colorkey)
        self.rect = self.image.get_rect()
        
    
    def turnLeft(self):
        
        self.angle = (self.angle - 45) % 360

        
    def turnRight(self):

        self.angle = (self.angle + 45) % 360

        
    def update(self):
        
        old_center = self.rect.center
        
        self.image = pygame.transform.rotate(self.original_image, self.angle).convert()
        self.image.set_colorkey(self.colorkey)
     
       
        self.rect = self.image.get_rect(center=old_center)
        self.mask = pygame.mask.from_surface(self.image)

        self.olist = self.mask.outline()

        if self.olist:
            pygame.draw.lines(self.image, (0, 0, 0), 3, self.olist)
        
        
    def draw(self, screen):
        
        screen.blit(self.image, self.rect) 

class Pong(Image): 

    def __init__(self, screen_size, width, height, filename, color=(255,0,0)):

        super().__init__(screen_size, width, height, filename, color=(255, 0, 0))
        
        _centerx = screen_size[0] //2 
        _centery = screen_size[1] //2 
        self.radius = 10
        self.rect = pygame.Rect(_centerx-self.radius,
                                _centery-self.radius,
                                self.radius*2, self.radius*2)

        self.speedx = 4
        self.speedy = 6
        self.direction = [-0.5, 1] 

        self.hit_edge_left = False 
        self.hit_edge_right = False 
        self.score = 0 

    
    def checkCollision(self, player_paddle, ai_paddle):
        return pygame.sprite.collide_mask(self, player_paddle)

    def collisionFormula(self, paddle):

        #if self.checkCollision(self, player_paddle) or self.checkCollision(ai_paddle):
        relative_IntersectionY = paddle.rect.centery - self.rect.centery
        normal_IntersectionY = relative_IntersectionY / (paddle.rect.height /2)
        angleList = [3*math.pi/4, 2*math.pi/3, 5*math.pi/12]
        randomMaxAngle = angleList[random.randint(0,2)]
        bounce_angle = normal_IntersectionY * (randomMaxAngle )
        
        self.direction[0] = math.cos(bounce_angle)
        self.direction[1] = -1 * math.sin(bounce_angle)
        

    def update_ball_position(self):
        #update the position of the ball
        self.rect.centerx += self.direction[0] * self.speedx 
        self.rect.centery += self.direction[1] * self.speedy
    
    def reset(self):
        _centerx = screen_size[0] //2 
        _centery = screen_size[1] //2
        self.rect = pygame.Rect(_centerx-self.radius,
                                _centery-self.radius,
                                self.radius*2, self.radius*2)

        self.direction = [-1, 1]
        
    def reset_ball(self, player_paddle, ai_paddle):
        #Reset the ball if the ball crosses the sides
        if self.rect.right >= self.screen_size[0]-1:
            self.hit_edge_right = True
            player_paddle.score += 1
            print(self.rect.centery)
            self.reset()
            
        elif self.rect.left <= 0:
            self.hit_edge_left = True
            ai_paddle.score += 1
            self.reset()
            

    def collision_checks(self, player_paddle, ai_paddle):
        
    
        if self.rect.top <= 0:
            self.direction[1] * -1
            if self.direction[1] <0:
                self.direction[1] *= -1
          
        
        if self.rect.bottom >= self.screen_size[1] - 1:
            self.direction[1] *= -1
        
        
        #if the pong hits the paddles, change how the pong ball moves 
        if pygame.sprite.collide_mask(self, player_paddle):
            self.collisionFormula(player_paddle)
        '''
        
        if pygame.sprite.collide_rect(self, player_paddle):
            self.collisionFormula(player_paddle)'''
        
        if pygame.sprite.collide_mask(self, ai_paddle):
            self.collisionFormula(ai_paddle)
    
    
    def pong_and_bullet_collision(self, bullet):
        if pygame.sprite.collide_mask(self, bullet):
            self.direction[0] *= -1 
        

    def update(self, player_paddle, ai_paddle):
        
        super().update()
        
        #self.collision_checks(player_paddle, ai_paddle)
        self.update_ball_position()
        self.collision_checks(player_paddle, ai_paddle)
        self.reset_ball(player_paddle, ai_paddle)
        
        
        

class PlayerPaddle(Image):

    def __init__(self, screen_size, width, height, filename, bullet_group, ultimate_group, color=(255,0,0)):

        # speed and direction have to be before super() 
        self.speed = 3
        self.direction = 0
        self.bullet_group = bullet_group 
        self.ultimate_group = ultimate_group
        self.score = 0 
        
        self.MAX_MANA = 5
        self.mana = 0
        self.hasHit = False 
        self.mbWidth = 200
        self.mbHeight = 15
        self.mbBase = pygame.Surface((self.mbWidth, self.mbHeight))#Actual base is White part (not drawing the blue mana part)
        self.mbBase.fill(WHITE)
        
        
        super().__init__(screen_size, width, height, filename, color=(255, 0, 0))
        
        self.rect.centerx = 40
        self.rect.centery = screen_size[1] // 2

        self.rect.height = 100 
    
    def drawHB(self):
        if self.mana >=0:
            #Calculating the blue/mana part of the entire mana bar
            width = int((self.mana / self.MAX_MANA) * self.mbWidth)
            #create the actual white mana bar
            
            mb = pygame.Surface((width, self.mbHeight))
            mb.fill(BLUE)
            
            #blit the actual blue onto the white 
            self.mbBase.fill(WHITE)
            self.mbBase.blit(mb,(0,0))
            
            #put the health bar at top left 
            self.image.blit(self.mbBase, (100, 100))
        
    def gainMana(self):
        self.mana += 1
        self.drawHB()
        if self.mana > self.MAX_MANA:
            self.mana = 0 
    
    def loseMana(self):
        self.mana -= 1
        self.drawHB()
        if self.mana < 0:
            self.mana = 0
        
            
    def ultimateAudio(self):
        
        if self.mana == self.MAX_MANA:
            speech.record()
            if speech.isLoudEnough:
                ult = UltimateSpecial(screen_size, 100, 100, "images/blueball.png", color = (255, 0, 0))
                ult.rect.centerx = self.rect.centerx
                ult.rect.centery = self.rect.centery
                self.ultimate_group.add(ult)
                self.mana = 0
                self.drawHB()
                speech.isLoudEnough = False
            
        
    def update(self):

        self.rect.centery += self.direction*self.speed  
        
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen_size[1]-1:
            self.rect.bottom = self.screen_size[1]-1
              
        super().update()
        
        
        
            
        self.ultimateAudio()
            
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.direction = -1
            elif event.key == pygame.K_DOWN:
                self.direction = 1      
            elif event.key == pygame.K_LEFT:
                self.turnLeft()
            elif event.key == pygame.K_RIGHT:
                self.turnRight()
            elif event.key == pygame.K_u:
                bullet = Bullet(screen_size, 25, 25, "images/shuriken.jpg", color = (255, 0 , 0))
                bullet.rect.centerx = self.rect.centerx
                bullet.rect.centery = self.rect.centery 
                self.bullet_group.add(bullet)
            
                    
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP and self.direction == -1:
                self.direction = 0
            elif event.key == pygame.K_DOWN and self.direction == 1:
                self.direction = 0
                
    def draw(self, screen):
        
        super().draw(screen)
        screen.blit(self.mbBase, (100,100))

class Player2Paddle(Image):
    
    def __init__(self, screen_size, width, height, filename, bullet_group, ultimate_group, color=(255,0,0)):

         
        self.speed = 3
        self.direction = 0
        self.bullet_group = bullet_group
        
        self.ultimate_group = ultimate_group 
        self.score = 0 
        
        self.MAX_MANA = 5
        self.mana = 0
        self.hasHit = False 
        self.mbWidth = 200
        self.mbHeight = 15
        self.mbBase = pygame.Surface((self.mbWidth, self.mbHeight))#Actual base is White part (not drawing the blue mana part)
        self.mbBase.fill(WHITE)
        
        super().__init__(screen_size, width, height, filename, color=(255, 0, 0))
        
        self.rect.centerx = screen_size[0] - 40
        self.rect.centery = screen_size[1] // 2

        self.rect.height = 100 
        
    def drawHB(self):
        if self.mana >= 0:
            #Calculating the blue/mana part of the entire mana bar
            width = int((self.mana / self.MAX_MANA) * self.mbWidth)
            #create the actual white mana bar
            mb = pygame.Surface((width, self.mbHeight))
            mb.fill(BLUE)
            
            #blit the actual blue onto the white 
            self.mbBase.fill(WHITE)
            self.mbBase.blit(mb,(0,0))
            
            #put the health bar at top left 
            self.image.blit(self.mbBase, (800, 100))
        
    def gainMana(self):
        self.mana += 1
        self.drawHB()
        if self.mana > self.MAX_MANA:
            self.mana = 0 
            
    def loseMana(self):
        self.mana -= 1
        self.drawHB()
        if self.mana < 0:
            self.mana = 0
            
    def ultimateAudio(self):
        
        if self.mana == self.MAX_MANA:
            speech.record()
            if speech.isLoudEnough:
                
                ult = UltimateSpecial(screen_size, 100, 100, "images/blueball.png", color = (255, 0, 0))
                ult.rect.centerx = self.rect.centerx
                ult.rect.centery = self.rect.centery
                self.ultimate_group.add(ult)
                self.mana = 0
                self.drawHB()
                speech.isLoudEnough = False
        
    def update(self):
        
        self.rect.centery += self.direction*self.speed   

        super().update()
        
        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > self.screen_size[1]-1:
            self.rect.bottom = self.screen_size[1]-1
            
        self.ultimateAudio()
            
    def handle_event(self, event):
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.direction = -1
            elif event.key == pygame.K_s:
                self.direction = 1      
            elif event.key == pygame.K_a:
                self.turnLeft()
            elif event.key == pygame.K_d:
                self.turnRight()
            
            elif event.key == pygame.K_SPACE:
                bullet = Bullet(screen_size, 25, 25, "images/shuriken.jpg", color = (255, 0 , 0))
                bullet.rect.centerx = self.rect.centerx
                bullet.rect.centery = self.rect.centery 
                
                self.bullet_group.add(bullet)
            
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w and self.direction == -1:
                self.direction = 0
            elif event.key == pygame.K_s and self.direction == 1:
                self.direction = 0
                
    def draw(self, screen):
        
        super().draw(screen)
        screen.blit(self.mbBase, (800,100))
        
class AIPaddle(Image):

    final_y_position = None 
    runthis = False 

    def __init__(self, screen_size, width, height, filename, color=(255,0,0)):
        
       
        self.lifetime = pygame.time.get_ticks() + 2000
        
        self.positiveDir = False 
        self.MAX_MANA = 5
        self.mana = 0
        self.hasHit = False 
        self.mbWidth = 200
        self.mbHeight = 15
        self.mbBase = pygame.Surface((self.mbWidth, self.mbHeight))#Actual base is White part (not drawing the blue mana part)
        self.mbBase.fill(WHITE)
        
        super().__init__(screen_size, width, height, filename, color=(255, 0, 0))

        self.rect.centerx = screen_size[0] 
        self.rect.centery = screen_size[1] // 2

        self.rect.height = 100 
        self.rect.width = 10   

        self.time_to_move = False 
        self.speed = 3 
        self.score = 0 
        
        
    def drawHB(self):
        if self.mana >= 0:
            #Calculating the blue/mana part of the entire mana bar
            width = int((self.mana / self.MAX_MANA) * self.mbWidth)
            #create the actual white mana bar
            mb = pygame.Surface((width, self.mbHeight))
            mb.fill(BLUE)
            
            #blit the actual blue onto the white 
            self.mbBase.fill(WHITE)
            self.mbBase.blit(mb,(0,0))
            
            #put the health bar at top left 
            self.image.blit(self.mbBase, (800, 100))
            
    def gainMana(self):
        self.mana += 1
        self.drawHB()
        if self.mana > self.MAX_MANA:
            self.mana = 0 
            
    def loseMana(self):
        self.mana -= 1
        self.drawHB()
        if self.mana < 0:
            self.mana = 0

    def collision_with_wall_check(self):

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen_size[1]-1:
            self.rect.bottom = self.screen_size[1]-1 
            

    def normalMode(self, pong):
       
        if pong.rect.top < self.rect.top:
           
            self.rect.centery -= self.speed 
        elif pong.rect.bottom > self.rect.bottom:
           
            self.rect.centery += self.speed 
        

    def hardMode(self, pong, player_paddle):
        
        tempX = pong.rect.centerx
        tempY = pong.rect.centery
        tempXVel = pong.direction[0] * pong.speedx
        tempYVel = pong.direction[1] * pong.speedy
        print("Initial TempX", tempX, "Initial TempY", tempY)
        print("Initial Pong Direction:", pong.direction)
        print("Intial XVel", tempXVel, "Intial YVel", tempYVel)
        print("ScreenLimit is", pong.screen_size[0] - 100)
        
        while tempX < pong.screen_size[0]-100:
            
            #print("temp X ", tempX, "+ tempXVel", tempXVel)
            #print("Before update the final y position is", AIPaddle.final_y_position)
            tempX += tempXVel
            tempY += tempYVel
            #print("Tempx is now", tempX, "TempY is now", tempY)
            
            #print("Before tempY", tempYVel)
            if tempY >= pong.screen_size[1] or tempY <= 0:
                tempYVel *= -1 
            AIPaddle.final_y_position = int(tempY) 
            
        
        print("Final", AIPaddle.final_y_position)
         
    
    
    def update(self, pong, player_paddle):
        
        
        super().update()
        if scenes.SceneBase.game_mode == "Hard":
            if pong.direction[0] > 0 and pygame.sprite.collide_mask(pong, player_paddle) :
                #if pygame.sprite.collide_mask(pong, player_paddle):
                self.hardMode(pong, player_paddle)
           
        
        if AIPaddle.final_y_position != None:
            print("AI paddle position is", self.rect.centery)
            print("Desired position is", AIPaddle.final_y_position)
            if AIPaddle.final_y_position  < self.rect.centery:
                self.rect.centery -= self.speed
            elif AIPaddle.final_y_position  > self.rect.centery:
                self.rect.centery += self.speed
        
        
                        
        if scenes.SceneBase.game_mode == "Normal":
            self.normalMode(pong)

        self.collision_with_wall_check()
        
    def draw(self, screen):
        
        super().draw(screen)
        screen.blit(self.mbBase, (800,100))

    
class Bullet(Image):
    
    def __init__(self, screen_size, width, height, filename, color = (255, 0, 0)):
        
        super().__init__(screen_size, width, height, filename, color = (255, 0, 0))
        self.lifetime = pygame.time.get_ticks() + 2000
        
    def checkCollision(self, thing):
        
        return pygame.sprite.collide_mask(self, thing)
    
    def checkCollisionWithOpponent(self, paddle):
        if self.checkCollision(paddle):
            self.kill()
            paddle.loseMana()
            
    def removeBullet(self, powerup, player_paddle):
        if self.checkCollision(powerup):
            self.kill()
            powerup.kill()
            player_paddle.gainMana()
        
        
    def update(self, powerup, player_paddle, ai_paddle, dx):
        self.rect.centerx += dx
        self.removeBullet(powerup, player_paddle)
        self.checkCollisionWithOpponent(ai_paddle)
        

class PowerUp(Image):
    
    kill_time = 0
    def __init__(self, screen_size, width, height, filename,  color = (255, 0, 0)):
        
        super().__init__(screen_size, width, height, filename, color = (255, 0 , 0))
        
        _centerx = random.randint(20, 1100) 
        _centery = random.randint(20, 780)
        self.radius = 10
        self.rect = pygame.Rect(_centerx-self.radius,
                                _centery-self.radius,
                                self.radius*2, self.radius*2)
                                
    def update(self):
        pass 
        

class UltimateSpecial(Image):
    
    def __init__(self, screen_size, width, height, filename,  color = (255, 0, 0)):
        
        self.direction = [1, 1]
        super().__init__(screen_size, width, height, filename, color = (255, 0 , 0))
    
    
    def checkCollision(self, paddle):
        
        return pygame.sprite.collide_mask(self, paddle)
    
    def update(self, dx):
        
        super().update()
        self.rect.centerx += dx
        
        