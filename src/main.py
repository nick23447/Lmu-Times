"""
Author: Nicholas Laus
Collaborators: Jaden Path, Nikita Smolyanoy
Created: 4/30/24
Updated: 2/1/25
Desctiption: Wordle Game

"""
import pygame 
import pygame.gfxdraw 
import os
from wordgenerator import get_random_word


# pygame setup
pygame.init()
screen = pygame.display.set_mode((620, 620))
clock = pygame.time.Clock()
pygame.display.set_caption('Wordle')
pygame.font.init()


# load and resize images
def load_img(name, x, y, resize = True):
    ## Add Comment
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) 
    path = os.path.join(base_path, "images", name)  
    image = pygame.image.load(path)
    if not resize:
        return image
    icon = pygame.transform.smoothscale(image, (x, y))
    return icon
    
# Condense?
start_icon = load_img('start.png', 100,50)
help_icon = load_img('help.png', 100,50)
start_highlight = load_img('start_highlighted.png', 100,50)
help_highlight = load_img('help_highlighted.png', 100,50)
play_again = load_img('play_again.png', 100,50)
play_again_highlight = load_img('play_again_highlighted.png', 100,50)
back = load_img('back.png', 100,50)
back_highlight = load_img('back_highlighted.png', 100,50)
cozy_background = load_img('cozy.jpg', 620,620)
instructions = load_img('instructions.png', 520,320)
boxes_icon = load_img('00 copy.png',0,0,resize=False)



# Input text to blit it at your desired location
def text(word, text_color,font_type,font_size,x,y):
    ## Add Comment
    font = pygame.font.Font(font_type, font_size)
    text = font.render(word, True, text_color)
    textRect = text.get_rect()
    textRect.center = (x,y)
    screen.blit(text, textRect)
    

# lights up play & help button when mouse hovers over & opens new display if mouse presses on either button (Code inspired from Lab 15)
def button(type,x,y,w,h,action=None):
    ## Add Comment
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Draw active (bright) button color if mouse hovers over it.
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        if type == 'start':
            screen.blit(start_highlight, (x, y))
        elif type == 'help':
            screen.blit(help_highlight, (x, y))
        elif type == 'play again':
            screen.blit(play_again_highlight, (x, y))
        else: 
            screen.blit(back_highlight, (x, y))

    # The user clicks the button
        if (click[0] == 1) and (action is not None):
            action()

    # Default button view
    else:
        if type == "start":
         screen.blit(start_icon, (x, y))
        elif type == 'help':
            screen.blit(help_icon, (x, y))
        elif type == 'play again':
            screen.blit(play_again, (x, y))
        else:
            screen.blit(back, (x, y))
    

# title interface
def game_intro():
     ## Add Comment

    # fill screen, set title, and set play and help button
    screen.fill('#5F6A6A')
    text('Wordle','#212F3C','freesansbold.ttf', 100, 305, 200)
    
    running = True

    while running:

        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # if user presses play or help, takes them to corresponding screen
        button('start', 150, 390, 100, 50, game_loop)
        button('help', 360, 390, 100, 50, help_menu)
        
        
        pygame.display.update()
        clock.tick(60)  # limits FPS to 60
    
     
# game interface
def game_loop():
     ## Add Comment

    # fill screen and set title
    screen.fill('#AAB7B8')
    screen.blit(cozy_background, (0, 0))
    text('Wordle','#B2BABB','freesansbold.ttf', 70, 308, 50)

    # load boxes
    screen.blit(boxes_icon, (140,150))
    
    # Initialize Box class
    box = Box()
    
    running = True

    while running:

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            

            # if user presses back, takes them to corresponding screen
            button('back', 20, 550, 100, 50, game_intro)

            # main loop; updates, deletes, colors boxes, and checks if row is full when user presses corresponding keys
            if event.type == pygame.KEYDOWN:
                box.delete_box(event.key)
                if box.count > 4:
                    box.colored_boxes(event.key)
                    box.row_full(event.key)
                    box.finished_game()
                    continue
                box.update_box(event.key)
               
                
        
        pygame.display.update()
        clock.tick(60)  # limits FPS to 60

# if user guess correctly
def win_screen():
     ## Add Comment

    #fill screen and set title 
    screen.fill('#5F6A6A')
    text('You Won!','#212F3C','freesansbold.ttf', 100, 300, 170)

    running = True

    while running:

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # if user presses play again or back, takes them to corresponding screen
        button('play again', 150, 390, 100, 50, game_loop)
        button('back', 360, 390, 100, 50, game_intro)

        pygame.display.update()
        clock.tick(60)  # limits FPS to 60


# if user runs out of guesses
def lose_screen():
     ## Add Comment

    #fill screen and set title 
    screen.fill('#5F6A6A')
    text('You Lost :(','#212F3C','freesansbold.ttf', 100, 300, 150)
    text(f'The word was: {word}','#154360','freesansbold.ttf', 40, 300, 300)

    running = True

    while running:

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # if user presses play again or back, takes them to corresponding screen
        button('play again', 150, 450, 100, 50, game_loop)
        button('back', 360, 450, 100, 50, game_intro)

        pygame.display.update()
        clock.tick(60)  # limits FPS to 60



# if user presses help
def help_menu():
     ## Add Comment

    # fill screen and set title  
    screen.fill('#5F6A6A')
    text('How to Play','#212F3C','freesansbold.ttf', 80, 305, 100)
    screen.blit(instructions, (50, 200))

    running = True

    while running:

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # if user presses start or back, takes them to corresponding screen
        button('start', 150, 550, 100, 50, game_loop)
        button('back', 360, 550, 100, 50, game_intro)
        

        pygame.display.update()
        clock.tick(60)  # limits FPS to 60



# Allows user to guess the word
class Box():
     ## Add Comment

    def __init__(self):
         ## Add Comment
        self.abc_keys = [pygame.K_a,pygame.K_b,pygame.K_c,pygame.K_d,pygame.K_e,pygame.K_f,pygame.K_g,pygame.K_h,pygame.K_i,pygame.K_j,pygame.K_k,pygame.K_l,pygame.K_m,pygame.K_n,pygame.K_o,pygame.K_p,pygame.K_q,pygame.K_r,pygame.K_s,pygame.K_t,pygame.K_u,pygame.K_v,pygame.K_w,pygame.K_x,pygame.K_y,pygame.K_z]
        self.abc_dict = {'97':'A','98':'B','99':'C','100':'D','101':'E','102':'F','103':'G','104':'H','105':'I','106':'J','107':'K','108':'L','109':'M','110':'N','111':'O','112':'P','113':'Q','114':'R','115':'S','116':'T','117':'U','118':'V','119':'W','120':'X','121':'Y','122':'Z'}

        # Letter Font
        self.box_font = pygame.font.Font('freesansbold.ttf', 50)

        # The user's guess and the actual word pulled from random generator
        self.random_word = get_random_word().upper()
        self.word = ''

        # Coordinates for the first box in first row
        self.x = 177
        self.y = 187

        # Count for boxes filled and for rows completed
        self.count = 0
        self.row_count = 0

        # Empty list in which a letters coordinates are later added
        self.word_x = []
        self.word_y = []
       

    def update_box(self, event_key):
         ## Add Comment

        # if user presses a letter key, blits letter onto box, adds to x coordinate each time to acccount for the 5 boxes
        if event_key in self.abc_keys:
            
            # appends letter to self.word and blits letter that user pressed on the corresponding box
            self.word += (f'{self.abc_dict[str(event_key)]}')
            box_text = self.box_font.render(f'{self.abc_dict[str(event_key)]}', True, 'black')
            tRect = box_text.get_rect()
            tRect.center = (self.x,self.y)
            screen.blit(box_text, tRect)

            # Adds to x axis postion so next letter goes into new box
            self.x += 66

            #Appends the current letter position to the empty lists
            self.word_x.append(self.x)
            self.word_y.append(self.y)

            # add to count of how many boxes filled
            self.count += 1


    def colored_boxes(self, event_key):
         ## Add Comment

        # if user presses enter and row is filled, changes color of boxes depending on if letter is correct/ in right positon/ incorrect
        # iterates through self.word to see if letter in the actual word and uses letter coordinates to correctly re-blit letters onto colored boxes
        if event_key == pygame.K_RETURN:
            for index, guessed_letter in enumerate(self.word):
                if index < len(self.random_word):
                    correct_letter = self.random_word[index]
                    if guessed_letter == correct_letter:
                        pygame.draw.rect(screen, '#1E8449', [self.word_x[index] - 90, self.word_y[index] - 27, 50, 50], 0)
                        box_text = self.box_font.render(f'{guessed_letter}', True, 'black')
                        tRect = box_text.get_rect()
                        tRect.center = (self.word_x[index]- 66,self.word_y[index])
                        screen.blit(box_text, tRect)

                    elif guessed_letter in self.random_word:
                        pygame.draw.rect(screen, '#D4AC0D', [self.word_x[index] - 90, self.word_y[index] - 27, 50, 50], 0)
                        box_text = self.box_font.render(f'{guessed_letter}', True, 'black')
                        tRect = box_text.get_rect()
                        tRect.center = (self.word_x[index] - 66,self.word_y[index])
                        screen.blit(box_text, tRect)
                    else:
                        pygame.draw.rect(screen, '#616A6B', [self.word_x[index] - 90, self.word_y[index] - 27, 50, 50], 0)
                        box_text = self.box_font.render(f'{guessed_letter}', True, 'black')
                        tRect = box_text.get_rect()
                        tRect.center = (self.word_x[index] - 66,self.word_y[index])
                        screen.blit(box_text, tRect)



    def delete_box(self, event_key):
         ## Add Comment


        # if user presses delete, blits white rect to "erase" current letter
        if event_key == pygame.K_BACKSPACE:
             # makes sure you can't delete if no letters in row
            if self.x <= 177:
                pass
            
            else:
                # makes sure to update letter in user's guess
                store = self.word[:-1]
                self.word = ''
                self.word += store
                self.word_x = self.word_x[:-1]
                self.word_y = self.word_y[:-1]

                # draw white rect, subtract from x coordinate and count to account for the user undoing current letter
                pygame.draw.rect(screen,'white', [self.x - 90,self.y - 25,50,50],0)
                self.x -= 66
                self.count -= 1



    def row_full(self, event_key):
         ## Add Comment

        # if user presses return, checks if their guess is correct
        if event_key == pygame.K_RETURN:
            # if correct, move to win screen
            if self.random_word == self.word:
                win_screen()

            # else, reset user guess, letter coordinates, box filled count, and adds to row count
            else:
                self.count = 0

                #used later in lose screen to tell user what the correct word was
                global word
                word = self.random_word

                # reset user guess, reset letter x coordinate, add to letter y coordinate, and add to row filled count
                self.word = ''
                self.x = 177
                self.y += 67
                self.row_count += 1
                self.word_x = []
                self.word_y = []

        
    def finished_game(self):
        ## Add Comment

        # if user fills all rows without guessing correctly, moves to lose screen
        if self.row_count > 5:
            lose_screen()

   
    def __str__(self):
        return (f'The word is {self.random_word}')
   





# main code
game_intro()

