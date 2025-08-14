import pygame 
import math 

pygame.init() 

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("raycasting_engine")
clock = pygame.time.Clock() 

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

player_x, player_y = 3.0, 3.0 
player_angle = math.pi / 4 

FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH
MAX_DEPTH = 20

def cast_ray(angle, player_x, player_y):
    sin_a = math.sin(angle)  
    cos_a = math.cos(angle)  
    
    for distance in range(1, MAX_DEPTH * 10):
        ray_distance = distance / 10.0
        
        ray_x = player_x + cos_a * ray_distance
        ray_y = player_y + sin_a * ray_distance
        
        map_x = int(ray_x)
        map_y = int(ray_y)
        
        if 0 <= map_y < len(game_map) and 0 <= map_x < len(game_map[0]) and game_map[map_y][map_x] == 1:
            return ray_distance
    
    return MAX_DEPTH

def draw_game():
    screen.fill((100, 100, 100))
    pygame.draw.rect(screen, (70, 70, 70), (0, HEIGHT // 2, WIDTH, HEIGHT // 2))
    
    for column in range(NUM_RAYS):
        ray_angle = player_angle - HALF_FOV + (column / NUM_RAYS) * FOV
        
        ray_distance = cast_ray(ray_angle, player_x, player_y)
        
        angle_diff = player_angle - ray_angle
        corrected_distance = ray_distance * math.cos(angle_diff)
        
        wall_height = int(HEIGHT / (corrected_distance + 0.0001))
        
        color_shade = max(0, 255 - int(ray_distance * 15))
        wall_color = (color_shade, color_shade, color_shade)
        
        top = (HEIGHT - wall_height) // 2
        
        pygame.draw.line(screen, wall_color, (column, top), (column, top + wall_height), 1)

def main():
    global player_x, player_y, player_angle
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        move_speed = 0.1
        turn_speed = 0.05
        
        new_x, new_y = player_x, player_y
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            new_x += math.cos(player_angle) * move_speed
            new_y += math.sin(player_angle) * move_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            new_x -= math.cos(player_angle) * move_speed
            new_y -= math.sin(player_angle) * move_speed
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_angle -= turn_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_angle += turn_speed
            
        if game_map[int(new_y)][int(new_x)] == 0:
            player_x, player_y = new_x, new_y
            
        draw_game()
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit() 

if __name__ == '__main__':
    main()
