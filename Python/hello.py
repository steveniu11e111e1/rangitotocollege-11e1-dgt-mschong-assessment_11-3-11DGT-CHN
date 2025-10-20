from tkinter import *
import tkinter as tk
from tkinter import ttk
import random
import time
import tkinter.messagebox

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
        self.game_paused = False
        self.timeDelayVar = None

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
        self.extrawindow.bind("<space>", self.start_game)
        self.extrawindow.bind("<Escape>", self.toggle_pause)
        self.extrawindow.bind("p", self.toggle_pause)

    def create_start_screen(self):
        # Clear canvas
        self.canvas.delete("all")

        # Title
        self.canvas.create_text(300, 100, text="SPACE INVADERS", font=("Helvetica", 24, "bold"), fill="white")
        self.canvas.create_text(300, 150, text="Defend Earth from alien invasion!", font=("Helvetica", 12), fill="yellow")
        
        # Controls
        self.canvas.create_text(300, 200, text="CONTROLS:", font=("Helvetica", 14, "bold"), fill="white")
        self.canvas.create_text(300, 230, text="← → : Move Left/Right", font=("Helvetica", 12), fill="lightblue")
        self.canvas.create_text(300, 260, text="SPACE : Shoot", font=("Helvetica", 12), fill="lightblue")
        self.canvas.create_text(300, 290, text="P or ESC : Pause Game", font=("Helvetica", 12), fill="lightblue")
        
        # Start instruction
        self.canvas.create_text(300, 350, text="Press SPACE to Start", font=("Helvetica", 16, "bold"), fill="green")

    def show_pause_screen(self):
        # Create semi-transparent overlay
        self.pause_overlay = self.canvas.create_rectangle(0, 0, 600, 400, fill="black", stipple="gray50")
        self.pause_text = self.canvas.create_text(300, 200, text="GAME PAUSED", font=("Helvetica", 24, "bold"), fill="white")
        self.continue_text = self.canvas.create_text(300, 250, text="Press P or ESC to Continue", font=("Helvetica", 14), fill="yellow")

    def hide_pause_screen(self):
        if hasattr(self, 'pause_overlay'):
            self.canvas.delete(self.pause_overlay)
            self.canvas.delete(self.pause_text)
            self.canvas.delete(self.continue_text)

    def toggle_pause(self, event=None):
        if self.game_started and not self.game_over:
            self.game_paused = not self.game_paused
            if self.game_paused:
                self.show_pause_screen()
            else:
                self.hide_pause_screen()
                self.game_loop()

    def start_game(self, event=None):
        if not self.game_started:
            self.game_started = True
            self.game_paused = False
            self.game_over = False
            # clear the start screen
            self.canvas.delete("all")

            # create the player
            self.player = self.canvas.create_rectangle(275, 360, 325, 380, fill="blue")

            # Bind the keyboard
            self.extrawindow.bind("<Left>", self.move_player)
            self.extrawindow.bind("<Right>", self.move_player)
            self.extrawindow.bind("<space>", lambda event: self.fire_bullet())

            # create our enemies
            self.create_enemies()

            # Start game loop
            self.game_loop()

    def move_player(self, event):
        if self.game_paused or not self.game_started or self.game_over:
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
        if self.game_paused or not self.game_started or self.game_over:
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
        for bullet in self.bullets[:]:
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
        for bullet in self.bullets[:]:
            bullet_coords = self.canvas.coords(bullet)
            for enemy in self.enemies[:]:
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

    def game_over_screen(self):
        self.game_over = True
        self.canvas.create_rectangle(150, 150, 450, 250, fill="black", outline="white")
        self.canvas.create_text(300, 180, text="GAME OVER", fill="red", font=("Helvetica", 24, "bold"))
        self.canvas.create_text(300, 220, text=f"Final Score: {self.score}", fill="white", font=("Helvetica", 14))
        self.canvas.create_text(300, 350, text="Press R to Restart or ESC to Quit", fill="yellow", font=("Helvetica", 12))
        self.extrawindow.bind("r", self.restart_game)

    def win_screen(self):
        self.game_over = True
        self.canvas.create_rectangle(150, 150, 450, 250, fill="black", outline="green")
        self.canvas.create_text(300, 180, text="YOU WIN!", fill="green", font=("Helvetica", 24, "bold"))
        self.canvas.create_text(300, 220, text=f"Final Score: {self.score}", fill="white", font=("Helvetica", 14))
        self.canvas.create_text(300, 350, text="Press R to Restart or ESC to Quit", fill="yellow", font=("Helvetica", 12))
        self.extrawindow.bind("r", self.restart_game)

    def restart_game(self, event=None):
        # Reset game state
        self.game_started = False
        self.game_paused = False
        self.game_over = False
        self.score = 0
        self.bullets = []
        self.enemies = []
        self.score_label.config(text=f"Score: {self.score}")
        
        # Unbind restart key
        self.extrawindow.unbind("r")
        
        # Show start screen
        self.create_start_screen()

    # game loop
    def game_loop(self):
        if self.game_paused or self.game_over or not self.game_started:
            return

        self.move_bullets()
        self.move_enemies()
        self.check_collisions()

        # check if enemies reach the player (game over)
        for enemy in self.enemies:
            if self.canvas.coords(enemy)[3] >= 360:
                self.game_over_screen()
                return

        # check if all enemies are destroyed (win condition)
        if not self.enemies:
            self.win_screen()
            return

        # set game speed
        self.extrawindow.after(50, self.game_loop)


class Game2:
    def __init__(self, window=None):
        if window is None:
            self.window = Tk()
        else:
            self.window = window
           
        # Game dimensions
        self.WIDTH = 500
        self.HEIGHT = 500
        self.SPEED = 200
        self.SPACE_SIZE = 20
        self.BODY_SIZE = 3
        self.SNAKE = "#00FF00"
        self.FOOD = "#FF0000" 
        self.BACKGROUND = "#000000"
       
        self.score = 0
        self.direction = 'right'
        self.game_started = False
        self.game_paused = False
        self.game_ended = False  # Changed from game_over to avoid conflict
        self.snake = None
        self.food = None
       
        self.setup_window()
        self.create_widgets()
        self.show_start_screen()
       
    def setup_window(self):
        self.window.title("Snake Game")
        self.window.bind('<Left>', lambda e: self.change_direction('left'))
        self.window.bind('<Right>', lambda e: self.change_direction('right'))
        self.window.bind('<Up>', lambda e: self.change_direction('up'))
        self.window.bind('<Down>', lambda e: self.change_direction('down'))
        self.window.bind('p', self.toggle_pause)
        self.window.bind('<Escape>', self.toggle_pause)
        self.window.bind('r', self.restart_game)
        self.window.bind('<space>', self.start_game)
       
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

    def show_start_screen(self):
        self.canvas.delete("all")
        self.canvas.create_text(self.WIDTH/2, self.HEIGHT/2 - 50, 
                               text="SNAKE GAME", font=('consolas', 24, 'bold'), fill="white")
        self.canvas.create_text(self.WIDTH/2, self.HEIGHT/2, 
                               text="Use Arrow Keys to Move", font=('consolas', 14), fill="lightgreen")
        self.canvas.create_text(self.WIDTH/2, self.HEIGHT/2 + 30, 
                               text="P or ESC: Pause Game", font=('consolas', 14), fill="lightblue")
        self.canvas.create_text(self.WIDTH/2, self.HEIGHT/2 + 60, 
                               text="R: Restart Game", font=('consolas', 14), fill="lightblue")
        self.canvas.create_text(self.WIDTH/2, self.HEIGHT/2 + 120, 
                               text="Press SPACE to Start", font=('consolas', 16, 'bold'), fill="yellow")
        
        self.window.bind('<space>', self.start_game)

    def show_pause_screen(self):
        self.pause_overlay = self.canvas.create_rectangle(0, 0, self.WIDTH, self.HEIGHT, fill="black", stipple="gray50")
        self.pause_text = self.canvas.create_text(self.WIDTH/2, self.HEIGHT/2 - 20, 
                                                text="GAME PAUSED", font=('consolas', 24, 'bold'), fill="white")
        self.continue_text = self.canvas.create_text(self.WIDTH/2, self.HEIGHT/2 + 20, 
                                                   text="Press P or ESC to Continue", font=('consolas', 14), fill="yellow")

    def hide_pause_screen(self):
        if hasattr(self, 'pause_overlay'):
            self.canvas.delete(self.pause_overlay)
            self.canvas.delete(self.pause_text)
            self.canvas.delete(self.continue_text)

    def toggle_pause(self, event=None):
        if self.game_started and not self.game_ended:
            self.game_paused = not self.game_paused
            if self.game_paused:
                self.show_pause_screen()
            else:
                self.hide_pause_screen()
                self.next_turn()

    def start_game(self, event=None):
        if not self.game_started:
            self.game_started = True
            self.game_paused = False
            self.game_ended = False
            self.score = 0
            self.direction = 'right'
            self.window.unbind('<space>')
            self.canvas.delete("all")
            
            # Initialize snake in the center - align to grid
            start_x = (self.WIDTH // 2 // self.SPACE_SIZE) * self.SPACE_SIZE
            start_y = (self.HEIGHT // 2 // self.SPACE_SIZE) * self.SPACE_SIZE
            
            # Create snake using the proper Snake class
            self.snake = self.Snake(self.canvas, self.BODY_SIZE, self.SPACE_SIZE, self.SNAKE, start_x, start_y)
            
            # Create first food
            self.food = self.Food(self.canvas, self.WIDTH, self.HEIGHT, self.SPACE_SIZE, self.FOOD)
            
            self.label.config(text=f"Points: {self.score}")
            self.next_turn()

    def change_direction(self, new_direction):
        if self.game_paused or not self.game_started or self.game_ended:
            return
            
        # Prevent 180-degree turns
        if (new_direction == 'left' and self.direction != 'right') or \
           (new_direction == 'right' and self.direction != 'left') or \
           (new_direction == 'up' and self.direction != 'down') or \
           (new_direction == 'down' and self.direction != 'up'):
            self.direction = new_direction
               
    def next_turn(self):
        if self.game_paused or self.game_ended or not self.game_started:
            return
            
        if not hasattr(self, 'snake') or not self.snake.coordinates:
            return
            
        # Get current head position
        head_x, head_y = self.snake.coordinates[0]

        # Calculate new head position based on direction
        if self.direction == "up":
            new_head = (head_x, head_y - self.SPACE_SIZE)
        elif self.direction == "down":
            new_head = (head_x, head_y + self.SPACE_SIZE)
        elif self.direction == "left":
            new_head = (head_x - self.SPACE_SIZE, head_y)
        elif self.direction == "right":
            new_head = (head_x + self.SPACE_SIZE, head_y)

        # Insert new head position
        self.snake.coordinates.insert(0, new_head)

        # Create new head square
        square = self.canvas.create_rectangle(
            new_head[0], new_head[1], 
            new_head[0] + self.SPACE_SIZE, 
            new_head[1] + self.SPACE_SIZE, 
            fill=self.SNAKE, tags="snake"
        )
        self.snake.squares.insert(0, square)

        # Check for food collision
        food_x, food_y = self.food.coordinates
        head_x, head_y = new_head
        
        # Check if head overlaps with food (exact coordinate match)
        if head_x == food_x and head_y == food_y:
            self.score += 1
            self.label.config(text=f"Points: {self.score}")
            self.canvas.delete("food")
            self.food = self.Food(self.canvas, self.WIDTH, self.HEIGHT, self.SPACE_SIZE, self.FOOD)
            # Snake grows when food is eaten, so don't remove tail
        else:
            # Remove tail if no food eaten
            del self.snake.coordinates[-1]
            self.canvas.delete(self.snake.squares[-1])
            del self.snake.squares[-1]

        # Check for collisions
        if self.check_collisions():
            self.show_game_over()
        else:
            self.window.after(self.SPEED, self.next_turn)
           
    def check_collisions(self):
        if not hasattr(self, 'snake') or not self.snake.coordinates:
            return True
            
        head_x, head_y = self.snake.coordinates[0]

        # Wall collision
        if head_x < 0 or head_x >= self.WIDTH or head_y < 0 or head_y >= self.HEIGHT:
            return True

        # Self collision (check if head hits any body segment)
        for body_part in self.snake.coordinates[1:]:
            if head_x == body_part[0] and head_y == body_part[1]:
                return True

        return False
       
    def show_game_over(self):  # Renamed from game_over to avoid conflict
        self.game_ended = True
        self.canvas.delete("all")
        self.canvas.create_text(self.WIDTH/2, self.HEIGHT/2 - 40, 
                               font=('consolas', 40), text="GAME OVER", fill="red", tag="gameover")
        self.canvas.create_text(self.WIDTH/2, self.HEIGHT/2 + 20, 
                               font=('consolas', 20), text=f"Score: {self.score}", fill="white")
        self.canvas.create_text(self.WIDTH/2, self.HEIGHT/2 + 60, 
                               font=('consolas', 14), text="Press R to Restart", fill="yellow")

    def restart_game(self, event=None):
        self.score = 0
        self.direction = 'right'
        self.game_started = False
        self.game_paused = False
        self.game_ended = False
        self.snake = None
        self.food = None
        self.label.config(text=f"Points: {self.score}")
        self.canvas.delete("all")
        self.show_start_screen()

    # Fixed Snake and Food classes as inner classes
    class Snake:
        def __init__(self, canvas, body_size, space_size, color, start_x, start_y):
            self.canvas = canvas
            self.body_size = body_size
            self.space_size = space_size
            self.color = color
            self.coordinates = []
            self.squares = []
            
            # Initialize snake body starting from start position
            for i in range(body_size):
                self.coordinates.append([start_x - (i * space_size), start_y])

            # Create visual squares for the snake
            for x, y in self.coordinates:
                square = canvas.create_rectangle(
                    x, y, x + space_size, y + space_size,
                    fill=color, tags="snake")
                self.squares.append(square)

    class Food:
        def __init__(self, canvas, width, height, space_size, color):
            self.canvas = canvas
            self.space_size = space_size
            
            # Ensure food spawns on grid and doesn't spawn on edges
            max_x = (width // space_size) - 1
            max_y = (height // space_size) - 1
            
            x = random.randint(1, max_x) * space_size
            y = random.randint(1, max_y) * space_size
            
            self.coordinates = [x, y]

            # Create food visual
            canvas.create_oval(
                x, y, x + space_size, y + space_size, 
                fill=color, tags="food", outline="darkred"
            )

    # Fixed Snake and Food classes as inner classes
    class Snake:
        def __init__(self, canvas, body_size, space_size, color, start_x, start_y):
            self.canvas = canvas
            self.body_size = body_size
            self.space_size = space_size
            self.color = color
            self.coordinates = []
            self.squares = []
            
            # Initialize snake body starting from start position
            for i in range(body_size):
                self.coordinates.append([start_x - (i * space_size), start_y])

            # Create visual squares for the snake
            for x, y in self.coordinates:
                square = canvas.create_rectangle(
                    x, y, x + space_size, y + space_size,
                    fill=color, tags="snake")
                self.squares.append(square)

    class Food:
        def __init__(self, canvas, width, height, space_size, color):
            self.canvas = canvas
            self.space_size = space_size
            
            # Ensure food spawns on grid and doesn't spawn on edges
            max_x = (width // space_size) - 1
            max_y = (height // space_size) - 1
            
            x = random.randint(1, max_x) * space_size
            y = random.randint(1, max_y) * space_size
            
            self.coordinates = [x, y]

            # Create food visual
            canvas.create_oval(
                x, y, x + space_size, y + space_size, 
                fill=color, tags="food", outline="darkred"
            )

class GameLauncher:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("600x450")
        self.window.title('Game Launcher')
       
        self.create_widgets()
       
    def create_widgets(self):
        # Title
        title_label = Label(self.window, text="GAME LAUNCHER", font=("Helvetica", 24, "bold"))
        title_label.pack(pady=20)
        
        button1 = ttk.Button(self.window, text='Space Invaders',
                            command=lambda: Game1(Toplevel(self.window)))
        button1.pack(expand=True, pady=10)

        button2 = ttk.Button(self.window, text='Snake Game',
                            command=lambda: Game2(Toplevel(self.window)))
        button2.pack(expand=True, pady=10)
        
        button3 = ttk.Button(self.window, text='Dinosaur Run',
                            command=lambda: Game3(Toplevel(self.window)))
        button3.pack(expand=True, pady=10)
       
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    launcher = GameLauncher()
    launcher.run()