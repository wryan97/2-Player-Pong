## Created 12/20/2018
## Ryan <wryan97 on github>




import pygame, sys
from pygame.locals import *


#Colors of game
BLACK = (0,0,0)
WHITE = (255,255,255)

#Window width/height
WINDOW_HEIGHT = 300
WINDOW_WIDTH = 400

#Line thickness and paddle height
line_thickness = 10
paddle_height = 50

#starts game with ball going towards player 1's upper corner
dir_x = -1
dir_y = -1

#sets up window
DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

# Number of frames per second
FPS = 200
FPSCLOCK = pygame.time.Clock()

#the ball class with its methods
class Ball():
	def __init__(self,x,y,w,h,speed):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.speed = speed
		self.dir_x = -1  ## -1 = left, 1 = right
		self.dir_y = -1  ## -1 = up, 1 = down

		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

	#draws ball
	def draw(self):
		pygame.draw.rect(DISPLAYSURF, WHITE, self.rect)

	#moves the ball in accordance with speed
	#also uses detection methods for walls and ceilings
	def move(self, dir_x, dir_y):
		self.hit_ceiling_floor(dir_y)
		self.hit_wall()
		self.rect.x += (self.dir_x * self.speed)
		self.rect.y += (self.dir_y * self.speed)

	#changes the direction of the ball (if it was about to go out the top, change direction to bottom)
	def bounce(self,axis):
		if axis == 'x' :
			self.dir_x = self.dir_x * -1
		elif axis == 'y' :
			self.dir_y = self.dir_y * -1

	#detects if it will hit either the bottom or the top of the window
	def hit_ceiling_floor(self, dir_y): 
		if(self.rect.top == (line_thickness) or self.rect.bottom == (WINDOW_HEIGHT - 10)) :
			self.bounce('y')

	#detects if ball will hit walls of window
	def hit_wall(self):
		if(self.rect.left == (line_thickness) or self.rect.right == (WINDOW_WIDTH - 10)):
			self.bounce('x')

	#detects if ball will hit one of the paddles
	def hit_paddle(self, paddle): 
		if (self.dir_x == -1 and paddle.rect.right == self.rect.left and
			paddle.rect.top < self.rect.top and
			paddle.rect.bottom > self.rect.bottom):
			return True
		elif (self.dir_x == 1 and paddle.rect.left == self.rect.right and
			paddle.rect.top < self.rect.top and
			paddle.rect.bottom > self.rect.bottom):
			return True
		else:
			return False

	#detects if the ball has passed player 1
	def pass_user1(self):
		if self.rect.left == line_thickness:
			return True

	#detects if the ball has passed player 2
	def pass_user2(self):
		if self.rect.right == WINDOW_WIDTH - line_thickness:
			return True

#defines the paddle class and its methods
class Paddle():
	def __init__(self,x,w,h):
		self.x = x
		self.w = w
		self.h = h
		self.y = int(WINDOW_HEIGHT / 2 - self.h / 2) 

		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

	#draws the paddle
	def draw(self):
		#stops if moving too low
		if self.rect.bottom > WINDOW_HEIGHT - line_thickness:
			self.rect.bottom = WINDOW_HEIGHT - line_thickness
		#stops if moving too high
		elif self.rect.top < line_thickness:
			self.rect.top = line_thickness
		#draws paddle
		pygame.draw.rect(DISPLAYSURF, WHITE, self.rect)

	#moves the paddle up and down
	def move(self, pos):
		if pos == 1:
			self.rect.y = self.rect.y + 40
			self.draw
		elif pos == -1:
			self.rect.y = self.rect.y - 40
			self.draw

#defines the scoreboard class and its methods
class ScoreBoard():
	def __init__(self,score1 = 0, score2 = 0, x = WINDOW_WIDTH-150, y = 25, font_size = 20):
		self.score1 = score1
		self.score2 = score2
		self.x = x
		self.y = y
		self.font = pygame.font.Font('freesansbold.ttf', font_size) 

	#displays both the score of player 1 and 2
	def display(self, score1, score2):
		result1Surf = BASICFONT.render('Score = %s' %(score2), True, WHITE)
		result1Rect = result1Surf.get_rect()
		result1Rect.topright = (WINDOW_WIDTH-50, 25)
		DISPLAYSURF.blit(result1Surf, result1Rect)


		result2Surf = BASICFONT.render('Score = %s' %(score1), True, WHITE)
		result2Rect = result2Surf.get_rect()
		result2Rect.topleft = (WINDOW_WIDTH-350, 25)
		DISPLAYSURF.blit(result2Surf, result2Rect)

#defines the game class and its inner methods
class Game():
	def __init__(self, line_thickness = 10,speed = 5):
		global BASICFONT
		BASICFONT = pygame.font.Font('freesansbold.ttf', 20)
		self.line_thickness = line_thickness
		self.speed = speed
		self.score1 = 0
		self.score2 = 0
		
		ball_x = int(WINDOW_WIDTH/2 - self.line_thickness/2)
		ball_y = int(WINDOW_HEIGHT/2 - self.line_thickness/2)
		self.ball = Ball(ball_x,ball_y, self.line_thickness, 
							self.line_thickness, self.speed)

		self.paddles = {}

		paddle_width = self.line_thickness

		user1_paddle_x = 20
		user2_paddle_x = WINDOW_WIDTH - paddle_width - 20

		self.paddles['user1'] = Paddle(user1_paddle_x, paddle_width, paddle_height)
		self.paddles['user2'] = Paddle(user2_paddle_x, paddle_width, paddle_height)

		self.scoreboard = ScoreBoard(0, 0)

	#draws the area for the game to be played in
	def draw_arena(self):
		DISPLAYSURF.fill(BLACK)
		pygame.draw.rect(DISPLAYSURF, WHITE, ((0,0),
			(WINDOW_WIDTH,WINDOW_HEIGHT)), 20)
		pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOW_WIDTH/2),0),((WINDOW_WIDTH/2),WINDOW_HEIGHT), 3)

	#refreshes the screen to show what has changed in the game
	def update(self):
		if (self.score1 == 5):
			DISPLAYSURF.fill(BLACK)
			winner1Surf = BASICFONT.render('PLAYER 1 WINS', True, WHITE)
			winner1Rect = winner1Surf.get_rect()
			winner1Rect = (WINDOW_WIDTH - 275, WINDOW_HEIGHT/2)
			DISPLAYSURF.blit(winner1Surf, winner1Rect)

		elif (self.score2 == 5):
			DISPLAYSURF.fill(BLACK)
			winner2Surf = BASICFONT.render('PLAYER 2 WINS', True, WHITE)
			winner2Rect = winner2Surf.get_rect()
			winner2Rect = (WINDOW_WIDTH - 275, WINDOW_HEIGHT/2)
			DISPLAYSURF.blit(winner2Surf, winner2Rect)
		else:
			self.ball.move(dir_x, dir_y)

			if self.ball.hit_paddle(self.paddles['user1']):
				self.ball.bounce('x')
				self.ball.move(dir_x, dir_y)

			elif self.ball.hit_paddle(self.paddles['user2']):
				self.ball.bounce('x')
				self.ball.move(dir_x, dir_y)

			
			elif self.ball.pass_user1():
				self.score2 += 1
				ball_x = int(WINDOW_WIDTH/2 - self.line_thickness/2)
				ball_y = int(WINDOW_HEIGHT/2 - self.line_thickness/2)
				self.ball = Ball(ball_x,ball_y, self.line_thickness, 
							self.line_thickness, self.speed)

			elif self.ball.pass_user2():
				self.score1 += 1
				ball_x = int(WINDOW_WIDTH/2 - self.line_thickness/2)
				ball_y = int(WINDOW_HEIGHT/2 - self.line_thickness/2)
				self.ball = Ball(ball_x,ball_y, self.line_thickness, 
						self.line_thickness, self.speed)

			self.draw_arena()
			self.ball.draw()
			self.paddles['user1'].draw()
			self.paddles['user2'].draw()
			self.scoreboard.display(self.score1, self.score2)

#main function to create window
def main():
	pygame.init()
	pygame.display.set_caption('Pong')

	game = Game()

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()			
			if event.type == pygame.KEYDOWN:
				#W is up for player1
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
				if event.key == pygame.K_t:
					main()
				if event.key == pygame.K_w:
					game.paddles['user1'].move(-1)
				#S is down for player 1
				elif event.key == pygame.K_s:
					game.paddles['user1'].move(1)
				#I is up for player 2
				elif event.key == pygame.K_UP:
					game.paddles['user2'].move(-1)
				#K is down for player 2
				elif event.key == pygame.K_DOWN:
					game.paddles['user2'].move(1)

		game.update()		
		pygame.display.update()
		FPSCLOCK.tick(FPS)
		
if __name__ == '__main__':
	main()

