# the pygame library is used for handling graphics, window creation, and user input.
import pygame 
# the math library provides access to mathematical functions like sine, cosine, and pi.
import math 

# initializes all of the pygame modules to get the engine ready.
pygame.init() 

# defines the width and height of the game window.
WIDTH, HEIGHT = 800, 600
# creates the main display surface (the game window itself).
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Python Raycasting Engine")
# creates a clock object, which is used to manage the frame rate.
clock = pygame.time.Clock() 

# this is the 2D game world map. it's a list of lists.
# '1' represents a wall, and '0' represents an empty space.
game_map = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

# the player's position in the game world, using floating-point numbers for smooth movement.
player_x, player_y = 3.0, 3.0 
# the player's viewing angle, measured in radians. math.pi/4 is 45 degrees.
player_angle = math.pi / 4 

# the field of view (FOV) of the player's "camera".
FOV = math.pi / 3  # 60 degrees in radians.
# half of the FOV, used to calculate the starting angle for the rays.
HALF_FOV = FOV / 2
# the number of rays we will cast. we cast one ray per vertical column of pixels.
NUM_RAYS = WIDTH
# the maximum distance a ray will travel before it gives up.
MAX_DEPTH = 20

# this function casts a single ray into the game world and returns the distance it travels before hitting a wall.
def cast_ray(angle, player_x, player_y):
    # calculate the sine and cosine of the ray's angle. these determine the ray's direction.
    sin_a = math.sin(angle)  
    cos_a = math.cos(angle)  
    
    # we check for a wall collision by taking small steps along the ray's path.
    # the loop iterates up to a maximum distance (MAX_DEPTH).
    for distance in range(1, MAX_DEPTH * 10):
        # the length of the ray at the current step. we use 0.1 increments.
        ray_distance = distance / 10.0
        
        # calculate the current x and y coordinates of the ray's tip.
        ray_x = player_x + cos_a * ray_distance
        ray_y = player_y + sin_a * ray_distance
        
        # convert the floating-point ray coordinates to integer map grid coordinates.
        map_x = int(ray_x)
        map_y = int(ray_y)
        
        # check if the current map grid cell is a wall ('1').
        # we also check to make sure the coordinates are within the map's boundaries.
        if 0 <= map_y < len(game_map) and 0 <= map_x < len(game_map[0]) and game_map[map_y][map_x] == 1:
            # if a wall is hit, return the distance to the wall.
            return ray_distance
    
    # if the ray never hits a wall within MAX_DEPTH, return MAX_DEPTH.
    return MAX_DEPTH

# this function handles drawing the entire 3D scene for a single frame.
def draw_game():
    # first, draw the floor and ceiling. this provides a sense of space.
    screen.fill((100, 100, 100))  # a solid color for the ceiling.
    # draw a rectangle for the floor, starting from the middle of the screen.
    pygame.draw.rect(screen, (70, 70, 70), (0, HEIGHT // 2, WIDTH, HEIGHT // 2))  
    
    # we iterate through each vertical column of the screen to draw a "wall slice."
    for column in range(NUM_RAYS):
        # calculate the angle for the current ray. we span from player_angle - HALF_FOV to player_angle + HALF_FOV.
        ray_angle = player_angle - HALF_FOV + (column / NUM_RAYS) * FOV
        
        # cast the ray and get the distance to the wall.
        ray_distance = cast_ray(ray_angle, player_x, player_y)
        
        # correct for the "fisheye" distortion that occurs at the edges of the screen.
        # this makes the walls look straight and realistic.
        angle_diff = player_angle - ray_angle
        corrected_distance = ray_distance * math.cos(angle_diff)
        
        # calculate the height of the wall slice. it's an inverse relationship: closer walls are taller.
        wall_height = int(HEIGHT / (corrected_distance + 0.0001))
        
        # apply simple depth-based shading: farther walls are darker.
        color_shade = max(0, 255 - int(ray_distance * 15))
        wall_color = (color_shade, color_shade, color_shade)
        
        # calculate the vertical position of the wall slice to center it on the screen.
        top = (HEIGHT - wall_height) // 2
        
        # draw a single, 1-pixel-wide vertical line for the wall slice.
        pygame.draw.line(screen, wall_color, (column, top), (column, top + wall_height), 1)

# this is the main function that runs the game loop.
def main():
    # the 'global' keyword allows us to modify these variables from within this function.
    global player_x, player_y, player_angle
    
    # a flag to control the game loop.
    running = True
    while running:
        # check for user events, like closing the window.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # get a list of all keys currently being pressed.
        keys = pygame.key.get_pressed()
        move_speed = 0.1
        turn_speed = 0.05
        
        # store the player's potential new position before applying it.
        new_x, new_y = player_x, player_y
        
        # handle forward and backward movement based on the player's current angle.
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            new_x += math.cos(player_angle) * move_speed
            new_y += math.sin(player_angle) * move_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            new_x -= math.cos(player_angle) * move_speed
            new_y -= math.sin(player_angle) * move_speed
        
        # handle rotation using both the arrow keys and 'a'/'d'.
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_angle -= turn_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_angle += turn_speed
            
        # collision detection: check if the potential new position is a wall.
        # if it's an empty space, we update the player's position.
        # this prevents the player from moving into walls.
        if game_map[int(new_y)][int(new_x)] == 0:
            player_x, player_y = new_x, new_y
            
        # call the function to draw the game world.
        draw_game()
        # update the entire screen to display what was just drawn.
        pygame.display.flip()
        # cap the frame rate at 60 frames per second.
        clock.tick(60)
    
    # once the loop ends, shut down pygame.
    pygame.quit() 

# a standard python entry point. this ensures main() is called when the script is run.
if __name__ == '__main__':
    main()
