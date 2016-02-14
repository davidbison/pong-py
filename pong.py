# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
PUCK_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

puck_pos = [WIDTH / 2, HEIGHT / 2]
paddle1_pos = [[5,5], [7,7], [8,8], [10,10]]
paddle2_pos = []
#paddle1_vel =
#paddle2_vel =

PUCK_COLOR = 'Aqua'
PUCK_OUTLINE = 'White'
paddle_1_fill = 'Aqua'
paddle_1_outline = 'White'
paddle_2_fill = paddle_1_fill
paddle_2_outline = paddle_1_outline



# initialize puck_pos and puck_vel for new bal in middle of table
# if direction is RIGHT, the puck's velocity is upper right, else upper left
def spawn_puck(direction):
    global puck_pos, puck_vel # these are vectors stored as lists
    puck_pos = [WIDTH / 2, HEIGHT / 2]
    if direction:
        # vertical velocity: random.randrange(60, 180)
        # horizontal velocity: random.randrange(120, 240)
        puck_vel = [random.randrange(1, 5), -random.randrange(1, 5)]
    else:
        puck_vel = [-random.randrange(1, 5), -random.randrange(1, 5)]



# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints

    # randomizes direction of puck at new game
    spawn_direction = random.randrange(1, 3)
    if spawn_direction == 1:
        spawn_puck(LEFT)
    elif spawn_direction == 2:
        spawn_puck(RIGHT)



def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, puck_pos, puck_vel

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update puck
    puck_pos[0] += puck_vel[0]
    puck_pos[1] += puck_vel[1]

    # draw puck
    canvas.draw_circle(puck_pos, PUCK_RADIUS, 2, PUCK_OUTLINE, PUCK_COLOR)

    # reflect puck against top and bottom walls
    if puck_pos[1] <= PUCK_RADIUS or puck_pos[1] >= (HEIGHT - PUCK_RADIUS):
        puck_vel[1] = -puck_vel[1]

    # puck respawns when it touches/collides with gutters
    if (puck_pos[0]-PUCK_RADIUS) <= PAD_WIDTH:
        spawn_puck(LEFT)
    elif (puck_pos[0]+PUCK_RADIUS) >= (WIDTH - PAD_WIDTH):
        spawn_puck(RIGHT)

    # update paddle's vertical position, keep paddle on the screen

    # draw left paddle
    canvas.draw_polygon([[0, HEIGHT / 2 - PAD_HEIGHT / 2], [PAD_WIDTH, HEIGHT / 2 - PAD_HEIGHT / 2], [PAD_WIDTH, HEIGHT / 2 + PAD_HEIGHT / 2], [0, HEIGHT / 2 + PAD_HEIGHT / 2]], 1, paddle_1_outline, paddle_1_fill)
    # draw right paddle
    canvas.draw_polygon([[WIDTH - PAD_WIDTH, HEIGHT / 2 - PAD_HEIGHT / 2], [WIDTH, HEIGHT / 2 - PAD_HEIGHT / 2], [WIDTH, HEIGHT / 2 + PAD_HEIGHT / 2], [WIDTH - PAD_WIDTH, HEIGHT / 2 + PAD_HEIGHT / 2]], 1, paddle_2_outline, paddle_2_fill)

    # determine whether paddle and puck collide

    # draw scores



def keydown(key):
    global paddle1_vel, paddle2_vel

def keyup(key):
    global paddle1_vel, paddle2_vel


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()