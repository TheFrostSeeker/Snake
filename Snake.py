# Imports
import turtle
import time
from random import randrange as rdr
from tkinter import *

global delay
screen_width = 600
screen_height = 600
half_screen_width = int((screen_width / 2) - 10)
half_screen_height = int((screen_height /2) -10)

# Environnement
window = turtle.Screen()
window.title("Snake en python")
window.bgcolor("dark green")
window.setup(width=screen_width, height=screen_height)
window.tracer(0)
window.cv._rootwindow.resizable(False, False) # Disable window scaling

# Difficulty
main_delay = 0.2
delay = 0.2

# Scores
score = 0
high_score = 0

# Snake head
snake = turtle.Turtle()
snake.speed(0)
snake.shape("square")
snake.color("black")
snake.penup()
snake.goto(-10, -10)
snake.direction = "stop"

# Food
food = turtle.Turtle()
food.speed(0)
food.shape("square")
food.color("red")
food.penup()
food.goto(rdr(-half_screen_width, half_screen_width, 20), rdr(-half_screen_height, half_screen_height, 20))

segments = []

# Scoreboard
scoreboard = turtle.Turtle()
scoreboard.speed(0)
scoreboard.color("white")
scoreboard.penup()
scoreboard.hideturtle()
scoreboard.goto(0, half_screen_width -30)
scoreboard.write("Score: 0  High score: 0", align="center", font=("ds-digital", 24, "normal"))

# Fonctions

def easy():
    global main_delay, delay
    main_delay = 0.2
    delay = main_delay
    difficulty.destroy()

def medium():
    global main_delay, delay
    main_delay = 0.1
    delay = main_delay
    difficulty.destroy()

def hard():
    global main_delay, delay
    main_delay = 0.05
    delay = main_delay
    difficulty.destroy()

def go_up():
    if snake.direction != "down":
        snake.direction = "up"

def go_down():
    if snake.direction != "up":
        snake.direction = "down"

def go_left():
    if snake.direction != "right":
        snake.direction = "left"

def go_right():
    if snake.direction != "left":
        snake.direction = "right"

def move():
    if snake.direction == "up":
        y = snake.ycor()
        snake.sety(y + 20)
    if snake.direction == "down":
        y = snake.ycor()
        snake.sety(y - 20)
    if snake.direction == "left":
        x = snake.xcor()
        snake.setx(x - 20)
    if snake.direction == "right":
        x = snake.xcor()
        snake.setx(x + 20)

# Keyboard binding
window.listen()
window.onkeypress(go_up, "z")
window.onkeypress(go_down, "s")
window.onkeypress(go_left, "q")
window.onkeypress(go_right, "d")

####################
#  Main game loop  #
####################
if __name__ == '__main__':

    # Difficulty window
    difficulty = Tk()
    difficulty.title("Choix de la difficultée")

    # Difficulty selection
        # Button creation
    easy = Button(difficulty, text="EASY", padx=50, pady=50, command=easy, fg="black", bg="green")
    medium = Button(difficulty, text="MEDIUM", padx=45, pady=50, command=medium, fg="black", bg="yellow")
    hard = Button(difficulty, text="HARD", padx=50, pady=50, command=hard, fg="black", bg="red")
        # Set on a grid
    easy.grid(row=0, column=0)
    medium.grid(row=0, column=1)
    hard.grid(row=0, column=2)

    width = 420
    height = 123
    weight_screen = difficulty.winfo_screenwidth()
    height_screen = difficulty.winfo_screenheight()
    x = (weight_screen / 2) - (width / 2)
    y = (height_screen / 2) - (height / 2)
    difficulty.geometry('%dx%d+%d+%d' % (width, height, x, y))

    # Game
    while True:
        window.update()
        move()

        # Collision with border
        if snake.xcor() > half_screen_width or snake.xcor() < -half_screen_width or snake.ycor() > half_screen_height or snake.ycor() < -half_screen_height:
            time.sleep(1)  # Add delay
            snake.goto(-10, -10)
            snake.direction = "stop"

            # Hide segments
            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()

            # Move food randomly
            food.goto(rdr(-half_screen_width, half_screen_width, 20), rdr(-half_screen_height, half_screen_height, 20))

            # Reset score
            score = 0
            scoreboard.clear()
            scoreboard.write("Score: {}  High score: {}".format(score, high_score), align="center", font=("ds-digital", 24, "normal"))

            # Reset delay
            delay = main_delay

        # Collision with body
        for segment in segments:
            if segment.distance(snake) < 20:
                time.sleep(1)
                snake.goto(-10, -10)
                snake.direction = "stop"

                # Hide segments
                for segment in segments:
                    segment.goto(1000, 1000)
                segments.clear()

                # Move food randomly
                food.goto(rdr(-half_screen_width, half_screen_width, 20), rdr(-half_screen_height, half_screen_height, 20))

                # Reset score
                score = 0
                scoreboard.clear()
                scoreboard.write("Score: {}  High score: {}".format(score, high_score), align="center", font=("ds-digital", 24, "normal"))

                # Reset delay
                delay = main_delay

        # Food eating
        if snake.distance(food) < 20:
            # Move food randomly
            food.goto(rdr(-half_screen_width, half_screen_width, 20), rdr(-half_screen_height, half_screen_height, 20))

            # Add new segment
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("black")
            new_segment.penup()
            segments.append(new_segment)

            # Shorten delay
            delay -= 0.001

            # Increase score
            score += 1
            if score > high_score:
                high_score = score
            scoreboard.clear()
            scoreboard.write("Score: {}  High score: {}".format(score, high_score), align="center", font=("ds-digital", 24, "normal"))

        # Segments reverse order move
        for i in range(len(segments) - 1, 0, -1):
            x = segments[i - 1].xcor()
            y = segments[i - 1].ycor()
            segments[i].goto(x, y)

        if len(segments) > 0:
            x = snake.xcor()
            y = snake.ycor()
            segments[0].goto(x, y)

        time.sleep(delay)