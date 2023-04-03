import pygame

def main():
    game = Game()
    game.run()

class Game:
    def __init__(self):
        pygame.init() # Initializes modules     
        self.screen = pygame.display.set_mode((800, 600)) # Screen size, coordinates as tuple within their own parenthesis
        self.running = False # Game is running
        self.init_graphics()
        self.init_objects()
    
    def init_graphics(self):
        img_bird1 = pygame.image.load("images/chicken/flying/frame-1.png")
        self.img_bird1 = pygame.transform.rotozoom(img_bird1, 0, 1/16)
    
    def init_objects(self):
        self.bird_y_speed = 1
        self.bird_pos = (200, 300)
        self.bird_lift = False

    def run(self):                    
        clock = pygame.time.Clock()               
        self.running = True
        
        # While loop for quitting the game
        while self.running:            
            self.handle_events()
            self.handle_game_logic()         
            self.update_screen()               
            clock.tick(60) # Wait until screen's update speed is 60fps

        pygame.quit() # Quits the game

    def handle_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        self.bird_lift = True
                elif event.type == pygame.KEYUP:
                    if event.key in (pygame.K_SPACE, pygame.K_UP):
                        self.bird_lift = False
    

    def handle_game_logic(self):        
        bird_y = self.bird_pos[1]

        
        if self.bird_lift:
            # Bird gets lifted (0.5 px / frame)
            self.bird_y_speed -= 0.5
        else:        
            # Gravity (adds falling velocity in every frame)
            self.bird_y_speed += 0.2

        # Move the bird
        bird_y += self.bird_y_speed
        self.bird_pos = (self.bird_pos[0], bird_y) # Bird's position for movement

    def update_screen(self):        
        self.screen.fill((240, 240, 255)) # Give screen color by text (ie. "green") or rpg        
        self.screen.blit(self.img_bird1, self.bird_pos) # Draw the bird

        pygame.display.flip()

if __name__ == "__main__":
    main()