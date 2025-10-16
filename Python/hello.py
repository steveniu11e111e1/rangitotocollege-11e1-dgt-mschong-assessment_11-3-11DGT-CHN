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
        self.BODY_SIZE = 2
        self.SNAKE = "#00FF00"
        self.FOOD = "#FFFFFF"
        self.BACKGROUND = "#000000"
       
        self.score = 0
        self.direction = 'down'
        self.game_started = False
        self.game_paused = False
        self.game_over = False
       
        self.setup_window()
        self.create_widgets()
        self.show_start_screen()
       
    def setup_window(self):
        self.window.title("Snake Game")
        self.window.bind('<Left>', self.change_direction)
        self.window.bind('<Right>', self.change_direction)
        self.window.bind('<Up>', self.change_direction)
        self.window.bind('<Down>', self.change_direction)
        self.window.bind('p', self.toggle_pause)
        self.window.bind('<Escape>', self.toggle_pause)
        self.window.bind('r', self.restart_game)
       
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
        if self.game_started and not self.game_over:
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
            self.window.unbind('<space>')
            self.canvas.delete("all")
            self.snake = Snake(self.canvas, self.BODY_SIZE, self.SPACE_SIZE, self.SNAKE)
            self.food = Food(self.canvas, self.WIDTH, self.HEIGHT, self.SPACE_SIZE, self.FOOD)
            self.next_turn()

    def change_direction(self, new_direction):
        if self.game_paused or not self.game_started or self.game_over:
            return
            
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
        if self.game_paused or self.game_over or not self.game_started:
            return
            
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
        self.game_over = True
        self.canvas.delete(ALL)
        self.canvas.create_text(self.WIDTH/2, self.HEIGHT/2 - 20, 
                               font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")
        self.canvas.create_text(self.WIDTH/2, self.HEIGHT/2 + 40, 
                               font=('consolas', 20), text=f"Score: {self.score}", fill="white")
        self.canvas.create_text(self.WIDTH/2, self.HEIGHT/2 + 80, 
                               font=('consolas', 14), text="Press R to Restart", fill="yellow")

    def restart_game(self, event=None):
        self.score = 0
        self.direction = 'down'
        self.game_started = False
        self.game_paused = False
        self.game_over = False
        self.label.config(text=f"Points: {self.score}")
        self.show_start_screen()


class Game3:
    def __init__(self, window=None):
        if window is None:
            self.window = Tk()
        else:
            self.window = window
            
        self.window.title("Dinosaur Run")
        self.window.geometry("800x400")
        
        # Game variables
        self.game_speed = 10
        self.jump_height = 150
        self.jump_speed = 15
        self.score = 0
        self.high_score = 0
        self.is_jumping = False
        self.is_crouching = False
        self.game_started = False
        self.game_paused = False
        self.game_over = False
        self.jump_count = 0
        self.gravity = 8
        
        # Dinosaur dimensions
        self.normal_height = 40
        self.crouch_height = 20
        self.dino_width = 40
        
        # Ground level
        self.ground_y = 350
        
        # Create canvas
        self.canvas = Canvas(self.window, width=800, height=400, bg="white")
        self.canvas.pack()
        
        # Score display
        self.score_display = self.canvas.create_text(700, 30, text=f"Score: {self.score}", font=("Arial", 16), fill="black")
        self.high_score_display = self.canvas.create_text(700, 60, text=f"High Score: {self.high_score}", font=("Arial", 16), fill="black")
        
        self.setup_window()
        self.show_start_screen()
        
    def setup_window(self):
        self.window.bind("<space>", self.start_game)
        self.window.bind("<Up>", self.jump)
        self.window.bind("<Down>", self.crouch)
        self.window.bind("<KeyRelease-Down>", self.stand_up)  # New binding for key release
        self.window.bind("p", self.toggle_pause)
        self.window.bind("<Escape>", self.toggle_pause)
        self.window.bind("r", self.restart_game)
        
    def show_start_screen(self):
        self.canvas.delete("all")
        self.canvas.create_text(400, 100, text="DINOSAUR RUN", font=("Arial", 32, "bold"), fill="black")
        self.canvas.create_text(400, 150, text="Infinite Runner Game", font=("Arial", 18), fill="gray")
        
        # Draw a simple dinosaur
        self.draw_dinosaur(400, 250, 50)
        
        self.canvas.create_text(400, 320, text="CONTROLS:", font=("Arial", 16, "bold"), fill="black")
        self.canvas.create_text(400, 340, text="UP ARROW: Jump", font=("Arial", 14), fill="darkgreen")
        self.canvas.create_text(400, 360, text="DOWN ARROW: Crouch (Hold)", font=("Arial", 14), fill="darkgreen")
        self.canvas.create_text(400, 380, text="P or ESC: Pause Game", font=("Arial", 14), fill="darkblue")
        
        self.canvas.create_text(400, 300, text="Press SPACE to Start", font=("Arial", 20, "bold"), fill="red")
        
    def draw_dinosaur(self, x, y, size):
        # Draw a simple dinosaur character
        body = self.canvas.create_rectangle(x-size//2, y-size//2, x+size//2, y+size//2, fill="green", outline="darkgreen")
        head = self.canvas.create_rectangle(x+size//2, y-size//2, x+size, y-size//4, fill="green", outline="darkgreen")
        eye = self.canvas.create_oval(x+size//1.5, y-size//2, x+size//1.2, y-size//1.5, fill="white")
        pupil = self.canvas.create_oval(x+size//1.4, y-size//1.7, x+size//1.3, y-size//1.6, fill="black")
        leg1 = self.canvas.create_rectangle(x-size//4, y+size//2, x, y+size, fill="green", outline="darkgreen")
        leg2 = self.canvas.create_rectangle(x+size//4, y+size//2, x+size//2, y+size, fill="green", outline="darkgreen")
        
    def start_game(self, event=None):
        if not self.game_started:
            self.game_started = True
            self.game_paused = False
            self.score = 0
            self.canvas.delete("all")
            
            # Draw ground
            self.ground = self.canvas.create_rectangle(0, self.ground_y, 800, 400, fill="gray", outline="gray")
            
            # Draw dinosaur (normal size)
            self.dino_x = 100
            self.dino_y = self.ground_y
            self.dino = self.canvas.create_rectangle(
                self.dino_x - self.dino_width//2, 
                self.dino_y - self.normal_height,
                self.dino_x + self.dino_width//2, 
                self.dino_y, 
                fill="green", 
                outline="darkgreen"
            )
            
            # Initialize obstacles
            self.obstacles = []
            self.obstacle_speed = self.game_speed
            
            # Start game loop
            self.update_score_display()
            self.game_loop()
            
    def jump(self, event=None):
        if not self.game_started or self.game_paused or self.game_over:
            return
            
        if not self.is_jumping and not self.is_crouching:
            self.is_jumping = True
            self.jump_count = 0
            
    def crouch(self, event=None):
        if not self.game_started or self.game_paused or self.game_over:
            return
            
        if not self.is_jumping:  # Can't crouch while jumping
            self.is_crouching = True
            # Make dinosaur shorter when crouching
            self.canvas.coords(self.dino, 
                             self.dino_x - self.dino_width//2, 
                             self.dino_y - self.crouch_height,
                             self.dino_x + self.dino_width//2, 
                             self.dino_y)
            
    def stand_up(self, event=None):
        if self.is_crouching and not self.is_jumping:
            self.is_crouching = False
            # Restore normal dinosaur size
            self.canvas.coords(self.dino, 
                             self.dino_x - self.dino_width//2, 
                             self.dino_y - self.normal_height,
                             self.dino_x + self.dino_width//2, 
                             self.dino_y)
            
    def toggle_pause(self, event=None):
        if self.game_started and not self.game_over:
            self.game_paused = not self.game_paused
            if self.game_paused:
                self.show_pause_screen()
            else:
                self.hide_pause_screen()
                self.game_loop()
                
    def show_pause_screen(self):
        self.pause_overlay = self.canvas.create_rectangle(200, 150, 600, 250, fill="white", outline="black", width=2)
        self.pause_text = self.canvas.create_text(400, 200, text="GAME PAUSED", font=("Arial", 24, "bold"), fill="black")
        
    def hide_pause_screen(self):
        if hasattr(self, 'pause_overlay'):
            self.canvas.delete(self.pause_overlay)
            self.canvas.delete(self.pause_text)
            
    def update_score_display(self):
        self.canvas.itemconfig(self.score_display, text=f"Score: {self.score}")
        self.canvas.itemconfig(self.high_score_display, text=f"High Score: {self.high_score}")
        
    def create_obstacle(self):
        obstacle_types = [
            {"width": 20, "height": 40, "y": self.ground_y - 40, "color": "red"},  # Cactus
            {"width": 40, "height": 20, "y": self.ground_y - 20, "color": "brown"},  # Rock
            {"width": 60, "height": 30, "y": self.ground_y - 30, "color": "darkred"}   # Big rock
        ]
        
        obstacle_type = random.choice(obstacle_types)
        obstacle = self.canvas.create_rectangle(
            800, obstacle_type["y"] - obstacle_type["height"],
            800 + obstacle_type["width"], obstacle_type["y"],
            fill=obstacle_type["color"], outline="black"
        )
        
        self.obstacles.append({
            "id": obstacle,
            "width": obstacle_type["width"],
            "height": obstacle_type["height"],
            "y": obstacle_type["y"]
        })
        
    def move_obstacles(self):
        for obstacle in self.obstacles[:]:
            self.canvas.move(obstacle["id"], -self.obstacle_speed, 0)
            
            # Remove obstacles that are off screen
            if self.canvas.coords(obstacle["id"])[2] < 0:
                self.canvas.delete(obstacle["id"])
                self.obstacles.remove(obstacle)
                
    def check_collisions(self):
        dino_coords = self.canvas.coords(self.dino)
        
        for obstacle in self.obstacles:
            obstacle_coords = self.canvas.coords(obstacle["id"])
            
            # Simple collision detection
            if (dino_coords[2] > obstacle_coords[0] and  # Dino right edge > obstacle left edge
                dino_coords[0] < obstacle_coords[2] and  # Dino left edge < obstacle right edge
                dino_coords[1] < obstacle_coords[3] and  # Dino top < obstacle bottom
                dino_coords[3] > obstacle_coords[1]):    # Dino bottom > obstacle top
                return True
                
        return False
        
    def handle_jump(self):
        if self.is_jumping:
            if self.jump_count < self.jump_height // self.jump_speed:
                self.canvas.move(self.dino, 0, -self.jump_speed)
                self.jump_count += 1
            else:
                self.is_jumping = False
        elif self.canvas.coords(self.dino)[3] < self.ground_y:
            # Apply gravity
            self.canvas.move(self.dino, 0, self.gravity)
            
    def game_loop(self):
        if self.game_paused or self.game_over or not self.game_started:
            return
            
        # Handle jumping
        self.handle_jump()
        
        # Move obstacles
        self.move_obstacles()
        
        # Create new obstacles randomly
        if random.random() < 0.02 and len(self.obstacles) < 3:  # 2% chance each frame
            self.create_obstacle()
            
        # Increase score
        self.score += 1
        if self.score > self.high_score:
            self.high_score = self.score
            
        # Increase difficulty
        if self.score % 500 == 0:
            self.obstacle_speed += 1
            
        # Check collisions
        if self.check_collisions():
            self.game_over_screen()
            return
            
        self.update_score_display()
        self.window.after(30, self.game_loop)
        
    def game_over_screen(self):
        self.game_over = True
        # Make sure dinosaur is standing up when game ends
        if self.is_crouching:
            self.stand_up()
            
        self.canvas.create_rectangle(200, 150, 600, 300, fill="white", outline="red", width=3)
        self.canvas.create_text(400, 180, text="GAME OVER", font=("Arial", 28, "bold"), fill="red")
        self.canvas.create_text(400, 220, text=f"Final Score: {self.score}", font=("Arial", 20), fill="black")
        self.canvas.create_text(400, 250, text=f"High Score: {self.high_score}", font=("Arial", 20), fill="black")
        self.canvas.create_text(400, 280, text="Press R to Restart", font=("Arial", 16), fill="blue")
        
    def restart_game(self, event=None):
        self.score = 0
        self.game_started = False
        self.game_paused = False
        self.game_over = False
        self.is_crouching = False  # Reset crouching state
        self.is_jumping = False    # Reset jumping state
        self.obstacle_speed = self.game_speed
        self.obstacles = []
        self.show_start_screen()

# Assets of Snake Game
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
        x = random.randint(0, (width // space_size)-1) * space_size
        y = random.randint(0, (height // space_size) - 1) * space_size
        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + space_size, y + space_size, fill=color, tag="food")


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