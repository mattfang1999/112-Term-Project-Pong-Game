import pygame
import os 
import classes
import random


####COLORS
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255,0,0)
GREEN = (0,255,0)
ORANGE = (255, 205, 0)
#########

screen = pygame.display.set_mode((800, 400))
pygame.init()

 
screen_size = (1200, 800)

#################CITATION
#Some of the button logic taken from this website
#https://pythonprogramming.net/making-interactive-pygame-buttons/
###############################
class Button():
    def __init__(self, txt, location, action, bg=WHITE, fg=BLACK, size=(200, 200), font_name="Moyko", font_size=35):
        self.color = bg  # the static (normal) color
        self.bg = bg  # actual background color, can change on mouseover
        self.fg = fg  # text color
        self.size = size

        self.font = pygame.font.SysFont(font_name, font_size)
        self.txt = txt
        self.txt_surf = self.font.render(self.txt, 1, self.fg)
        self.txt_rect = self.txt_surf.get_rect(center=[s//2 for s in self.size])

        self.surface = pygame.surface.Surface(size)
        self.rect = self.surface.get_rect(center=location)

        self.call_back_ = action

    def draw(self):
        self.mouseover()

        self.surface.fill(self.bg)
        self.surface.blit(self.txt_surf, self.txt_rect)
        screen.blit(self.surface, self.rect)

    def mouseover(self):
        self.bg = self.color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.bg = GREY  # mouseover color

    def call_back(self):
        self.call_back_()

############################
########Functions to change mode

def mousebuttondown(button):
    pos = pygame.mouse.get_pos()
   
    if button.rect.collidepoint(pos):
        button.call_back()
        
#########################


##############################################CITATION
#Much of the Scene Logic was taken from this website:
#http://www.nerdparadise.com/programming/pygame/part7
#######################################################


class SceneBase:
    number_of_players = None
    is_game_over = False 
    third_player_mode = None 
    game_mode = None
    player1_character = None 
    player2_character = None 
    winner = None 
  
    characterlist = ["images/naruto.png", "images/aang.png", "images/yugi.png", "images/goku.png"]
    
    def __init__(self):
        self.next = self
    
    def ProcessInput(self, events, pressed_keys):
        pass

    def Update(self):
        pass

    def Render(self, screen):
        pass

    def SwitchToScene(self, next_scene):
        self.next = next_scene
    
    def Terminate(self):
        self.SwitchToScene(None)
        
class TitleScreen(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        
        #create button 
        self.play_button = Button("Play", (200, 300), self.switch_to_choosenumberofplayerscreen)
        self.instruction_button = Button("Instructions", (200, 500), self.switch_to_instructionscreen)
        #create font
        self.my_font = pygame.font.SysFont("Moyko", 100)
        #create background
        self.bg = pygame.image.load("images/bamboo.jpg")
        
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Move to the next scene when the user pressed Enter 
                self.SwitchToScene(GameScreen())
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousebuttondown(self.play_button)
                mousebuttondown(self.instruction_button)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                self.SwitchToScene(TwoPlayerScreen()) 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_o:
                self.SwitchToScene(ChooseNumberOfPlayerScreen())
    
    def Update(self):
        pass 
        
        
    def Render(self, screen):
        #draw the background
        screen.blit(self.bg, (0, 0))
        #Draw the text here 
        textImage = self.my_font.render("Anime Pong", True, (BLACK))
        screen.blit(textImage, (screen_size[0] // 2 - 100, screen_size[1] // 2))
        #Just draw the button here 
        self.play_button.draw()
        self.instruction_button.draw()
        
    def switch_to_gamescreen(self):
        self.SwitchToScene(GameScreen())
    
    def switch_to_difficultyscreen(self):
        self.SwitchToScene(DifficultyScreen())
    def switch_to_choosenumberofplayerscreen(self):
        self.SwitchToScene(ChooseNumberOfPlayerScreen())
    def switch_to_instructionscreen(self):
        self.SwitchToScene(InstructionsScreen())
    
    def SwitchToScene(self, next_scene):
        self.next = next_scene

class InstructionsScreen(SceneBase):
    def __init__(self):
        
        SceneBase.__init__(self)
        
        self.my_font = pygame.font.SysFont("Moyko", 30)
        self.bg = pygame.image.load("images/bamboo.jpg")
    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.SwitchToScene(ChooseNumberOfPlayerScreen())
    
    def Render(self, screen):
        #draw the background
        screen.blit(self.bg, (0, 0))
        #Draw the text here 
        textImage = self.my_font.render("Get the PokeBall to the Other Side!", True, (BLACK))
        textImage2 = self.my_font.render("Don't Let the opponent score on you!", True, (BLACK))
        textImage3 = self.my_font.render("Hit the Ramens to increase your Mana!", True, (BLACK))
        textImage4 = self.my_font.render("Once you reach full mana, scream to unleash your special!", True, (BLACK))
        textImage5 = self.my_font.render("Player One: Up/Down to Move, Left/Right to Rotate, U to shoot, i/k to move special", True, (BLACK))
        textImage6 = self.my_font.render("Player Two: W/S to Move, A/D to Rotate, Space to shoot, r/f to move special", True, (BLACK))
        textImage7 = self.my_font.render("Click Enter to Continue", True, (BLACK))
        
        screen.blit(textImage, (0, 100))
        screen.blit(textImage2,(0, 200))
        screen.blit(textImage3,(0, 300))
        screen.blit(textImage4,(0, 400))
        screen.blit(textImage5,(0, 500))
        screen.blit(textImage6,(0, 600))
        screen.blit(textImage7,(0, 700))
        
        
        
class ChooseNumberOfPlayerScreen(SceneBase):
    
    def __init__(self):
        
        SceneBase.__init__(self)
        
        self.one_player_button = Button("One", (400, 400), self.choose_one_player_mode, bg = GREEN)
        self.two_player_button = Button("Two", (850,400), self.choose_two_player_mode, bg = GREEN)
        
        self.my_font = pygame.font.SysFont("Moyko", 50)
        self.bg = pygame.image.load("images/bamboo.jpg")
        
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousebuttondown(self.one_player_button)
                mousebuttondown(self.two_player_button)
    
    def Render(self, screen):
        #draw the background
        screen.blit(self.bg, (0, 0))
        #Draw the text here 
        textImage = self.my_font.render("How many people will be in my dojo today?", True, (BLACK))
        screen.blit(textImage, (200, 100))
        #Just draw the button here 
        self.one_player_button.draw()
        self.two_player_button.draw()
    
    def choose_one_player_mode(self):
        SceneBase.number_of_players = 1
        self.SwitchToScene(ChooseCharacterScreen())
    def choose_two_player_mode(self):
        SceneBase.number_of_players = 2 
        self.SwitchToScene(ChooseCharacterScreen())
        
    def SwitchToScene(self, next_scene):
        self.next = next_scene
    

class ChooseCharacterScreen(SceneBase):
    
    def __init__(self):
        SceneBase.__init__(self)
            
        self.my_font = pygame.font.SysFont("Moyko", 50)
        
        self.bg = pygame.image.load("images/narutohead.jpg")
        self.bg2 = pygame.image.load("images/aangface.jpg")
        self.bg3 = pygame.image.load("images/gokuface.jpg")
        self.bg4 = pygame.image.load("images/yugiface.jpg")
        
        
        
        self.naruto_button = Button("Naruto", (200, 600), self.clicked_on_naruto, bg = RED)
        self.aang_button = Button("Aang", (500, 600), self.clicked_on_aang, bg = ORANGE)
        self.goku_button = Button("Goku", (800, 600), self.clicked_on_goku, bg = RED)
        self.yugi_button = Button("Yugi", (1100, 600), self.clicked_on_yugi, bg = ORANGE)
        
        self.ButtonClicked = False 
        
        
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousebuttondown(self.naruto_button)
                mousebuttondown(self.aang_button)
                mousebuttondown(self.goku_button)
                mousebuttondown(self.yugi_button)
    
    def Render(self, screen):
        
        screen.blit(self.bg, (0, 0))
        screen.blit(self.bg2, (300,0))
        screen.blit(self.bg3, (600,0))
        screen.blit(self.bg4, (900,0))
        self.naruto_button.draw()
        self.aang_button.draw()
        self.goku_button.draw()
        self.yugi_button.draw()
        
        textImage = self.my_font.render("Choose your companions!", True, (RED))
        screen.blit(textImage, (200, 100))
    
    def Update(self):
        pass 
        
        
    def SwitchToScene(self, next_scene):
        self.next = next_scene 
    #If it's one player mode, you click on a button. Assign that button to first player. Then go to the game.
    #If it's two player mode, you click on a button. Assign that button to first player. You click on another button. Then go to game. 
    
    def clicked_on_naruto(self):
        if SceneBase.number_of_players == 1:
            SceneBase.player1_character = "images/naruto.png"
            SceneBase.characterlist.remove("images/naruto.png")
            self.SwitchToScene(DifficultyScreen())
        if SceneBase.number_of_players == 2 and self.ButtonClicked:
            SceneBase.player2_character = "images/naruto.png"
            self.SwitchToScene(GameScreen())
        if SceneBase.number_of_players == 2 and self.ButtonClicked == False:
            SceneBase.player1_character = "images/naruto.png"
            self.ButtonClicked = True 
        
    
    def clicked_on_aang(self):
        if SceneBase.number_of_players == 1:
            SceneBase.player1_character = "images/aang.png"
            SceneBase.characterlist.remove("images/aang.png")
            self.SwitchToScene(DifficultyScreen())
        if SceneBase.number_of_players == 2 and self.ButtonClicked:
            SceneBase.player2_character = "images/aang.png"
            self.SwitchToScene(TwoPlayerScreen()) # <-- TwoPlayerScreen instead of GameScene
        if SceneBase.number_of_players == 2 and self.ButtonClicked == False:
            SceneBase.player1_character = "images/aang.png"
            self.ButtonClicked = True 
        
    
    def clicked_on_yugi(self):
        if SceneBase.number_of_players == 1:
            SceneBase.player1_character = "images/yugi.png"
            SceneBase.characterlist.remove("images/yugi.png")
            self.SwitchToScene(DifficultyScreen())
        if SceneBase.number_of_players == 2 and self.ButtonClicked:
            SceneBase.player2_character = "images/yugi.png"
            self.SwitchToScene(TwoPlayerScreen()) # <-- TwoPlayerScreen instead of GameScene
        if SceneBase.number_of_players == 2 and self.ButtonClicked == False:
            SceneBase.player1_character = "images/yugi.png"
            self.ButtonClicked = True 
        
    
    def clicked_on_goku(self):
        if SceneBase.number_of_players == 1:
            SceneBase.player1_character = "images/goku.png"
            SceneBase.characterlist.remove("images/goku.png")
            self.SwitchToScene(DifficultyScreen())
        if SceneBase.number_of_players == 2 and self.ButtonClicked:
            
            SceneBase.player2_character = "images/goku.png"
            self.SwitchToScene(TwoPlayerScreen()) # <-- TwoPlayerScreen instead of GameScene
        if SceneBase.number_of_players == 2 and self.ButtonClicked == False:
            
            SceneBase.player1_character = "images/goku.png"
            self.ButtonClicked = True 
        
        
class DifficultyScreen(SceneBase):
    def __init__(self):
        SceneBase.__init__(self)
        self.bg = pygame.image.load("images/bamboo2.jpg")
        self.normal_button = Button("Normal", (800, 300), self.change_to_normalmode, bg = GREEN)
        self.hard_button = Button("Hard", (800, 500), self.change_to_hardmode, bg = GREEN)
        
        self.my_font = pygame.font.SysFont("Moyko", 100)
        
    def ProcessInput(self, events, pressed_keys):
        
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.SwitchToScene(GameScreen())
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousebuttondown(self.normal_button)
                mousebuttondown(self.hard_button)
                
    def Update(self):
        
        if SceneBase.game_mode == "None":
            textImage = self.my_font.render("CHOOSE YOUR DIFFICULTY YOUNG GRASSHOPPER", True, BLACK)
            screen.blit(textImage, (100, 500))
           
        if SceneBase.game_mode == "Normal":
            textImage = self.my_font.render("I see you want to warm up a little!", True, BLACK)
            
            #screen.blit(textImage, (300, 500))
        if SceneBase.game_mode == "Hard":
            textImage = self.my_font.render("A good test to see your skills!", True, BLACK)
            #screen.blit(textImage, (300, 500))
        
    def Render(self, screen):
        # The game scene is just a blank blue screen 
        screen.blit(self.bg, (0, 0))
        
        self.normal_button.draw()
        self.hard_button.draw()
        
        textImage = self.my_font.render("Choose a Difficulty Mode!", True, BLACK)
        screen.blit(textImage, (400,100))
     
    def change_to_hardmode(self):
        
        SceneBase.game_mode = "Hard"
        print(SceneBase.game_mode)
        if SceneBase.number_of_players == 1:
            self.SwitchToScene(GameScreen())
        elif SceneBase.number_of_players == 2:
            self.SwitchToScene(TwoPlayerScreen())
            
    
    def change_to_normalmode(self):
        
        SceneBase.game_mode = "Normal"
        if SceneBase.number_of_players == 1:
            self.SwitchToScene(GameScreen())
        elif SceneBase.number_of_players == 2:
            self.SwitchToScene(TwoPlayerScreen())
    

class GameScreen(SceneBase):
    
    randomNumber = random.randint(0, 2)
    
    def __init__(self):
        SceneBase.__init__(self)
        self.bg = pygame.image.load("images/asianbackground.jpg")
        self.my_font = pygame.font.SysFont("Arial", 50)
        
        self.bullets_group = pygame.sprite.Group()
       
        self.powerup_group = pygame.sprite.Group()
        self.ultimate_group = pygame.sprite.Group()
        self.player_paddle = classes.PlayerPaddle(screen_size, 100, 100, SceneBase.player1_character, self.bullets_group, self.ultimate_group)
        
        self.ai_paddle = classes.AIPaddle(screen_size, 100, 200, SceneBase.characterlist[GameScreen.randomNumber])
        self.pong = classes.Pong(screen_size, 20, 20, "images/pokeball.png")
        
        self.now1 = pygame.time.get_ticks()
        
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            self.player_paddle.handle_event(event)
            
            for ultimate in self.ultimate_group:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                    ultimate.rect.centery -= 10
                if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                    ultimate.rect.centery += 10
                
            
    def Update(self):
    
        #update the objects
        self.player_paddle.update() 
        self.ai_paddle.update(self.pong, self.player_paddle)
        self.pong.update(self.player_paddle, self.ai_paddle)
        
        
        for bullet in self.bullets_group:
            self.pong.pong_and_bullet_collision(bullet)
       
        
        # if someone reaches a score of 2, then exit the game 
        if self.player_paddle.score == 5:
            SceneBase.winner = "Player 1"
            SceneBase.is_game_over = True 
            self.SwitchToScene(GameOverScreen())
        elif self.ai_paddle.score == 5:
            SceneBase.winner = "You Lose!"
            SceneBase.is_game_over = True 
            self.SwitchToScene(GameOverScreen())
            
        
        time_difference1 = pygame.time.get_ticks() - self.now1
        
        current_time = pygame.time.get_ticks()
        
        if time_difference1 >= 2000:
            powerup = classes.PowerUp(screen_size, 40, 40, "images/ramen.png")
            powerup.kill_time = current_time + 5000
            self.powerup_group.add(powerup)
            self.now1 = pygame.time.get_ticks()
            
        current_time = pygame.time.get_ticks()
        
        #kill powerups after a while 
        for powerup in self.powerup_group:
            for bullet in self.bullets_group:
                bullet.update(powerup, self.player_paddle, self.ai_paddle, 3)
            if powerup.kill_time <= current_time:
                self.powerup_group.remove(powerup)
        
        for ultimate in self.ultimate_group:
            ultimate.update(3)
            if ultimate.checkCollision(self.ai_paddle):
                SceneBase.is_game_over = True 
                self.SwitchToScene(GameOverScreen())
                
            
    def Render(self, screen):
        screen.blit(self.bg, (0, 0))
        self.bullets_group.draw(screen)
        self.powerup_group.draw(screen)
        self.player_paddle.draw(screen)
        self.ai_paddle.draw(screen)
        self.pong.draw(screen)
        self.ultimate_group.draw(screen)
        
        #Make the text for the user 
        
        player_text = "Player 1" + ": " + str(self.player_paddle.score)
        player_text_image = self.my_font.render(player_text, True, BLACK)
        screen.blit(player_text_image, (screen_size[0] //4, screen_size[1] * 0.8))
        
        #Make the text for the AI
        ai_text = "Player 2" + ": " + str(self.ai_paddle.score)
        ai_text_image = self.my_font.render(ai_text, True, BLACK)
        screen.blit(ai_text_image, (3* screen_size[0] // 4, screen_size[1] * 0.8))
    
    def SwitchToScene(self, next_scene):
        self.next = next_scene
        
class TwoPlayerScreen(SceneBase):
    
    def __init__(self):
        SceneBase.__init__(self)
        self.bg = pygame.image.load("images/asianbackground.jpg")
        #self.my_font = pygame.font.SysFont("Arial", 50)
        self.my_font = pygame.font.SysFont("Arial", 50)
        
        self.p1_bullets_group = pygame.sprite.Group()
        self.p2_bullets_group = pygame.sprite.Group()
        self.p1_ultimate_group = pygame.sprite.Group()
        self.p2_ultimate_group = pygame.sprite.Group()
        self.powerup_group = pygame.sprite.Group()
        self.player_paddle = classes.PlayerPaddle(screen_size, 40, 100, SceneBase.player1_character, self.p1_bullets_group, self.p1_ultimate_group)
        self.player2_paddle = classes.Player2Paddle(screen_size, 40, 100, SceneBase.player2_character, self.p2_bullets_group, self.p2_ultimate_group)
        self.pong = classes.Pong(screen_size, 20, 20, "images/pokeball.png")
        
        self.now1 = pygame.time.get_ticks()
        
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            self.player_paddle.handle_event(event)
            self.player2_paddle.handle_event(event)
            
            for ultimate in self.p1_ultimate_group:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
                    ultimate.rect.centery -= 10
                if event.type == pygame.KEYDOWN and event.key == pygame.K_k:
                    ultimate.rect.centery += 10
                    
            for ultimate in self.p2_ultimate_group:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    ultimate.rect.centery -= 10
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    ultimate.rect.centery += 10
            
    
    def Update(self):
        self.player_paddle.update() 
        self.player2_paddle.update() 
        self.pong.update(self.player_paddle, self.player2_paddle)
        
        for bullet in self.p1_bullets_group:
            self.pong.pong_and_bullet_collision(bullet)
            
        for bullet in self.p2_bullets_group:
            self.pong.pong_and_bullet_collision(bullet)
            
        
        time_difference1 = pygame.time.get_ticks() - self.now1
        
        current_time = pygame.time.get_ticks()
        
        if time_difference1 >= 1000:
            powerup = classes.PowerUp(screen_size, 40, 40, "images/ramen.png")
            powerup.kill_time = current_time + 5000
            self.powerup_group.add(powerup)
            self.now1 = pygame.time.get_ticks()
            
        current_time = pygame.time.get_ticks()
            
            
        for powerup in self.powerup_group:
            for bullet in self.p1_bullets_group:
                bullet.update(powerup, self.player_paddle, self.player2_paddle, 3)
                
            for bullet in self.p2_bullets_group:
                bullet.update(powerup, self.player2_paddle, self.player_paddle, -3)
            if powerup.kill_time <= current_time:
                self.powerup_group.remove(powerup)
                
        for ultimate in self.p1_ultimate_group:
            ultimate.update(3)
            if ultimate.checkCollision(self.player2_paddle):
                SceneBase.is_game_over = True 
                self.SwitchToScene(GameOverScreen())
        for ultimate in self.p2_ultimate_group:
            ultimate.update(-3)
            if ultimate.checkCollision(self.player_paddle):
                SceneBase.is_game_over = True 
                self.SwitchToScene(GameOverScreen())
            
        
        
        # if someone reaches a score of 2, then exit the game 
        if self.player_paddle.score == 5: 
            SceneBase.winner = "Player 1!"
            SceneBase.is_game_over = True 
            self.SwitchToScene(GameOverScreen())
        elif self.player2_paddle.score == 5:
            SceneBase.winner = "Player 2!"
            SceneBase.is_game_over = True 
            self.SwitchToScene(GameOverScreen())
            
        
    def Render(self, screen):
        screen.blit(self.bg, (0, 0))
        self.p1_bullets_group.draw(screen)
        self.p2_bullets_group.draw(screen)
        self.player_paddle.draw(screen)
        self.player2_paddle.draw(screen)
        self.powerup_group.draw(screen)
        self.pong.draw(screen)
        self.p1_ultimate_group.draw(screen)
        self.p2_ultimate_group.draw(screen)
        
        #Make the text for the user 
        player_text = "Player 1" + ":  " + str(self.player_paddle.score)
        player_text_image = self.my_font.render(player_text, True, BLACK)
        screen.blit(player_text_image, (screen_size[0] //4, screen_size[1] * 0.8))
        
        #Make the text for the AI
        player2_text = "Player 2" + ": " + str(self.player2_paddle.score)
        player2_text_image = self.my_font.render(player2_text, True, BLACK)
        screen.blit(player2_text_image, (3* screen_size[0] // 4, screen_size[1] * 0.8))
    
    def SwitchToScene(self, next_scene):
        self.next = next_scene
            

class GameOverScreen(SceneBase):
    
    def __init__(self):
        SceneBase.__init__(self)
        self.my_font = pygame.font.SysFont("Moyko", 50)
        self.restart_button = Button("Try Again?", (600, 400), self.change_game_state)
        self.bg = pygame.image.load("images/bamboo2.jpg")
    
    
    def ProcessInput(self, events, pressed_keys):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Move to the next scene when the user pressed Enter 
                self.SwitchToScene(DifficultyScene())
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousebuttondown(self.restart_button)
               
    def Update(self):
        self.switch_to_game_screen()
        
    def Render(self, screen):
        # The game scene is just a blank blue screen 
        screen.fill(RED)
        screen.blit(self.bg, (0, 0))
        textImage = self.my_font.render("The winner is " + str(SceneBase.winner), True, (BLACK))
        screen.blit(textImage, (screen_size[0] // 2, screen_size[1] // 2))
        self.restart_button.draw()
        
    
    def switch_to_game_screen(self):
        if SceneBase.is_game_over == False:
            if SceneBase.number_of_players == 1:
                self.SwitchToScene(GameScreen())
            elif SceneBase.number_of_players == 2:
                self.SwitchToScene(TwoPlayerScreen())
                
    def change_game_state(self):
        SceneBase.is_game_over = False  
        
        
