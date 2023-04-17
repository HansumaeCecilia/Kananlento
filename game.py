import random
import pygame

DEFAULT_SCREEN_SIZE = (800, 450)
FPS_TEXT_COLOR = (128, 0, 128) # Dark purple
TEXT_COLOR = (128, 0, 0) # Dark red
DEBUG = 0

def main():
    game = Game()
    game.run()

class Game:
    def __init__(self):
        pygame.init() # Initializes modules     
        self.clock = pygame.time.Clock()
        self.is_fullscreen = False
        self.show_fps = True
        self.screen = pygame.display.set_mode(DEFAULT_SCREEN_SIZE)
        self.screen_w = self.screen.get_width()
        self.screen_h = self.screen.get_height()        
        self.running = False # Game is running
        self.font16 = pygame.font.Font("fonts/SyneMono-Regular.ttf", 16)
        self.init_graphics()
        self.init_objects()
    
    def init_graphics(self):
        big_font_size = int(96 * self.screen_h / 450)
        self.font_big = pygame.font.Font("fonts/SyneMono-Regular.ttf", big_font_size)
        original_bird_images = [pygame.image.load(f"images/chicken/flying/frame-{i}.png")
                                for i in [1, 2, 3, 4]]        
        
        self.bird_imgs = [
            pygame.transform.rotozoom(x, 0, self.screen_h / 9600).convert_alpha()
            for x in original_bird_images
        ]    

        self.bird_radius = self.bird_imgs[0].get_height()  / 2 # Approximate value
        original_bird_dead_images = [
            pygame.image.load(f"images/chicken/got_hit/frame-{i}.png")
            for i in [1, 2]
        ]

        self.bird_dead_imgs = [
            pygame.transform.rotozoom(img, 0, self.screen_h / 9600).convert_alpha()
            for img in original_bird_dead_images
        ]   
        original_bg_images = [
            pygame.image.load(f"images/background/layer_{i}.png")
            for i in [1, 2, 3]
        ]
        self.bg_imgs = [
            pygame.transform.rotozoom(img, 0, self.screen_h / img.get_height()).convert_alpha()
            for img in original_bg_images
        ]
        self.bg_widths = [img.get_width() for img in self.bg_imgs]
        self.bg_pos = [0, 0, 0]

    def init_objects(self):
        self.bird_alive = True
        self.bird_y_speed = 0
        self.bird_pos = (self.screen_w / 3, self.screen_h / 4)
        self.bird_angle = 0
        self.bird_frame = 0
        self.bird_lift = False
        self.obstacles = []
        self.add_obstacle()

    def add_obstacle(self):
        obstacle = Obstacle.make_random(self.screen_w, self.screen_h)
        self.obstacles.append(obstacle)      

    def remove_oldest_obstacle(self):
        self.obstacles.pop(0)

    def scale_positions(self, scale_x, scale_y):
        self.bird_pos = (self.bird_pos[0] * scale_x, self.bird_pos[1] * scale_y)
        for i in range(len(self.bg_pos)):
            self.bg_pos[i] = self.bg_pos[i] * scale_x      
     
    def run(self):                                         
        self.running = True
        
        # While loop for quitting the game
        while self.running:            
            self.handle_events()
            self.handle_game_logic()         
            self.update_screen()               
            self.clock.tick(60) # Wait until screen's update speed is 60fps

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
                    elif event.key in (pygame.K_f, pygame.K_F11):
                        self.toggle_fullscreen()
                    elif event.key in (pygame.K_r, pygame.K_RETURN):
                        self.init_objects()
    

    def toggle_fullscreen(self):
        old_w = self.screen_w
        old_h = self.screen_h
        if self.is_fullscreen:
            pygame.display.set_mode(DEFAULT_SCREEN_SIZE)
            self.is_fullscreen = False
        else:
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.is_fullscreen = True
        
        screen = pygame.display.get_surface()
        self.screen_w = screen.get_width()
        self.screen_h = screen.get_height()
        self.init_graphics()
        self.scale_positions(
            scale_x=(self.screen_w / old_w),
            scale_y=(self.screen_h / old_h),
        )
    
    def handle_game_logic(self):
        if self.bird_alive:
            self.bg_pos[0] -= 0.5
            self.bg_pos[1] -= 1
            self.bg_pos[2] -= 3

        bird_y = self.bird_pos[1]

        
        if self.bird_alive and self.bird_lift:
            # Bird gets lifted (0.5 px / frame)
            self.bird_y_speed -= 0.5
        else:        
            # Gravity (adds falling velocity in every frame)
            self.bird_y_speed += 0.2
        
        if self.bird_lift or not self.bird_alive:
            self.bird_frame += 1

        # Move bird by its set speed
        bird_y += self.bird_y_speed        

        if self.bird_alive:
            # Calculate the bird's angle position
            self.bird_angle = -90 * 0.04 * self.bird_y_speed
            self.bird_angle = max(min(self.bird_angle, 60), -60)

        # Check if bird has hit the ground
        if bird_y > self.screen_h * 0.82:
            bird_y = self.screen_h * 0.82
            self.bird_y_speed = 0
            self.bird_alive = False
        
        # Set bird's x-y-coordinates into self.bird_pos variable
        self.bird_pos = (self.bird_pos[0], bird_y)

        # Add new obstacle when the latest has passed screen's midpoint
        if self.obstacles[-1].position < self.screen_w / 2:
            self.add_obstacle()

        # Remove left obstacle when it disappears from the screen
        if not self.obstacles[0].is_visible():
            self.remove_oldest_obstacle()

        self.bird_collides_with_obstacle = False
        
        for obstacle in self.obstacles:            
            if self.bird_alive:
                obstacle.move(self.screen_w * 0.005)

            if obstacle.collides_with_circle(self.bird_pos, self.bird_radius):
                self.bird_collides_with_obstacle = True
            
        if self.bird_collides_with_obstacle:
            self.bird_alive = False

    def update_screen(self):    

        # Draw background layers    
        for i in range(len(self.bg_imgs)):
            # First draw the left-side bg
            self.screen.blit(self.bg_imgs[i], (self.bg_pos[i], 0))
            # If the left bg doesn't cover entire screen...
            if self.bg_pos[i] + self.bg_widths[i] < self.screen_w:
                # ...draw the same bg on the right side
                self.screen.blit(
                    self.bg_imgs[i],
                    (self.bg_pos[i] + self.bg_widths[i], 0)
                )
            # If bg had already been moved its width's worth...
            if self.bg_pos[i] < -self.bg_widths[i]:
                # ...start over
                self.bg_pos[i] += self.bg_widths[i]

        for obstacle in self.obstacles:
            obstacle.render(self.screen)

        # Draw the bird
        if self.bird_alive:
            bird_img_i = self.bird_imgs[(self.bird_frame // 3) % 4]
        else:
            bird_img_i = self.bird_dead_imgs[(self.bird_frame // 10) % 2]
        bird_img = pygame.transform.rotozoom(bird_img_i, self.bird_angle, 1)
        bird_x = self.bird_pos[0] - bird_img.get_width() / 2 * 1.55
        bird_y = self.bird_pos[1] - bird_img.get_height() / 2
        self.screen.blit(bird_img, (bird_x, bird_y))

        # Draw "GAME OVER" text
        if not self.bird_alive:
            game_over_img = self.font_big.render("GAME OVER", True, TEXT_COLOR)
            x = self.screen_w / 2 - game_over_img.get_width() / 2
            y = self.screen_h / 2 - game_over_img.get_height() / 2
            self.screen.blit(game_over_img, (x, y))

        if DEBUG:
            color = (0, 0, 0) if not self.bird_collides_with_obstacle else (255, 0, 0)
            pygame.draw.circle(self.screen, color, self.bird_pos, self.bird_radius)

        # Draw FPS number
        if self.show_fps:
            fps_text = f"{self.clock.get_fps():.1f} fps"
            fps_img = self.font16.render(fps_text, True, FPS_TEXT_COLOR)
            self.screen.blit(fps_img, (0, 0))


        pygame.display.flip()

class Obstacle:
    def __init__(self, position, upper_height, lower_height, 
                 hole_size, width=100):
        self.position = position  # Left side's position
        self.upper_height = upper_height
        self.lower_height = lower_height
        self.hole_size = hole_size
        self.width = width
        self.color = (0, 128, 0)  # Dark green

    @classmethod
    def make_random(cls, screen_w, screen_h):
        hole_size = random.randint(int(screen_h * 0.25),
                                   int(screen_h * 0.75))
        h2 = random.randint(int(screen_h * 0.15), int(screen_h * 0.75))
        h1 = screen_h - h2 - hole_size
        return cls(upper_height=h1, lower_height=h2,
                   hole_size=hole_size, position=screen_w)

    def move(self, speed):
        self.position -= speed        

    def is_visible(self):
        return self.position + self.width >= 0    
    
    def collides_with_circle(self, center, radius):
        (x, y) = center
        y1 = self.upper_height
        y2 = self.upper_height + self.hole_size
        p = self.position
        q = self.position + self.width

        if x - radius > q or x + radius < p:
            return False
        
        if y1 > y - radius or y2 < y + radius:
            return True
        
        return False

    def render(self, screen):
        x = self.position
        uy = 0
        uh = self.upper_height
        pygame.draw.rect(screen, self.color, (x, uy, self.width, uh))
        ly = screen.get_height() - self.lower_height
        lh = self.lower_height
        pygame.draw.rect(screen, self.color, (x, ly, self.width, lh))

if __name__ == "__main__":
    main()