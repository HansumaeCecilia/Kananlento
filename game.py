import pygame

def main():
    game = Game()
    game.run()

class Game:
    def __init__(self):
        pygame.init() # Initializes modules     
        self.screen = pygame.display.set_mode((800, 600)) # Screen size, coordinates as tuple within their own parenthesis
        self.running = False # Game is running

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

    def update_screen(self):
        self.screen.fill((240, 240, 255)) # Give screen color by text (ie. "green") or rpg  
        pygame.display.flip()

    def handle_game_logic(self):
        pass

if __name__ == "__main__":
    main()