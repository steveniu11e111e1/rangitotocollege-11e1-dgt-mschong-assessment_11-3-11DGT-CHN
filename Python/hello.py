"""Project starfish: A GUI-based game launcher with three mini-games.




1.Space Invaders: Defend Earth from alien invasion by shooting them down.
2.Snake Game: Control a snake to eat food and grow without hitting
walls or yourself.
3.Dinosaur Run: Jump over obstacles as a running dinosaur to achieve
high score.




Class: purpose is to organize each function of the game.
Def: are the function of the game in control of the games controls,
mechancis and UI.
try and except: blocks to catch errors and display message boxes for
user feedback.
message box: are used to inform users of there error of interaction.
"""


from tkinter import *
import tkinter as tk
from tkinter import ttk
import random
import time
import tkinter.messagebox


class Game1:
    def __init__(self, window=None):
        try:
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
            self.game_over = False
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


        except Exception as e:
            tkinter.messagebox.showerror("Initialization Error", f"Failed to initialize Space Invaders: {str(e)}")
            if hasattr(self, 'extrawindow'):
                self.extrawindow.destroy()


    def create_start_screen(self):
        try:
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
        except Exception as e:
            tkinter.messagebox.showerror("UI Error", f"Failed to create start screen: {str(e)}")


    def show_pause_screen(self):
        try:
            # Create semi-transparent overlay
            self.pause_overlay = self.canvas.create_rectangle(0, 0, 600, 400, fill="black", stipple="gray50")
            self.pause_text = self.canvas.create_text(300, 200, text="GAME PAUSED", font=("Helvetica", 24, "bold"), fill="white")
            self.continue_text = self.canvas.create_text(300, 250, text="Press P or ESC to Continue", font=("Helvetica", 14), fill="yellow")
        except Exception as e:
            tkinter.messagebox.showerror("UI Error", f"Failed to show pause screen: {str(e)}")


    def hide_pause_screen(self):
        try:
            if hasattr(self, 'pause_overlay'):
                self.canvas.delete(self.pause_overlay)
            if hasattr(self, 'pause_text'):
                self.canvas.delete(self.pause_text)
            if hasattr(self, 'continue_text'):
                self.canvas.delete(self.continue_text)
        except Exception as e:
            print(f"Error hiding pause screen: {e}")


    def toggle_pause(self, event=None):
        try:
            if self.game_started and not self.game_over:
                self.game_paused = not self.game_paused
                if self.game_paused:
                    self.show_pause_screen()
                else:
                    self.hide_pause_screen()
                    self.game_loop()
        except Exception as e:
            tkinter.messagebox.showerror("Game Error", f"Failed to toggle pause: {str(e)}")


    def start_game(self, event=None):
        try:
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
        except Exception as e:
            tkinter.messagebox.showerror("Game Error", f"Failed to start game: {str(e)}")


    def move_player(self, event):
        try:
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
        except Exception as e:
            print(f"Movement error: {e}")


    def fire_bullet(self):
        try:
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
        except Exception as e:
            print(f"Bullet creation error: {e}")


    def create_enemies(self):
        try:
            for i in range(5):
                for j in range(8):
                    enemy = self.canvas.create_rectangle(50 + j * 60, 50 + i * 30, 80 + j * 60, 80 + i * 30, fill="red")
                    self.enemies.append(enemy)
        except Exception as e:
            tkinter.messagebox.showerror("Game Error", f"Failed to create enemies: {str(e)}")


    def move_bullets(self):
        try:
            for bullet in self.bullets[:]:
                self.canvas.move(bullet, 0, self.bullet_speed)


                if self.canvas.coords(bullet)[1] < 0:
                    self.canvas.delete(bullet)
                    self.bullets.remove(bullet)
        except Exception as e:
            print(f"Bullet movement error: {e}")


    def move_enemies(self):
        try:
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
        except Exception as e:
            print(f"Enemy movement error: {e}")


    def check_collisions(self):
        try:
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
        except Exception as e:
            print(f"Collision detection error: {e}")


    def game_over_screen(self):
        try:
            self.game_over = True
            self.canvas.create_rectangle(150, 150, 450, 250, fill="black", outline="white")
            self.canvas.create_text(300, 180, text="GAME OVER", fill="red", font=("Helvetica", 24, "bold"))
            self.canvas.create_text(300, 220, text=f"Final Score: {self.score}", fill="white", font=("Helvetica", 14))
            self.canvas.create_text(300, 350, text="Press R to Restart or ESC to Quit", fill="yellow", font=("Helvetica", 12))
            self.extrawindow.bind("r", self.restart_game)
        except Exception as e:
            tkinter.messagebox.showerror("UI Error", f"Failed to show game over screen: {str(e)}")


    def win_screen(self):
        try:
            self.game_over = True
            self.canvas.create_rectangle(150, 150, 450, 250, fill="black", outline="green")
            self.canvas.create_text(300, 180, text="YOU WIN!", fill="green", font=("Helvetica", 24, "bold"))
            self.canvas.create_text(300, 220, text=f"Final Score: {self.score}", fill="white", font=("Helvetica", 14))
            self.canvas.create_text(300, 350, text="Press R to Restart or ESC to Quit", fill="yellow", font=("Helvetica", 12))
            self.extrawindow.bind("r", self.restart_game)
        except Exception as e:
            tkinter.messagebox.showerror("UI Error", f"Failed to show win screen: {str(e)}")


    def restart_game(self, event=None):
        try:
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
        except Exception as e:
            tkinter.messagebox.showerror("Game Error", f"Failed to restart game: {str(e)}")


    def game_loop(self):
        try:
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
        except Exception as e:
            tkinter.messagebox.showerror("Game Loop Error", f"Game loop failed: {str(e)}")




class Game2:
    def __init__(self, window=None):
        try:
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
            self.game_ended = False
            self.snake = None
            self.food = None
            self.snake_length = self.BODY_SIZE
           
            self.setup_window()
            self.create_widgets()
            self.show_start_screen()
           
        except Exception as e:
            tkinter.messagebox.showerror("Initialization Error", f"Failed to initialize Snake Game: {str(e)}")
            if hasattr(self, 'window'):
                self.window.destroy()


    def setup_window(self):
        try:
            self.window.title("Snake Game")
            self.window.bind('<Left>', lambda e: self.change_direction('left'))
            self.window.bind('<Right>', lambda e: self.change_direction('right'))
            self.window.bind('<Up>', lambda e: self.change_direction('up'))
            self.window.bind('<Down>', lambda e: self.change_direction('down'))
            self.window.bind('p', self.toggle_pause)
            self.window.bind('<Escape>', self.toggle_pause)
            self.window.bind('r', self.restart_game)
            self.window.bind('<space>', self.start_game)
        except Exception as e:
            tkinter.messagebox.showerror("Setup Error", f"Failed to setup window: {str(e)}")


    def create_widgets(self):
        try:
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
        except Exception as e:
            tkinter.messagebox.showerror("UI Error", f"Failed to create widgets: {str(e)}")


    def show_start_screen(self):
        try:
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
        except Exception as e:
            tkinter.messagebox.showerror("UI Error", f"Failed to show start screen: {str(e)}")


    def show_pause_screen(self):
        try:
            self.pause_overlay = self.canvas.create_rectangle(0, 0, self.WIDTH, self.HEIGHT, fill="black", stipple="gray50")
            self.pause_text = self.canvas.create_text(self.WIDTH/2, self.HEIGHT/2 - 20,
                                                    text="GAME PAUSED", font=('consolas', 24, 'bold'), fill="white")
            self.continue_text = self.canvas.create_text(self.WIDTH/2, self.HEIGHT/2 + 20,
                                                       text="Press P or ESC to Continue", font=('consolas', 14), fill="yellow")
        except Exception as e:
            tkinter.messagebox.showerror("UI Error", f"Failed to show pause screen: {str(e)}")


    def hide_pause_screen(self):
        try:
            if hasattr(self, 'pause_overlay'):
                self.canvas.delete(self.pause_overlay)
            if hasattr(self, 'pause_text'):
                self.canvas.delete(self.pause_text)
            if hasattr(self, 'continue_text'):
                self.canvas.delete(self.continue_text)
        except Exception as e:
            print(f"Error hiding pause screen: {e}")


    def toggle_pause(self, event=None):
        try:
            if self.game_started and not self.game_ended:
                self.game_paused = not self.game_paused
                if self.game_paused:
                    self.show_pause_screen()
                else:
                    self.hide_pause_screen()
                    self.next_turn()
        except Exception as e:
            tkinter.messagebox.showerror("Game Error", f"Failed to toggle pause: {str(e)}")


    def start_game(self, event=None):
        try:
            if not self.game_started:
                self.game_started = True
                self.game_paused = False
                self.game_ended = False
                self.score = 0
                self.direction = 'right'
                self.snake_length = self.BODY_SIZE
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
        except Exception as e:
            tkinter.messagebox.showerror("Game Error", f"Failed to start game: {str(e)}")


    def change_direction(self, new_direction):
        try:
            if self.game_paused or not self.game_started or self.game_ended:
                return
               
            # Prevent 180-degree turns
            if (new_direction == 'left' and self.direction != 'right') or \
               (new_direction == 'right' and self.direction != 'left') or \
               (new_direction == 'up' and self.direction != 'down') or \
               (new_direction == 'down' and self.direction != 'up'):
                self.direction = new_direction
        except Exception as e:
            print(f"Direction change error: {e}")


    def next_turn(self):
        try:
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
                self.snake_length += 1
                self.label.config(text=f"Points: {self.score}")
                self.canvas.delete("food")
                self.food = self.Food(self.canvas, self.WIDTH, self.HEIGHT, self.SPACE_SIZE, self.FOOD)
            else:
                # Remove tail if no food eaten AND snake is longer than it should be
                if len(self.snake.coordinates) > self.snake_length:
                    del self.snake.coordinates[-1]
                    self.canvas.delete(self.snake.squares[-1])
                    del self.snake.squares[-1]


            # Check for collisions
            if self.check_collisions():
                self.show_game_over()
            else:
                self.window.after(self.SPEED, self.next_turn)
        except Exception as e:
            tkinter.messagebox.showerror("Game Loop Error", f"Game loop failed: {str(e)}")
           
    def check_collisions(self):
        try:
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
        except Exception as e:
            print(f"Collision detection error: {e}")
            return True
       
    def show_game_over(self):
        try:
            self.game_ended = True
            self.canvas.delete("all")
            self.canvas.create_text(self.WIDTH/2, self.HEIGHT/2 - 40,
                                   font=('consolas', 40), text="GAME OVER", fill="red", tag="gameover")
            self.canvas.create_text(self.WIDTH/2, self.HEIGHT/2 + 20,
                                   font=('consolas', 20), text=f"Score: {self.score}", fill="white")
            self.canvas.create_text(self.WIDTH/2, self.HEIGHT/2 + 60,
                                   font=('consolas', 14), text="Press R to Restart", fill="yellow")
        except Exception as e:
            tkinter.messagebox.showerror("UI Error", f"Failed to show game over screen: {str(e)}")


    def restart_game(self, event=None):
        try:
            self.score = 0
            self.direction = 'right'
            self.game_started = False
            self.game_paused = False
            self.game_ended = False
            self.snake_length = self.BODY_SIZE
            self.snake = None
            self.food = None
            self.label.config(text=f"Points: {self.score}")
            self.canvas.delete("all")
            self.show_start_screen()
        except Exception as e:
            tkinter.messagebox.showerror("Game Error", f"Failed to restart game: {str(e)}")


    class Snake:
        def __init__(self, canvas, body_size, space_size, color, start_x, start_y):
            try:
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
            except Exception as e:
                raise Exception(f"Failed to create snake: {str(e)}")


    class Food:
        def __init__(self, canvas, width, height, space_size, color):
            try:
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
            except Exception as e:
                raise Exception(f"Failed to create food: {str(e)}")




class Game3:
    def __init__(self, window=None):
        try:
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
           
        except Exception as e:
            tkinter.messagebox.showerror("Initialization Error", f"Failed to initialize Dinosaur Run: {str(e)}")
            if hasattr(self, 'window'):
                self.window.destroy()


    def setup_window(self):
        try:
            self.window.bind("<space>", self.start_game)
            self.window.bind("<Up>", self.jump)
            self.window.bind("<Down>", self.crouch)
            self.window.bind("<KeyRelease-Down>", self.stand_up)
            self.window.bind("p", self.toggle_pause)
            self.window.bind("<Escape>", self.toggle_pause)
            self.window.bind("r", self.restart_game)
        except Exception as e:
            tkinter.messagebox.showerror("Setup Error", f"Failed to setup window controls: {str(e)}")


    def show_start_screen(self):
        try:
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
        except Exception as e:
            tkinter.messagebox.showerror("UI Error", f"Failed to show start screen: {str(e)}")


    def draw_dinosaur(self, x, y, size):
        try:
            # Draw a simple dinosaur character
            body = self.canvas.create_rectangle(x-size//2, y-size//2, x+size//2, y+size//2, fill="green", outline="darkgreen")
            head = self.canvas.create_rectangle(x+size//2, y-size//2, x+size, y-size//4, fill="green", outline="darkgreen")
            eye = self.canvas.create_oval(x+size//1.5, y-size//2, x+size//1.2, y-size//1.5, fill="white")
            pupil = self.canvas.create_oval(x+size//1.4, y-size//1.7, x+size//1.3, y-size//1.6, fill="black")
            leg1 = self.canvas.create_rectangle(x-size//4, y+size//2, x, y+size, fill="green", outline="darkgreen")
            leg2 = self.canvas.create_rectangle(x+size//4, y+size//2, x+size//2, y+size, fill="green", outline="darkgreen")
        except Exception as e:
            print(f"Error drawing dinosaur: {e}")


    def start_game(self, event=None):
        try:
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
        except Exception as e:
            tkinter.messagebox.showerror("Game Error", f"Failed to start game: {str(e)}")


    def jump(self, event=None):
        try:
            if not self.game_started or self.game_paused or self.game_over:
                return
               
            if not self.is_jumping and not self.is_crouching:
                self.is_jumping = True
                self.jump_count = 0
        except Exception as e:
            print(f"Jump error: {e}")


    def crouch(self, event=None):
        try:
            if not self.game_started or self.game_paused or self.game_over:
                return
               
            if not self.is_jumping:
                self.is_crouching = True
                # Make dinosaur shorter when crouching
                self.canvas.coords(self.dino,
                                 self.dino_x - self.dino_width//2,
                                 self.dino_y - self.crouch_height,
                                 self.dino_x + self.dino_width//2,
                                 self.dino_y)
        except Exception as e:
            print(f"Crouch error: {e}")


    def stand_up(self, event=None):
        try:
            if self.is_crouching and not self.is_jumping:
                self.is_crouching = False
                # Restore normal dinosaur size
                self.canvas.coords(self.dino,
                                 self.dino_x - self.dino_width//2,
                                 self.dino_y - self.normal_height,
                                 self.dino_x + self.dino_width//2,
                                 self.dino_y)
        except Exception as e:
            print(f"Stand up error: {e}")


    def toggle_pause(self, event=None):
        try:
            if self.game_started and not self.game_over:
                self.game_paused = not self.game_paused
                if self.game_paused:
                    self.show_pause_screen()
                else:
                    self.hide_pause_screen()
                    self.game_loop()
        except Exception as e:
            tkinter.messagebox.showerror("Game Error", f"Failed to toggle pause: {str(e)}")


    def show_pause_screen(self):
        try:
            self.pause_overlay = self.canvas.create_rectangle(200, 150, 600, 250, fill="white", outline="black", width=2)
            self.pause_text = self.canvas.create_text(400, 200, text="GAME PAUSED", font=("Arial", 24, "bold"), fill="black")
        except Exception as e:
            tkinter.messagebox.showerror("UI Error", f"Failed to show pause screen: {str(e)}")


    def hide_pause_screen(self):
        try:
            if hasattr(self, 'pause_overlay'):
                self.canvas.delete(self.pause_overlay)
            if hasattr(self, 'pause_text'):
                self.canvas.delete(self.pause_text)
        except Exception as e:
            print(f"Error hiding pause screen: {e}")


    def update_score_display(self):
        try:
            self.canvas.itemconfig(self.score_display, text=f"Score: {self.score}")
       
            self.canvas.itemconfig(self.high_score_display, text=f"High Score: {self.high_score}")
        except Exception as e:
            print(f"Score update error: {e}")
