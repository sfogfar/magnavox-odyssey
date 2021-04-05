# Implementation of classic arcade game Pong

# simplegui is a custom module for in browser graphics
# docs here http://www.codeskulptor.org/docs.html#tabs-Python
import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    if direction == True:
        ball_pos = [WIDTH / 2, HEIGHT / 2]
        ball_vel = [random.randrange(2, 3), random.randrange(1, 3)]
    elif direction == False:
        ball_pos = [WIDTH / 2, HEIGHT / 2]
        ball_vel = [random.randrange(2, 3) * -1, random.randrange(1, 3)]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, acc  # these are numbers
    global score1, score2  # these are ints
    
    paddle1_pos = HEIGHT / 2 - PAD_HEIGHT / 2
    paddle1_vel = 0
    paddle2_pos = HEIGHT / 2 - PAD_HEIGHT / 2
    paddle2_vel = 0
    acc = 2
    
    score1 = 0
    score2 = 0
    
    #spawn_ball(direction)
    direction = random.choice([LEFT, RIGHT])
    spawn_ball(direction)
    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos, ball_vel
 
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] -= ball_vel[1]
    
    if (ball_pos[1] - BALL_RADIUS) <= 0 or (ball_pos[1] + BALL_RADIUS) >= HEIGHT:
        ball_vel[1] *= -1
    elif (ball_pos[0] - BALL_RADIUS <= PAD_WIDTH) and (ball_pos[1] < paddle1_pos):
        spawn_ball(RIGHT)
        score2 += 1
    elif (ball_pos[0] - BALL_RADIUS <= PAD_WIDTH) and (ball_pos[1] > paddle1_pos + PAD_HEIGHT):
        spawn_ball(RIGHT)
        score2 += 1
    elif (ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH) and (ball_pos[1] < paddle2_pos):
        spawn_ball(LEFT)
        score1 += 1
    elif (ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH) and (ball_pos[1] > paddle2_pos + PAD_HEIGHT):
        spawn_ball(LEFT)
        score1 += 1
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 3, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if 0 <= paddle1_pos + paddle1_vel <= HEIGHT - PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    
    if 0 <= paddle2_pos + paddle2_vel <= HEIGHT - PAD_HEIGHT:
        paddle2_pos += paddle2_vel
    
    # draw paddles
    canvas.draw_polygon([(0, paddle1_pos), (0, paddle1_pos + PAD_HEIGHT), 
                         (PAD_WIDTH, paddle1_pos + PAD_HEIGHT), (PAD_WIDTH, paddle1_pos)], 
                        1, "White", "White")
    canvas.draw_polygon([(WIDTH, paddle2_pos), (WIDTH, paddle2_pos + PAD_HEIGHT), 
                        (WIDTH - PAD_WIDTH, paddle2_pos + PAD_HEIGHT), (WIDTH - PAD_WIDTH, paddle2_pos)], 
                        1, "White", "White")
    
    # determine whether paddle and ball collide
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        ball_vel[0] *= -1.1
    elif ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH:
        ball_vel[0] *= -1.1
        
    # draw scores
    canvas.draw_text(str(score1), [0.25 * WIDTH , 0.25 * HEIGHT], 50, "White")
    canvas.draw_text(str(score2), [0.75 * WIDTH , 0.25 * HEIGHT], 50, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel, acc
    
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= acc
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += acc
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= acc
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += acc
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("New Game", new_game)


# start frame
new_game()
frame.start()

