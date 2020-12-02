

# This game is called Pong and consists in scoring points by getting the
# ball to bounce off the opponent user's side of the screen.
# There is a ball which moves across the screen.
# There are also two paddles (one for each user) which can be moved up and down
# so that the users can prevent the ball from hitting their side of the screen.
# One point is added to the score of the corresponding user when the ball hits
# the other's side. The game ends when one of the users reaches 11 points. The
# game may also end if either of the users clicks the exit button.

import pygame


# User-defined functions

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   
   # define and create our game window
   # create a pygame display window
   size = (500, 400) # (width, height)
   surface = pygame.display.set_mode(size)  
   # set the title of the display window
   pygame.display.set_caption('Pong')  
   
   # get the display surface
   w_surface = pygame.display.get_surface()
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play()
   # quit pygame and clean up the pygame window
   pygame.quit()

   

# User-defined classes

class Game:
   # An object in this class represents a complete game.

   def __init__(self, surface):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object

      # === objects that are part of every game that we will discuss
      self.surface = surface
      self.bg_color = pygame.Color('black')
     
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      # boolean represents whether either paddle is being moved up or down.
      # when an attribute evaluates to False that paddle has no movement
      self.left_paddle_moved_down = False
      self.left_paddle_moved_up = False
      self.right_paddle_moved_down = False      
      self.right_paddle_moved_up = False
      # size of the surface
      self.size = (500, 400)
     
      # === game specific objects
      # attributes of the ball object
      x = 50
      y = 50
      dx = 4
      dy = 2
      radius = 6
      # attributes of the rectangle objects
      # the width and height of both paddles
      rectangle_width = 12
      rectangle_height = 50
      # the x position of the left paddle
      x_left = 100
      # the x position of the right paddle
      x_right = 388
      # the y position of the top left corner of both paddles
      y_rectangle = 175
      # the colour of the paddles
      white = (255, 255, 255)
     
      # create a Ball object and two Rect objects
      self.small_ball = Ball('white', radius, [x, y], [dx,dy], self.surface, self.size)
      self.left_paddle = Rect(x_left, y_rectangle, rectangle_width,
                              rectangle_height, white, self.surface, self.size)
      self.right_paddle = Rect(x_right, y_rectangle, rectangle_width,
                               rectangle_height, white, self.surface, self.size)
     
      # starting scores of both players
      self.score_left_player = 0
      self.score_right_player = 0    
     
      self.max_frames = 150
      self.frame_counter = 0

   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.

      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()
         self.draw()
         self.update_score()
         self.display_text()
         if self.continue_game:
            self.small_ball.collided(self.right_paddle.y, self.left_paddle.y)
            self.update()
            self.decide_continue()
         self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second
         
   def update_score(self):
      # Detects if the ball has hit one of the sides and updates the score
      # of each player
      if self.small_ball.center[0] > self.size[0] - self.small_ball.radius:
         self.score_left_player = self.score_left_player + 1
      if self.small_ball.center[0] < self.small_ball.radius:
         self.score_right_player = self.score_right_player + 1      
               
   def display_text(self):
      # This function displays text (the players' scores) to a pygame window
      # using the specified font colours, size, and type.
      white = (255,255,255)
      font = pygame.font.SysFont("arial", 60)
      text_ing = font.render(str(self.score_left_player), True, white,
                             self.bg_color)
      self.surface.blit(text_ing, [0,0])      
      text_ing = font.render(str(self.score_right_player), True, white,
                             self.bg_color)
      self.surface.blit(text_ing, [430,0])      
      pygame.display.update()

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled
     
      # exit the game if the user presses "X"
      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
         # check if either the a, q, l, or p keys have been pressed down,
         # signifying a movement in the corresponding paddle
         # assigns the boolean True if the condition is met
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
               self.left_paddle_moved_down = True
            if event.key == pygame.K_q:
               self.left_paddle_moved_up = True
            if event.key == pygame.K_l:
               self.right_paddle_moved_down = True
            if event.key == pygame.K_p:
               self.right_paddle_moved_up = True  
         # check if either the a, q, l, or p keys have been released,
         # which makes the corresponding paddle stop moving
         # assigns the boolean False if the condition is met
         if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
               self.left_paddle_moved_down = False
            if event.key == pygame.K_q:
               self.left_paddle_moved_up = False
            if event.key == pygame.K_l:
               self.right_paddle_moved_down = False
            if event.key == pygame.K_p:
               self.right_paddle_moved_up = False            
           
           

   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
     
      self.surface.fill(self.bg_color) # clear the display surface first
      self.small_ball.draw()
      self.left_paddle.draw_rectangle()
      self.right_paddle.draw_rectangle()
      pygame.display.update() # make the updated surface appear on the display

   def update(self):
      # Update the game objects.
      # - self is the Game to update
     
      self.small_ball.move()
      # checks if any of the paddles should be moving
      # if a paddle should be moving, it calls on the corresponding method
      # to make the paddle move
      if self.left_paddle_moved_down == True:
         self.left_paddle.move_rectangle_down()
      if self.right_paddle_moved_down == True:
         self.right_paddle.move_rectangle_down()
      if self.left_paddle_moved_up == True:
         self.left_paddle.move_rectangle_up()
      if self.right_paddle_moved_up == True:
         self.right_paddle.move_rectangle_up()
      self.frame_counter = self.frame_counter + 1
         
         

   def decide_continue(self):
      # Check and remember if the game should continue
      # - self is the Game to check
     
      if self.frame_counter > self.max_frames:
         self.continue_game = True
      if self.score_left_player == 11:
         self.continue_game = False
      if self.score_right_player == 11:
         self.continue_game = False      


class Ball:
   # An object in this class represents a Ball that moves  

   def __init__(self, ball_color, ball_radius, ball_center, ball_velocity,
                surface, surface_size):
      # Initialize a Ball.
      # - self is the Ball to initialize
      # - color is the pygame.Color of the ball
      # - center is a list containing the x and y int
      #   coords of the center of the ball
      # - radius is the int pixel radius of the ball
      # - velocity is a list containing the x and y components
      # - surface is the window's pygame.Surface object
      # - size is a tuple containing the size of the surface

      self.color = pygame.Color(ball_color)
      self.radius = ball_radius
      self.center = ball_center
      self.velocity = ball_velocity
      self.surface = surface
      self.size = surface_size
     
   def move(self):
      # Change the location of the Ball by adding the corresponding
      # speed values to the x and y coordinate of its center
      # - self is the Ball
      # To have the ball bounce off the sides of the surface, change either
      # the x or y direction of the ball (depending on which side it hits)
      # when it contacts a side
     
      for i in range(0,2):
         self.center[i] = (self.center[i] + self.velocity[i])
         if i == 0:
            if self.center[i] > self.size[0] - self.radius:
               self.velocity[i] = -self.velocity[i]
            if self.center[i] < self.radius:
               self.velocity[i] = -self.velocity[i]
         if i == 1:
            if self.center[i] > self.size[1] - self.radius:
               self.velocity[i] = -self.velocity[i]  
            if self.center[i] < self.radius:
               self.velocity[i] = -self.velocity[i]
   
   def collided(self, right_paddle_y, left_paddle_y):
      # Checks if the ball hits either one of the paddles from the outside
      # Makes the ball bounce of the paddles if the condition is met
      # right_paddle_y is the current y coordinate of the top left corner of the
      # right paddle
      # left_paddle_y is the current y coordinate of the top left corner of the
      # left paddle
     
      # the width and height of both paddles
      rectangle_width = 12
      rectangle_height = 50
      # the x position of the left paddle
      x_left = 100
      # the x position of the right paddle
      x_right = 388    
     
      if int(self.velocity[0]) > 0:
         if pygame.Rect(x_right, right_paddle_y, rectangle_width,
                        rectangle_height).collidepoint(self.center[0],
                                                       self.center[1]):
            self.velocity[0] = -self.velocity[0]
      else:
         if pygame.Rect(x_left, left_paddle_y, rectangle_width,
                        rectangle_height).collidepoint(self.center[0],
                                                       self.center[1]):
            self.velocity[0] = -self.velocity[0]    

   def draw(self):
      # Draw the ball on the surface
      # - self is the Ball
     
      pygame.draw.circle(self.surface, self.color, self.center, self.radius)
 

     
class Rect:
   # creates and draws a rectangle
   # the instantiations of the class will be the right and left paddles
   
   def __init__(self, rectangle_x, rectangle_y, rectangle_width,
                rectangle_height, rectangle_color, rectangle_surface, surface_size):
      # Initialize a Rectangle.
      # - self is the Rectangle to initialize
      # - rectangle_x is the int x coordinate of the left top corner of
      # the rectangle
      # - rectangle_y is the int y coordinate of the left top corner of
      # the rectangle
      # - width is the int width of the rectangle
      # - height is the int height of the rectangle
      # - color is the color of the rectangle in RGB
      # - surface is the window's pygame.Surface object      
      # - size is a tuple containing the size of the surface
     
      self.x = rectangle_x
      self.y = rectangle_y
      self.width = rectangle_width
      self.height = rectangle_height
      self.color = rectangle_color
      self.surface = rectangle_surface
      self.size = surface_size
 
   
   def draw_rectangle(self):
      # Draw all game objects.
      # - self is the Rectangle to draw      
      pygame.draw.rect(self.surface, self.color, (self.x, self.y,
                       self.width, self.height))
   
   def move_rectangle_up(self):
      # moves paddle up
      # if the paddle hits the top of the surface, the paddle stops moving
      if self.y <= 0:
         self.y = 0
      else:
         self.y = self.y - 5
     
   def move_rectangle_down(self):
      # moves paddle down
      # if the paddle hits the bottom of the surface, the paddle stops moving
      if self.y + self.height >= self.size[1]:
         self.y = self.size[1] - self.height
      else:
         self.y = self.y + 5
             


main()
