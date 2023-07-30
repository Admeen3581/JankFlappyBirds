"""
Jank Flappy Birb

My iteration of flappy bird.
Not 100% of the code is mine, you can find my inspiration here:
https://www.askpython.com/python/examples/flappy-bird-game-in-python
Some of the assets are my own because I didn't like the ones provided above.
All other code/assets/other details are my own work.

Author: Adam Long

License: No license, freedom of use in commerical or non-commerical contexts. I do ask
that you contact me via email (adam.jacob.long@gmail.com) if you plan on using my work
within your own project.
"""

#Imports
import random
import sys
import pygame
from pygame.locals import *
from time import sleep
from src.interactables import Clickable_Button
from src.data import Color_Data
from src.core.Scoring import *
print("Running Game")

def game_assets_init():
    """
        Description:
            Initalizes game assets. Stored inside a dictionary.

        Parameters:
            N/A

        Returns:
            N/A

        Raises:
            FileNotFoundError - Unable to find asset.

        Example:
            *start of program*
            game_assets_init()
            *...*

        """
    birb = "assets/Game Objects/yellowbird-midflap.png"
    #birb = "assets/Game Objects/giraffe.png"
    birb_up = "assets/Game Objects/yellowbird-upflap.png"
    #birb_up = "assets/Game Objects/giraffe.png"
    birb_down = "assets/Game Objects/yellowbird-downflap.png"
    #birb_down = "assets/Game Objects/giraffe.png"
    ground = "assets/Game Objects/base.png"
    ground_width = 112  # in pixels
    get_ready = "assets/UI/message.png"
    background = "assets/Game Objects/background-day.png"
    gameover = "assets/UI/gameover.png"
    pipe = "assets/Game Objects/pipe-green.png"

    global game_assets
    game_assets = {
        "numbers": ( #tuble inside a dictionary goes crazy
        pygame.image.load("assets/UI/Numbers/0.png").convert_alpha(),
        pygame.image.load("assets/UI/Numbers/1.png").convert_alpha(),
        pygame.image.load("assets/UI/Numbers/2.png").convert_alpha(),
        pygame.image.load("assets/UI/Numbers/3.png").convert_alpha(),
        pygame.image.load("assets/UI/Numbers/4.png").convert_alpha(),
        pygame.image.load("assets/UI/Numbers/5.png").convert_alpha(),
        pygame.image.load("assets/UI/Numbers/6.png").convert_alpha(),
        pygame.image.load("assets/UI/Numbers/7.png").convert_alpha(),
        pygame.image.load("assets/UI/Numbers/8.png").convert_alpha(),
        pygame.image.load("assets/UI/Numbers/9.png").convert_alpha()
        ),
        "player": {
            "mid": pygame.image.load(birb).convert_alpha(),#default birb
            "up": pygame.image.load(birb_up).convert_alpha(),
            "down": pygame.image.load(birb_down).convert_alpha()
        },
        #HS letters to mark high score... I tried to draw?
        "H": pygame.image.load("assets/UI/H2.png").convert_alpha(),
        "S": pygame.image.load("assets/UI/S2.png").convert_alpha(),
        "base": pygame.transform.scale(pygame.image.load(ground).convert_alpha(), (screen_width, ground_width)),
        "get-ready": pygame.image.load(get_ready).convert_alpha(),
        "background": pygame.transform.scale(pygame.image.load(background).convert_alpha(), (screen_width, screen_height)),
        "gameover": pygame.transform.scale(pygame.image.load(gameover).convert_alpha(), (screen_width/1.5, screen_height/6)),
        "pipe": (
        pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(), 180),
        pygame.image.load(pipe).convert_alpha()
        )
    }
    pygame.display.set_icon(game_assets["player"]["mid"])

def game_sounds_init():
    """
            Description:
                Initalizes game sound files. Stored inside a dictionary.

            Parameters:
                N/A

            Returns:
                N/A

            Raises:
                FileNotFoundError - Unable to find asset.

            Example:
                *start of program*
                game_sounds_init()
                *...*

            """
    global game_sounds

    game_sounds = {
        "die": pygame.mixer.Sound("assets/Sound Effects/die.wav"),
        "hit": pygame.mixer.Sound("assets/Sound Effects/hit.wav"),
        "point": pygame.mixer.Sound("assets/Sound Effects/point.wav"),
        "swoosh": pygame.mixer.Sound("assets/Sound Effects/swoosh.wav"),
        "wing": pygame.mixer.Sound("assets/Sound Effects/wing.wav")
    }

def run_game_init():
    """
            Description:
                Grouping method.

            Parameters:
                N/A

            Returns:
                N/A

            Raises:
                N/A

            Example:
                *start of program*
                run_game_init()
                *...*

            """
    global fps, screen_width, screen_height, screen, ground_y, fps_clock
    fps = 32
    screen_width = 510
    screen_height = 511
    screen = pygame.display.set_mode((screen_width, screen_height))
    ground_y = screen_height * 0.8

    pygame.init()
    fps_clock = pygame.time.Clock()
    pygame.display.set_caption("Jank Flappy Birb")

    game_assets_init()
    game_sounds_init()
    welcome_screen()

def exit_condition():
    """
            Description:
                Provides an exit for the game, closing it and terminating the program.
                Can be used with a sleep commmand to provide a pause to the game while
                still allowing termination.

            Parameters:
                N/A

            Returns:
                Controlled Crash - if an event condition is met such that the user requests an exit.
                Null - if an event condition is not met.

            Raises:
                N/A

            Example:
                *start of program*
                *user requests to quit*
                exit_condition()
                *...*

                OR

                *start of program*
                for x in range(10):
                   sleep(0.5) (pauses game while checking for an exit condition)
                   for event in pygame.event.get():
                      exit_condition(event)
                *...*

            Known Bug: If called before any 'score data' method is called. If a high score was
            reached, it will not be recorded. The current fix is to put the 'score data' method
            call before; however, this introduces possible lag where the user cannot exit from
            the game.
    """
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()

def welcome_screen():
    """
            Description:
                Initalizes the welcome screen (first screen) & allows for redirection
                after a 'gameover' condition is reached.

            Parameters:
                N/A

            Returns:
                N/A

            Raises:
                N/A

            Example:
                *start of program*
                welcome_screen()
                *...*

            """
    global diff #necessary to keep diff from being ref'ed before assignment.

    try:#if diff isn't defined then define it without affecting anything that MIGHT be stored in it.
        dead = diff
    except:
        diff = "easy"

    player_x = int(screen_width / 8)
    player_y = int(screen_height / 2)
    get_ready_x = int((screen_width - game_assets["get-ready"].get_width()) / 2)
    get_ready_y = int(screen_height*0.2)
    title_x = int((screen_width - game_assets["get-ready"].get_width()) / 2)
    title_y = int(screen_height*0.04)
    base_x = 0

    screen.blit(game_assets["background"], (0, 0))
    screen.blit(game_assets["get-ready"], (get_ready_x, get_ready_y))
    screen.blit(game_assets["player"]["mid"], (player_x, player_y))
    screen.blit(game_assets["base"], (base_x, ground_y))

    display_digits(high_score_data_read(), 0.88, True)

    button_list = define_difficulty_buttons()

    pygame.display.update()
    fps_clock.tick(fps)

    while True:
        for event in pygame.event.get():
            for button in button_list:
                if button.check_button(event):
                    for triggered in button_list:
                        if str(triggered.get_text()) == diff:
                            triggered.build_button(screen, Color_Data.WHITE)
                            break
                    button.build_button(screen, Color_Data.LIGHT_GRAY)
                    pygame.display.update()
                    diff = str(button.get_text())
                else:
                    continue
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif (event.type == KEYDOWN and event.key == K_SPACE):
                main_game(diff.lower())

def resolve_ending_scenario(player_x, player_y, difficulty):
    """
             Description:
                 Resolves the end of a game by displaying the necessary assets and
                 returning user to the welcome screen. Designed for conciseness.

             Parameters:
                 player_x - x pixel coordinate of the user.
                 player_y - y pixel coordinate of the user.
                 difficulty - The level's difficulty level when played. String.

             Returns:
                 True - if player collision is detected.
                 False - if player collision is not detected.

             Raises:
                 N/A

             Example:
                 *start of program*
                 if isCollide():
                    resolve_ending_scenario()
                 *...*
             """
    screen.blit(game_assets["player"]["mid"], (player_x, player_y))
    game_sounds["hit"].play()
    screen.blit(game_assets["gameover"], (90, screen_height / 4))  # hard-coded numbers
    pygame.display.update()
    for x in range(30):
        sleep(0.1)  # total of 3 seconds to react
        exit_condition()
    if check_high_score(game_score, difficulty):
        high_score_data_write(game_score, difficulty)
    welcome_screen()

def isCollide(player_x, player_y, upperPipes, lowerPipes, difficulty):
    """
            Description:
                Checks for player collision of objects and/or surfaces.

            Parameters:
                player_x - x pixel coordinate of the user.
                player_y - y pixel coordinate of the user.
                upperPipes - List containing information of the downward facing pipe objects.
                lowerPipes - List containing information of the upward facing pipe objects.
                difficulty - The level's difficulty level when played. String.

            Returns:
                True - if player collision is detected.
                False - if player collision is not detected.

            Raises:
                N/A

            Example:
                *start of program*
                *running game*
                if isCollide(): #to check for collision
                *show end condition screen*

            """
    if player_y > ground_y - 25 or player_y < 0:
        resolve_ending_scenario(player_x, player_y, difficulty)
        return True

    for pipe in upperPipes:
        pipeHeight = game_assets["pipe"][0].get_height()
        if (player_y < pipeHeight + pipe["y"]) and (
                abs(player_x - pipe["x"]) < game_assets["pipe"][0].get_width() - 15):
            resolve_ending_scenario(player_x, player_y, difficulty)
            return True

    for pipe in lowerPipes:
        if (player_y + game_assets["player"]["mid"].get_height() > pipe["y"]) and (
                abs(player_x - pipe["x"]) < game_assets["pipe"][0].get_width() - 15):
            resolve_ending_scenario(player_x, player_y, difficulty)
            return True

    return False

def display_digits(presented_num, height_factor, hs):
    """
                 Description:
                     Displays a digit count on screen given an integer.

                 Parameters:
                     presented_num - Integer to be displayed.
                     height_factor - Double ranging from 0 to 1. 0 is the top of the display and
                     1 is the bottom of the display. Will require some fiddling.
                     hs - Boolean determining placement of HS letters.

                 Returns:
                     N/A

                 Raises:
                     FileNotFoundError - Unable to find digit assets.

                 Example:
                     Self-explanatory.
                 """
    #separates presented_num into a list containing one integer per index
    individual_digits = [int(x) for x in list(str(presented_num))]

    # calculates pixel width of the digit count
    pixel_width = 0
    for digit in individual_digits:
        pixel_width += game_assets["numbers"][digit].get_width()

    #accounts for HS letters if needed.
    if hs:
        pixel_width += game_assets["H"].get_width()
        pixel_width += game_assets["S"].get_width()
        pixel_width += 25

    digit_x_offset = (screen_width - pixel_width) / 2

    #places HS letters if needed.
    if hs:
        screen.blit(game_assets["H"], (digit_x_offset, screen_height * height_factor))
        digit_x_offset += game_assets["H"].get_width()
        screen.blit(game_assets["S"], (digit_x_offset, screen_height * height_factor))
        digit_x_offset += game_assets["H"].get_width()
        digit_x_offset += 25

    # places digit assets on screen
    for digit in individual_digits:
        screen.blit(game_assets["numbers"][digit], (digit_x_offset, screen_height * height_factor))
        digit_x_offset += game_assets["numbers"][digit].get_width()
    pygame.display.update()

def get_random_pipe(difficulty):
    """
            Description:
                Creates a pipe object with a top & bottom. The gap between pipes is randomized.

            Parameters:
                difficulty - A string containing the difficultly level for the game. This
                is later converted to change the gap between the pipes.

            Returns:
                A pipe object.

            Raises:
                N/A

            Example:
                *start of program*
                new_pipe_object = get_random_pipe()
                *use random pipe*
                *...*

            """
    pipeHeight = game_assets["pipe"][0].get_height()

    pipe_gap_factor = 0
    match difficulty:
        case "easy":
            pipe_gap_factor = 2.5
        case "medium":
            pipe_gap_factor = 4
        case "hard":
            pipe_gap_factor = 5.75
        case "expert":
            pipe_gap_factor = 7.2

    offset_between_pipes = screen_height / pipe_gap_factor  # 7 to #2.5 (4 is default)

    y2 = offset_between_pipes + random.randrange(0, int(screen_height - game_assets["base"].get_height() - 1.2 * offset_between_pipes))
    y1 = pipeHeight - y2 + offset_between_pipes
    pipeX = screen_width + 10
    pipe = [
        {"x": pipeX, "y": -y1},
        {"x": pipeX, "y": y2}
    ]
    return pipe

def define_difficulty_buttons():
    """
    define_difficulty_buttons - Initializes buttons for the welcome screen
    :return: List. A list of buttons with the difficulty levels attached to them.
    """
    difficulty_list = ["Easy", "Medium", "Hard", "Expert"]
    button_list = [0,0,0,0]
    for x in range(4):
        button_list[x] = Clickable_Button.Clickable_Button(difficulty_list[x], 25+(x*120), 25, 100, 40)
        button_list[x].build_button(screen, Color_Data.WHITE)
    return button_list

def main_game(difficulty):
    """
            Description:
                Holds primary game running instructions.

            Parameters:
                difficulty - A string containing the difficulty level for the game.

            Returns:
                N/A

            Raises:
                N/A

            Example:
                *start of program*
                *player starts game*
                main_game()
                *...*

            """
    global game_score
    game_score = 0
    player_x = int(screen_width / 8)
    player_y = int(screen_height / 2)
    base_x = 0

    newPipe1 = get_random_pipe(difficulty)
    newPipe2 = get_random_pipe(difficulty)

    upperPipes = [
        {"x": screen_width + 100, "y": newPipe1[0]["y"]},
        {"x": screen_width + 100 + (screen_width / 2), "y": newPipe2[0]["y"]}
    ]
    lowerPipes = [
        {"x": screen_width + 100, "y": newPipe1[1]["y"]},
        {"x": screen_width + 100 + (screen_width / 2), "y": newPipe2[1]["y"]}
    ]

    pipeVelX = -4

    #negative go up, positive go down. It do be backwards.
    playerVelY = -6
    playerMaxVelY = 10
    playerMinVelY = -10
    playerAccY = 1

    playerFlapVel = -8
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if (event.type == KEYDOWN and event.key == K_SPACE) or (event.type == MOUSEBUTTONDOWN):
                if player_y > 0:
                    screen.blit(game_assets["player"]["up"], (player_x, player_y))
                    pygame.display.update()
                    playerVelY = playerFlapVel
                    playerFlapped = True
                    game_sounds["wing"].play()

        if isCollide(player_x, player_y, upperPipes, lowerPipes, difficulty):
            return

        playerMidPos = player_x + game_assets["player"]["mid"].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe["x"] + game_assets["pipe"][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                game_score += 1
                game_sounds["point"].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False

        playerHeight = game_assets["player"]["mid"].get_height()
        player_y = player_y + min(playerVelY, ground_y - player_y - playerHeight)

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe["x"] += pipeVelX
            lowerPipe["x"] += pipeVelX

        if 0 < upperPipes[0]["x"] < 5:
            newPipe = get_random_pipe(difficulty)
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        if upperPipes[0]["x"] < -game_assets["pipe"][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        screen.blit(game_assets["background"], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            screen.blit(game_assets["pipe"][0], (upperPipe['x'], upperPipe['y']))
            screen.blit(game_assets["pipe"][1], (lowerPipe['x'], lowerPipe['y']))
        screen.blit(game_assets["base"], (base_x, ground_y))

        if playerVelY < -1:
            screen.blit(game_assets["player"]["up"], (player_x, player_y))
        elif playerVelY > 1:
            screen.blit(game_assets["player"]["down"], (player_x, player_y))
        else:
            screen.blit(game_assets["player"]["mid"], (player_x, player_y))

        display_digits(game_score, 0.88, False)

        fps_clock.tick(fps)

#Main runner
run_game_init()
#goes into method-to-method recursion.