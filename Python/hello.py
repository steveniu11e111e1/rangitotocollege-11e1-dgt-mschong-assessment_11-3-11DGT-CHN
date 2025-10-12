from tkinter import *
import tkinter as tk
from tkinter import ttk
import random

class Game1:
    def __init__(self, window=None):
        if window is None:
            self.extrawindow = Tk()
        else:
            self.extrawindow = window
           
        self.extrawindow.title("Space Invaders!")
        self.extrawindow.geometry("600x450")
        self.extrawindow.config(bg="black")

        # Game variables
        self.player_speed = 10
        self.bullet_speed = -15
        self.enemy_speed = 2
        self.enemy_direction = 1
        self.game_started = False

        # list to hold bullets and enemies
        self.bullets = []
        self.enemies = []

        # Track score
        self.score = 0

        # create player canvas
        self.canvas = Canvas(self.extrawindow, width=600, height=400, bg="black", highlightthickness=0)
        self.canvas.pack()

        # Score label
        self.score_label = Label(self.extrawindow, text=f"Score: {self.score}", font=("Helvetica", 14), bg="black", fg="white")
        self.score_label.pack()
        
        # Create start screen
        self.create_start_screen()

        # Bind the keyboard
        self.extrawindow.bind("<space>", lambda event: self.start_game())

    def create_start_screen(self):
        # Clear canvas of game
        self.canvas.delete("all")

        #title 
        self.canvas.create_text(300,150, text="space invaders", font="Helvetica", fill="white")
        # start button/intructions 
        self.canvas.create_text(300, 280, text="Press Space to Start", foot="Helvetica", fill="yellow")

    def start_game(self, event=None):
        if not self.game_started:
            self.game_started = True
            # Clear canvas of start screen
            self.canvas.delete("all")

            # create the player
            self.player = self.canvas.create_rectangle(275, 360, 325, 380, fill="blue")

            # Bind the keyboard
            self.extrawindow.bind("<Left>", self.move_player)
            self.extrawindow.bind("<Right>", self.move_player)
            self.extrawindow.bind("<space>", lambda event: self.fire_bullet())

            # create enemies
            self.create_enemies()

            # Start game loop
            self.game_loop()

    def move_player(self, event):
        # game intitaliation
        if not self.game_started:
            return
        x = 0
        # move to the left
        if event.keysym == "Left" and self.canvas.coords(self.player)[0] > 0:
            x = -self.player_speed
        # Move to the right
        elif event.keysym == "Right" and self.canvas.coords(self.player)[2] < 600:
            x = self.player_speed
        self.canvas.move(self.player, x, 0)

    # create some bullets
    def fire_bullet(self):
        if not self.game_started:
            return
        bullet = self.canvas.create_rectangle(
            self.canvas.coords(self.player)[0] + 22,
            350,
            self.canvas.coords(self.player)[2] - 22,
            340,
            fill="yellow"
        )
        self.bullets.append(bullet)

    # create rows of enemies
    def create_enemies(self):
        for i in range(5):
            for j in range(8):
                enemy = self.canvas.create_rectangle(50 + j * 60, 50 + i * 30, 80 + j * 60, 80 + i * 30, fill="red")
                self.enemies.append(enemy)

    # Move bullets
    def move_bullets(self):
        for bullet in self.bullets[:]:  # Use slice copy to avoid modification during iteration
            self.canvas.move(bullet, 0, self.bullet_speed)

            if self.canvas.coords(bullet)[1] < 0:
                self.canvas.delete(bullet)
                self.bullets.remove(bullet)

    # move enemies
    def move_enemies(self):
        edge_reached = False

        for enemy in self.enemies:
            self.canvas.move(enemy, self.enemy_speed * self.enemy_direction, 0)

            x1, y1, x2, y2 = self.canvas.coords(enemy)

            if x2 >= 600 or x1 <= 0:
                edge_reached = True

        if edge_reached:
            self.enemy_direction *= -1
            for enemy in self.enemies:
                self.canvas.move(enemy, 0, 20)

    def check_collisions(self):
        for bullet in self.bullets[:]:  # Use slice copy to avoid modification during iteration
            bullet_coords = self.canvas.coords(bullet)
            for enemy in self.enemies[:]:  # Use slice copy to avoid modification during iteration
                enemy_coords = self.canvas.coords(enemy)

                if (bullet_coords[2] > enemy_coords[0] and bullet_coords[0] < enemy_coords[2] and
                    bullet_coords[3] > enemy_coords[1] and bullet_coords[1] < enemy_coords[3]):
                    self.canvas.delete(bullet)
                    self.canvas.delete(enemy)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                    self.score += 10
                    self.score_label.config(text=f"Score: {self.score}")
                    break

    # game loop
    def game_loop(self):
        if not self.game_started:
            return
        
        self.move_bullets()
        self.move_enemies()
        self.check_collisions()

        # check if enemies reach the player (game over)
        for enemy in self.enemies:
            if self.canvas.coords(enemy)[3] >= 360:
                self.canvas.create_text(300, 200, text="Game Over", fill="White", font=("Helvetica", 24))
                return

        # check if all enemies are destroyed (win condition)
        if not self.enemies:
            self.canvas.create_text(300, 200, text="You Win!", fill="White", font=("Helvetica", 24))
            self.game_started = False
            return

        # set game speed
        self.extrawindow.after(50, self.game_loop)
def restart_game(self, event=None):

    # Reset game state 
    self.game_stared = False
    self.bullets.clear = []
    self.enemies.clear = []
    self.score = 0
    self.score_label.config(text=f"Score: {self.score}")

    # clear canvas and show start screen
    self.canvas.delete("all")
    self.create_start_screen()

    # Rebind space to start game
    self.extrawindow.bind("<space>", lambda event: self.start_game())
    #Unbidn restart key
    self.extrawindow.unbind("r")


class Game2:
    def __init__(self, window=None):
        if window is None:
            self.window = Tk()
        else:
            self.window = window
            
        # Game dimensions
        self.WIDTH, self.HEIGHT, self.SPEED, self.SPACE_SIZE, self.BODY_SIZE= 500, 500, 200, 20, 2
        self.SNAKE = "#00FF00"
        self.FOOD = "#FFFFFF"
        self.BACKGROUND = "#000000"
        
        self.score = 0
        self.direction = 'down'
        
        self.setup_window()
        self.create_widgets()
        self.start_game()
        
    def setup_window(self):
        self.window.title("Snake Game")
        self.window.bind('<Left>', lambda event: self.change_direction('left'))
        self.window.bind('<Right>', lambda event: self.change_direction('right'))
        self.window.bind('<Up>', lambda event: self.change_direction('up'))
        self.window.bind('<Down>', lambda event: self.change_direction('down'))
        
    def create_widgets(self):
        # Score label
        self.label = Label(self.window, text=f"Points: {self.score}", font=('consolas', 20))
        self.label.pack()

        # Game canvas
        self.canvas = Canvas(self.window, bg=self.BACKGROUND, height=self.HEIGHT, width=self.WIDTH)
        self.canvas.pack()

        # Center window on screen
        self.window.update()
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = int((screen_width/2) - (window_width/2))
        y = int((screen_height/2) - (window_height/2))
        self.window.geometry(f"{self.WIDTH}x{self.HEIGHT+50}+{x}+{y}")
        
    def start_game(self):
        self.snake = Snake(self.canvas, self.BODY_SIZE, self.SPACE_SIZE, self.SNAKE)
        self.food = Food(self.canvas, self.WIDTH, self.HEIGHT, self.SPACE_SIZE, self.FOOD)
        self.next_turn()
        
    def change_direction(self, new_direction):
        if new_direction == 'left':
            if self.direction != 'right':
                self.direction = new_direction
        elif new_direction == 'right':
            if self.direction != 'left':
                self.direction = new_direction
        elif new_direction == 'up':
            if self.direction != 'down':
                self.direction = new_direction
        elif new_direction == 'down':
            if self.direction != 'up':
                self.direction = new_direction
                
    def next_turn(self):
        x, y = self.snake.coordinates[0]

        if self.direction == "up":
            y -= self.SPACE_SIZE
        elif self.direction == "down":
            y += self.SPACE_SIZE
        elif self.direction == "left":
            x -= self.SPACE_SIZE
        elif self.direction == "right":
            x += self.SPACE_SIZE

        self.snake.coordinates.insert(0, (x, y))

        square = self.canvas.create_rectangle(
            x, y, x + self.SPACE_SIZE,
            y + self.SPACE_SIZE, fill=self.SNAKE)

        self.snake.squares.insert(0, square)

        if x == self.food.coordinates[0] and y == self.food.coordinates[1]:
            self.score += 1
            self.label.config(text=f"Points: {self.score}")
            self.canvas.delete("food")
            self.food = Food(self.canvas, self.WIDTH, self.HEIGHT, self.SPACE_SIZE, self.FOOD)
        else:
            del self.snake.coordinates[-1]
            self.canvas.delete(self.snake.squares[-1])
            del self.snake.squares[-1]

        if self.check_collisions():
            self.game_over()
        else:
            self.window.after(self.SPEED, self.next_turn)
            
    def check_collisions(self):
        x, y = self.snake.coordinates[0]

        if x < 0 or x >= self.WIDTH:
            return True
        elif y < 0 or y >= self.HEIGHT:
            return True

        for body_part in self.snake.coordinates[1:]:
            if x == body_part[0] and y == body_part[1]:
                return True

        return False
        
    def game_over(self):
        self.canvas.delete(ALL)
        self.canvas.create_text(self.canvas.winfo_width()/2, 
                               self.canvas.winfo_height()/2,
                               font=('consolas', 70), 
                               text="GAME OVER", fill="red", 
                               tag="gameover")
class Game3:
    def __init__(self, window=None):
        if window is None:
            self.window = Tk()
        else:
            self.window = window
            
        self.window.title("Dinosaur Game")
        self.window.geometry("600x200")
        self.window.config(bg="white")
        




#assests of Snake Game
class Snake:
    def __init__(self, canvas, body_size, space_size, color):
        self.canvas = canvas
        self.body_size = body_size
        self.coordinates = []
        self.squares = []

        for i in range(0, body_size):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + space_size, y + space_size, 
                fill=color, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self, canvas, width, height, space_size, color):
        self.canvas = canvas
        x = random.randint(0, (width / space_size)-1) * space_size
        y = random.randint(0, (height / space_size) - 1) * space_size
        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + space_size, y +
                           space_size, fill=color, tag="food")


class GameLauncher:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("600x450")
        self.window.title('Game Launcher')
        
        self.create_widgets()
        
    def create_widgets(self):
        button1 = ttk.Button(self.window, text='Space Invaders', 
                            command=lambda: Game1(Toplevel(self.window)))
        button1.pack(expand=True)

        button2 = ttk.Button(self.window, text='Snake Game', 
                            command=lambda: Game2(Toplevel(self.window)))
        button2.pack(expand=True)

        button3 = ttk.Button(self.window, text='Dinosaur Game', 
                            command=lambda: Game3(Toplevel(self.window)))
        button3.pack(expand=True)
        
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    launcher = GameLauncher()
    launcher.run()