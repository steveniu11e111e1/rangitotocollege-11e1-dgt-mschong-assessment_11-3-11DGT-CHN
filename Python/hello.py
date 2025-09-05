from tkinter import *
import random

# Set up our window
root = Tk()
root.title("Space Invaders!")
root.geometry("600x450")
root.config(bg ="black")

# create canvas
canvas = Canvas(root, width=600, height=400, bg="black", highlightthickness=0)
canvas.pack()

# Game variables
player_speed = 10
bullet_speed = -15
enemy_speed = 2
enemy_direction = 1

# list to hold bullets and enemies
bullets = []
enemies = []

# Track score
score = 0
score_label = Label(root, text=f"Score: {score}", font=("Helvetica, 14"), bg="black", fg="white")
score_label.pack()

# ceate the player
player = canvas.create_rectangle(275, 360, 325, 380, fill="blue")

# move the player
def move_player(event):
    x = 0
    # move to the left
    if event.keysym == "Left" and canvas.coords(player)[0] > 0:
        x = -player_speed
    # Move to te right
    elif event.keysym == "Right" and canvas.coords(player)[2] < 600:
        x = player_speed

# Bind the keyboard
root.bind("<Left>", move_player)
root.bind("<Right>", move_player)

# create some bullets
def fire_bullet():
    bullet = canvas.create_rectangle(canvas.coords(player)[0] + 22, 350, canvas.coords(player)[2] - 22, fill="yellow")
    bullets.append(bullet)

# fire the bullets
root.bind("<space>", lambda event: fire_bullet())

# creae rows of enemies
def create_enemies():
    for i in range(5):
        for j in range(8):
            enemy = canvas.create_rectangle(50 + j * 60, 50 + i * 30, 80 + j * 60, 80 + i * 30, fill="red")
            enemies.append(enemy)

# create our enemies
create_enemies()

# Move bullets
def move_bullets():
    for bullet in bullets:
        canvas.move(bullet, 0, bullet_speed)

        if canvas.coords(bullet)[1] < 0:
            canvas.delete(bullet)
            bullets.remove(bullet)

# move enemies
def move_enemies():
    global enemy_direction
    edge_reached = False

    for enemy in enemies:
        canvas.move(enemy, enemy_speed * enemy_direction, 0)

        x1, y1, x2, y2 = canvas.coords(enemy)

        if x2 >= 600 or x1 <=0:
            edge_reached = True

    if edge_reached:
        enemy_directio *= -1
        for enemy in enemies:
            canvas.move(enemy, 0, 20)

def check_collisions():
    global score
    for bullet in bullets:
        bullet_coords = canvas.coords(bullets)
        for enemy in enemies:
            enemy_coords = canvas.coords(enemy)

            if (bullet_coords[2] > enemy_coords[0] and bullet_coords[0] < enemy_coords[2] and 
                bullet_coords[3] > enemy_coords[1] and bullet_coords[1] < enemy_coords[3]):
                canvas.delete(bullet)
                canvas.delete(enemy)
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                score_label.config(text=f"Score: {score}")
                break

#game loop
def game_loop():
    move_bullets()
    move_enemies()
    check_collisions()

    # check if enemies reach the player (game over)
    for enemy in enemies:
        if canvas.coords(enemy)[3] >= 360:
            canvas.create_text(300, 200, text="Game Over", fill="White", font=("Helvectica", 24))
            return

    # set game speeed
    root.after(50, game_loop)

game_loop()
root.mainloop

