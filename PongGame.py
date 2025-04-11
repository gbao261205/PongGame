import pygame
import random
import math

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ game
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong Game")

pygame.mixer.music.load("Music\music.mp3") 
volume_music = 50
pygame.mixer.music.set_volume(volume_music/100)

pygame.mixer.music.play(-1)

# Tải hình nền và điều chỉnh kích thước cho khớp với màn hình
background = pygame.image.load('Background\PONG_GAME_PLAY.png')
background = pygame.transform.scale(background, (screen_width, screen_height))

background_lose = pygame.image.load('Background\Background_Lose.png')
background_lose = pygame.transform.scale(background_lose, (screen_width, screen_height))

background_mode = pygame.image.load('Background\PONG_GAME.png')
background_mode = pygame.transform.scale(background_mode, (screen_width, screen_height))

background_player1 = pygame.image.load('Background\Background_winner_player1.png')
background_player1 = pygame.transform.scale(background_player1, (screen_width, screen_height))

background_player2 = pygame.image.load('Background\Background_winner_player2.png')
background_player2 = pygame.transform.scale(background_player2, (screen_width, screen_height))

background_draw = pygame.image.load('Background\Background_draw.png')
background_draw = pygame.transform.scale(background_draw, (screen_width, screen_height))

background_leaderboard = pygame.image.load('Background\BG_leaderboard.png')
background_leaderboard = pygame.transform.scale(background_leaderboard, (screen_width,screen_height))

background_setting = pygame.image.load('Background\Setting.png')
background_setting = pygame.transform.scale(background_setting, (screen_width,screen_height))

# Màu sắc
WHITE = (255, 255, 255)
RED = (255, 99, 71)
RED_BALL = (255, 103, 95)
BLACK = (0,0,0)
YELLOW = (251, 204, 36)
GREEN_PD =(6, 142, 76)
YELLOW_TEXT=(248, 246, 223)
BLUE_WHITE = (191, 233, 255)
LIGHT_YELLOW = (242, 220, 168)

# Vận tốc và kích thước của thanh đỡ (paddle)
paddle_width = 15
paddle_height = 120
paddle_speed = 12

# Kích thước và vận tốc của bóng (Ball)
ball_size = 25
ball_radius = 15
ball_x = screen_width // 2 - ball_size // 2
ball_y = screen_height // 2 - ball_size // 2
ball_dx = random.choice([-4, 4])
ball_dy = random.choice([-4, 4])
ball_speed_increase_interval = 2500  # Tăng vận tốc bóng sau mỗi 2.5 giây
last_speed_increase_time = 0

# Tạo vị trí ban đầu cho các thanh đỡ (Paddle)
paddle1_y = screen_height // 2 - paddle_height // 2
paddle2_y = screen_height // 2 - paddle_height // 2

# Điểm số của người chơi
score1 = 0
score2 = 0

# Giới hạn điểm và thời gian
score_limit = 5
time_limit = 120 # Giới hạn thời gian 120 giây

# Khởi tạo thời gian
start_ticks = pygame.time.get_ticks()  # Lấy thời gian bắt đầu (mili-giây)

# Biến chế độ 
play_with_ai = False  # True nếu chơi với máy, False nếu chơi với người
setting = False 

# Hàm lưu điểm
def save_score(player1_score, player2_score, time):
    with open("Score\scores.txt", "a") as file:
        file.write(f"Player 1: {player1_score}, Player 2: {player2_score}, with: {time}s\n")

def display_leaderboard():
    button_back = pygame.Rect(10, 440, 97, 33)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_back.collidepoint(event.pos):
                    return
                
        screen.fill((0, 0, 0))  # Xóa màn hình (background đen)
        screen.blit(background_leaderboard, (0, 0))

        font = pygame.font.Font('Font\lazy_dog.ttf', 29)  # Tải font cho bảng điểm
        with open("Score\scores.txt", "r") as file:
            scores = file.readlines() 

        with open("Score\scores.txt", "w") as file:
            score = scores[-5:]
            file.writelines(score)

        # Hiển thị từng dòng điểm số
        score_text1 = font.render(scores[0].strip(), True, LIGHT_YELLOW)
        screen.blit(score_text1, (145, 130))
        score_text2 = font.render(scores[1].strip(), True, LIGHT_YELLOW)
        screen.blit(score_text2, (145, 183))
        score_text3 = font.render(scores[2].strip(), True, LIGHT_YELLOW)
        screen.blit(score_text3, (145, 235))
        score_text4 = font.render(scores[3].strip(), True, LIGHT_YELLOW)
        screen.blit(score_text4, (145, 290))
        score_text5 = font.render(scores[4].strip(), True, LIGHT_YELLOW)
        screen.blit(score_text5, (145, 345))
        
        # pygame.draw.rect(screen, BLACK, button_back)
        pygame.display.flip()  # Cập nhật màn hình

def display_setting():
    global setting
    global volume_music
    global time_limit
    global score_limit
    button_back = pygame.Rect(50, 430, 76, 27)
    button_subvolume = pygame.Rect(316,183,20,10)
    button_upvolume = pygame.Rect(420,183,15,18)
    button_subtime = pygame.Rect(316,230,20,10)
    button_uptime = pygame.Rect(419,230,15,18)
    button_subscore = pygame.Rect(316,280,20,10)
    button_upscore = pygame.Rect(419,280,15,18)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    setting = False
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_back.collidepoint(event.pos):
                    setting = False
                    return
                if button_subvolume.collidepoint(event.pos):
                    volume_music -= 10
                    if volume_music < 0:
                        volume_music = 0
                    pygame.mixer.music.set_volume(volume_music/100)
                if button_upvolume.collidepoint(event.pos):
                    volume_music += 10
                    if volume_music > 100:
                        volume_music = 100
                    pygame.mixer.music.set_volume(volume_music/100)
                if button_subtime.collidepoint(event.pos):
                    time_limit -= 10
                    if time_limit < 10:
                        time_limit = 10
                if button_uptime.collidepoint(event.pos):
                    time_limit += 10
                    if time_limit > 120:
                        time_limit = 120
                if button_upscore.collidepoint(event.pos):
                    score_limit += 1
                    if score_limit > 10:
                        score_limit = 10
                if button_subscore.collidepoint(event.pos):
                    score_limit -= 1
                    if score_limit < 1:
                        score_limit = 1
                
        screen.fill((0, 0, 0)) 
        screen.blit(background_setting, (0, 0))
        font = pygame.font.Font('Font\lazy_dog.ttf', 45)  # Tải font cho cài đặt
        volume_text = font.render(f"{volume_music}", True, BLACK)
        screen.blit(volume_text, (355, 170))
        
        time_text = font.render(f"{time_limit}", True,BLACK)
        screen.blit(time_text, (355, 220))
        
        point_text = font.render(f"{score_limit}", True,BLACK)
        screen.blit(point_text, (355,267))
        pygame.display.flip()

# Vòng lặp chính của game
running = True
game_over = False

# Thông số nút hình tròn
circle_center = (37, 446)  # Tâm của hình tròn
circle_radius = 25          # Bán kính nút

def display_menu():
    """Hiển thị giao diện chọn chế độ chơi."""
    global play_with_ai
    global running
    global start_ticks
    global setting
    button_rect1 = pygame.Rect(145, 160, 360, 60)
    button_rect2 = pygame.Rect(145, 257, 360, 60)
    button_rect3 = pygame.Rect(125, 365, 405, 51)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_2:
                    start_ticks = pygame.time.get_ticks()
                    play_with_ai = False  # Chọn chế độ chơi với người
                    return
                elif event.key == pygame.K_2:
                    start_ticks = pygame.time.get_ticks()
                    play_with_ai = True  # Chọn chế độ chơi với máy
                    return
                elif event.key == pygame.K_3:
                    # leaderboard_option = True
                    display_leaderboard()
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                distance = math.sqrt(
                (mouse_pos[0] - circle_center[0]) ** 2 + 
                (mouse_pos[1] - circle_center[1]) ** 2
                )
                if distance <= circle_radius:
                    display_setting()
                if button_rect1.collidepoint(event.pos):
                    start_ticks = pygame.time.get_ticks()
                    play_with_ai = False
                    return
                elif button_rect2.collidepoint(event.pos):
                    start_ticks = pygame.time.get_ticks()
                    play_with_ai = True
                    return
                elif button_rect3.collidepoint(event.pos):
                    display_leaderboard()
                    
        
        # Vẽ giao diện menu
        screen.fill((0, 0, 0))  # Màu nền đen
        screen.blit(background_mode, (0, 0))
        font = pygame.font.SysFont(None, 55)
        pygame.display.flip()

# Khởi tạo biến kiểm tra chạm
touch_oracle = False
touch_paddle1 = False
touch_paddle2 = False
saved = False
paused = False
# Gọi hàm hiển thị menu trước khi vào vòng lặp chính của game
display_menu()

while running:
    # Xử lý sự kiện
    # global pause
    pause_button = pygame.Rect(300, 72, 50, 48)
    menu_button = pygame.Rect(500,410,106,44)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                saved = False
                score1 = score2 = 0
                paddle1_y = paddle2_y = screen_height // 2 - paddle_height // 2
                ball_x = screen_width // 2 - ball_size // 2
                ball_y = screen_height // 2 - ball_size // 2
                ball_dx = random.choice([-4, 4])
                ball_dy = random.choice([-4, 4])
                start_ticks = pygame.time.get_ticks()
                game_over = False
                display_menu()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pause_button.collidepoint(event.pos):
                paused = not paused
        if game_over :
            # Lưu điểm trước khi reset
            if saved == False:
                save_score(score1,score2,seconds)
                saved = True
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if (menu_button.collidepoint(event.pos)):
                saved = False
                score1 = score2 = 0
                paddle1_y = paddle2_y = screen_height // 2 - paddle_height // 2
                ball_x = screen_width // 2 - ball_size // 2
                ball_y = screen_height // 2 - ball_size // 2
                ball_dx = random.choice([-4, 4])
                ball_dy = random.choice([-4, 4])
                start_ticks = pygame.time.get_ticks()
                game_over = False
                display_menu()
        
        
    if paused:
        # Hiển thị màn hình Pause
        pause_font = pygame.font.Font("Minecraft.ttf", 50)
        pause_text = pause_font.render("Game Paused", True, RED)
        screen.blit(pause_text, (screen_width // 2 - pause_text.get_width() // 2, screen_height // 2))

        # Cập nhật màn hình và tiếp tục vòng lặp
        pygame.display.flip()
        continue
        
    if not game_over: 
        # Điều khiển paddle1 (bên trái)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and paddle1_y > 0:
            paddle1_y -= paddle_speed
        if keys[pygame.K_s] and paddle1_y < screen_height - paddle_height:
            paddle1_y += paddle_speed

        # Điều khiển paddle2 (bên phải)
        if play_with_ai:
            # Điều khiển paddle2 (máy)
            if paddle2_y + paddle_height // 2 < ball_y and paddle2_y < screen_height - paddle_height:
                paddle2_y += paddle_speed
            if paddle2_y + paddle_height // 2 > ball_y and paddle2_y > 0:
                paddle2_y -= paddle_speed
        else:
            # Điều khiển paddle2 (người chơi)
            if keys[pygame.K_UP] and paddle2_y > 0:
                paddle2_y -= paddle_speed
            if keys[pygame.K_DOWN] and paddle2_y < screen_height - paddle_height:
                paddle2_y += paddle_speed

        # Cập nhật vị trí của bóng
        ball_x += ball_dx
        ball_y += ball_dy

        # Tăng vận tốc bóng sau mỗi 5 giây
        current_ticks = pygame.time.get_ticks()
        if current_ticks - last_speed_increase_time >= ball_speed_increase_interval:
            # Tăng vận tốc bóng
            ball_dx *= 1.2  
            ball_dy *= 1.2
            last_speed_increase_time = current_ticks

        # Kiểm tra va chạm với tường (trên và dưới)
        if ball_y <= 0 or ball_y >= screen_height - ball_size:
            ball_dy = -ball_dy
            touch_oracle = False
            touch_paddle1 = False
            touch_paddle2 = False
            
        # Tính toán thời gian đã trôi qua
        seconds = (pygame.time.get_ticks() - start_ticks) // 1000  # Đổi mili-giây thành giây

        # Kiểm tra va chạm với thanh đỡ
        if ball_x-15 <= 18 and paddle1_y <= ball_y <= paddle1_y + paddle_height and touch_paddle1 == False:
            ball_dx = -ball_dx
            touch_oracle=False
            touch_paddle1 = True
            touch_paddle2 = False
        elif ball_x >= 615 and paddle2_y <= ball_y <= paddle2_y + paddle_height and touch_paddle2 == False:
            ball_dx = -ball_dx
            touch_oracle = False
            touch_paddle2 = True
            touch_paddle1 = False
        # Kiểm tra va chạm với thanh đỡ (vật cản)
        if seconds >= (time_limit // 2):
            if 320 <= ball_x - 15 <= 345 and (165 <= ball_y - 15 <= 315 or 165 <= ball_y + 15 <= 315) and touch_oracle == False:
                ball_dx = -ball_dx
                touch_oracle = True
                touch_paddle1 = False
                touch_paddle2 = False
                
            elif 290 <= ball_x + 15 <= 320 and (165 <= ball_y - 15 <= 315 or 165 <= ball_y + 15 <= 315) and touch_oracle == False:
                ball_dx = -ball_dx
                touch_oracle = True
                touch_paddle2 = False
                touch_paddle1 = False

        # Kiểm tra nếu bóng ra khỏi màn hình (điểm cho người chơi)
        if ball_x < 0:
            score2 += 1
            ball_x = screen_width // 2 - ball_size // 2
            ball_y = screen_height // 2 - ball_size // 2
            ball_dx = random.choice([-4, 4])
            ball_dy = random.choice([-4, 4])
        if ball_x > screen_width:
            score1 += 1
            ball_x = screen_width // 2 - ball_size // 2
            ball_y = screen_height // 2 - ball_size // 2
            ball_dx = random.choice([-4, 4])
            ball_dy = random.choice([-4, 4])

        # Kiểm tra nếu một trong hai người chơi đạt đến giới hạn điểm
        if score1 == score_limit or score2 == score_limit:
            game_over = True

        # Kiểm tra nếu thời gian vượt quá giới hạn
        if seconds >= time_limit:
            game_over = True


        # Làm mới màn hình
        screen.blit(background, (0, 0))  # Vẽ hình nền lên màn hình

        # Vẽ thanh đỡ (paddle)
        pygame.draw.rect(screen, GREEN_PD, (0, paddle1_y, paddle_width, paddle_height))
        pygame.draw.rect(screen, WHITE, (screen_width - paddle_width, paddle2_y, paddle_width, paddle_height))
        # Kiểm tra nếu thời gian đã được một nửa thì tạo vật cản
        if seconds >= (time_limit // 2):
            pygame.draw.rect(screen, BLACK, (307, 162, 26, 156))
            pygame.draw.rect(screen, BLUE_WHITE, ((screen_width-20) // 2, (screen_height-150) // 2, 20, 150))

        # Vẽ bóng (ball)
        pygame.draw.circle(screen, BLACK, (ball_x, ball_y), ball_radius + 2)
        pygame.draw.circle(screen, RED_BALL, (ball_x, ball_y), ball_radius)

        # Hiển thị điểm số
        custom_font = pygame.font.Font("Font\Minecraft.ttf", 30)
        text1 = custom_font.render(f"{score1}", True, BLACK)
        text2 = custom_font.render(f"{score2}", True, YELLOW_TEXT)
        
        screen.blit(text1, (screen_width // 4 + 22, 38))
        screen.blit(text2, (screen_width * 3 // 4 - 33, 38))

        # Hiển thị thời gian đã trôi qua
        time_font = pygame.font.Font("Font\Minecraft.ttf", 30)
        time_text = time_font.render(f"Time: {seconds}", True, BLACK)
        screen.blit(time_text, (screen_width // 2 - 50, 34))
        

    else:
        # Hiển thị thông báo kết thúc game
        endgame_font = pygame.font.Font("Font\Minecraft.ttf", 30)
        endgame_font_border = pygame.font.Font("Font\Minecraft.ttf", 51)
        if score1 > score2:
            screen.blit(background_player1, (0, 0))
        elif score2 > score1 and play_with_ai == False:
            screen.blit(background_player2, (0, 0))
        elif score2 > score1 and play_with_ai == True:
            screen.blit(background_lose, (0, 0))
        else:
            screen.blit(background_draw, (0, 0))
        # pygame.draw.rect(screen, GREEN_PD, menu_button)
        
    # Cập nhật màn hình
    pygame.display.flip()

    # Đặt tốc độ khung hình (FPS)
    pygame.time.Clock().tick(60)

# Thoát game
pygame.mixer.music.stop()
pygame.quit()


