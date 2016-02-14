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
paddle1_pos = HEIGHT / 2
paddle2_pos = HEIGHT / 2
paddle1_vel = 0
paddle2_vel = 0

PUCK_COLOR = 'Aqua'
PUCK_OUTLINE = 'White'
paddle1_fill = 'Aqua'
paddle1_outline = 'White'
paddle2_fill = paddle1_fill
paddle2_outline = paddle1_outline

score1 = 0
score2 = 0



# initialize puck_pos and puck_vel for new bal in middle of table
# if direction is RIGHT, the puck's velocity is upper right, else upper left
def spawn_puck(direction):
    global puck_pos, puck_vel # these are vectors stored as lists
    puck_pos = [WIDTH / 2, HEIGHT / 2]
    if direction:
        # vertical velocity: random.randrange(60, 180)
        # horizontal velocity: random.randrange(120, 240)
        puck_vel = [random.randrange(3, 5), -random.randrange(3, 5)]
    else:
        puck_vel = [-random.randrange(3, 5), -random.randrange(3, 5)]



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

    # puck respawns when it touches/collides with gutters, reflects when it hits a paddle
    if puck_pos[0] <= PAD_WIDTH + PUCK_RADIUS:
        if paddle1_pos + HALF_PAD_HEIGHT > puck_pos[1] and paddle1_pos - HALF_PAD_HEIGHT < puck_pos[1]:
            puck_vel[0] = -puck_vel[0]
            puck_vel[0] = puck_vel[0] + (puck_vel[0] * .1)
            puck_vel[1] = puck_vel[1] + (puck_vel[1] * .1)
        else:
            score2 += 1
            spawn_puck(RIGHT)
    elif puck_pos[0] >= WIDTH - PAD_WIDTH - PUCK_RADIUS:
        if paddle2_pos + HALF_PAD_HEIGHT > puck_pos[1] and paddle2_pos - HALF_PAD_HEIGHT < puck_pos[1]:
            puck_vel[0] = -puck_vel[0]
            puck_vel[0] = puck_vel[0] + (puck_vel[0] * .1)
            puck_vel[1] = puck_vel[1] + (puck_vel[1] * .1)
        else:
            score1 += 1
            spawn_puck(LEFT)

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos <= HALF_PAD_HEIGHT:
        paddle1_pos = HALF_PAD_HEIGHT
    elif paddle1_pos >= HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos = HEIGHT - HALF_PAD_HEIGHT
    elif paddle2_pos <= HALF_PAD_HEIGHT:
        paddle2_pos = HALF_PAD_HEIGHT
    elif paddle2_pos >= HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel

    # draw left paddle
    canvas.draw_polygon([[0, paddle1_pos - HALF_PAD_HEIGHT], [PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], [PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], [0, paddle1_pos + HALF_PAD_HEIGHT]], 1, paddle1_outline, paddle1_fill)
    # draw right paddle
    canvas.draw_polygon([[WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], [WIDTH, paddle2_pos - HALF_PAD_HEIGHT], [WIDTH, paddle2_pos + HALF_PAD_HEIGHT], [WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT]], 1, paddle2_outline, paddle2_fill)

    # draw scores
    canvas.draw_text(str(score1), (WIDTH / 2 - 25, 25), 25, "White")
    canvas.draw_text(str(score2), (WIDTH / 2 + 13, 25), 25, "White")


def keydown(key):
    global paddle1_vel, paddle2_vel
    # left paddle up with "W", down with "S"
    if key == 87:
        paddle1_vel -= 6
    if key == 83:
        paddle1_vel += 6
    # right paddle up with "Up arrow", down with "Down arrow"
    if key == 38:
        paddle2_vel -= 6
    if key == 40:
        paddle2_vel += 6

def keyup(key):
    global paddle1_vel, paddle2_vel
    # left paddle up with "S", down with "W"
    if key == 83 or key == 87:
        paddle1_vel = 0
    # right paddle up with "Up arrow", down with "Down arrow"
    if key == 40 or key == 38:
        paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()