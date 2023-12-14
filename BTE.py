import pygame
import sys

# Pygame 초기화 및 폰트 설정
pygame.init()
screen = pygame.display.set_mode((900, 800))
pygame.font.init()
font = pygame.font.SysFont(None, 26)
large_font = pygame.font.SysFont(None, 40)

# 이미지 로드
menu_background_image = pygame.image.load('C:/Users/USER/Desktop/GameProgrammingEngine/bullet_image.jpg')  
menu_background_rect = menu_background_image.get_rect()
menu_background_image = pygame.transform.scale(menu_background_image, (600, 300))
# 이미지 위치 설정 (화면 상단 중앙)
menu_background_rect = menu_background_image.get_rect()
menu_background_rect.top = 0  # 상단에 위치
menu_background_rect.centerx = screen.get_rect().centerx  # 가로 중앙 정렬
# 색상
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

class Bullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 5)
        self.speed = 0
        self.mass = 1
        self.energy = 0
        self.active = False
        self.energy_loss_per_hit = 10

    def update(self, targets):
        if self.active:
            self.rect.x += self.speed
            for target in targets:
                if self.rect.colliderect(target.rect) and not target.hit:
                    target.hit = True
                    target.pass_through_energy = self.energy  # 현재 에너지를 타겟에 기록
                    self.energy -= self.energy_loss_per_hit
                    if self.energy <= 0:
                        self.active = False
                        break

    def draw(self):
        if self.active:
            pygame.draw.rect(screen, RED, self.rect)

    def reset(self, speed, mass, energy_loss):
        self.speed = speed
        self.mass = mass
        self.energy = 0.5 * mass * speed**2
        self.energy_loss_per_hit = energy_loss
        self.rect.x = 0
        self.active = True

    def reset_for_power_test(self, speed, mass, energy_loss, distance):
        self.speed = speed
        self.mass = mass
        self.energy = 0.5 * mass * speed ** 2
        self.energy_loss_per_hit = energy_loss
        self.target_distance = distance
        self.rect.x = 0
        self.active = True

    def update_for_power_test(self, targets):
        if self.active:
            self.rect.x += self.speed
            for target in targets:
                if self.rect.colliderect(target.rect) and not target.hit:
                    target.hit = True
                    target.pass_through_energy = self.energy
                    self.energy -= self.energy_loss_per_hit
                    if self.energy <= 0 or self.rect.x >= self.target_distance:
                        self.active = False
                        break
            return target.pass_through_energy if target.hit else None
        return None


class Target:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.hit = False
        self.pass_through_energy = 0  # 총알이 관통했을 때의 에너지

    def draw(self):
        color = GREEN if not self.hit else RED
        pygame.draw.rect(screen, color, self.rect)
        if self.hit:
            energy_text = font.render(f"{self.pass_through_energy:.2f}", True, WHITE)
            screen.blit(energy_text, (self.rect.x + 5, self.rect.y - 15))

class InputBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = ""
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        text_surf = font.render(self.text, True, WHITE)
        screen.blit(text_surf, (self.rect.x + 5, self.rect.y + 5))

    def get_text(self):
        return self.text

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)




# 메뉴 버튼 생성
menu_button = Button(350, 400, 200, 50, "Bullet Penetration Test")
menu_button_power = Button(350, 480, 200, 50, "Power Test by Distance")

# 게임 상태 변수
MENU = 0
GAME = 1
POWER_TEST = 2
game_state = MENU


# 메뉴 화면 렌더링 함수
def draw_menu():
        # 배경 이미지 블리팅
    screen.blit(menu_background_image, menu_background_rect)

    screen.fill(BLACK)
    menu_button.draw()
    menu_button_power.draw()
    large_text_surface = large_font.render("Bullet Testing Engine", True, WHITE)
    large_text_rect = large_text_surface.get_rect(center=(450, 340))  # 화면 중앙에 위치하도록 조정
    screen.blit(large_text_surface, large_text_rect)
    screen.blit(menu_background_image, menu_background_rect)

    pygame.display.flip()
 # Power Test 렌더링 함수
def draw_power_test():
    screen.fill(BLACK)
    input_box_distance.draw()
    input_box_resistance.draw()
    fire_button_power.draw()
    target_power_test.draw()
    pygame.display.flip()   



# 텍스트 렌더링 함수
def draw_text(text, position):
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, position)

# 총알, 입력 상자, 버튼 생성 (Penetration Test용)
bullet = Bullet(0, 450)
input_box_speed = InputBox(720, 30, 140, 40)
input_box_mass = InputBox(720, 80, 140, 40)
input_box_energy_loss = InputBox(720, 130, 140, 40)
input_box_targets = InputBox(720, 180, 140, 40)
fire_button = Button(720, 230, 140, 40, "Fire")
targets = []
# (Power Test용 버튼)
input_box_distance = InputBox(720, 30, 140, 40)
input_box_resistance = InputBox(720, 80, 140, 40)
fire_button_power = Button(720, 130, 140, 40, "Fire")
target_power_test = Target(450, 400, 50, 100)



def calculate_energy(distance, resistance):
    """ 거리와 저항값에 따라 총알의 에너지를 계산 """
    initial_energy = 100  # 초기 에너지 값
    energy_loss_rate = resistance  # 저항값에 따른 에너지 손실 비율
    final_energy = initial_energy - (energy_loss_rate * distance)
    return max(final_energy, 0)  # 에너지가 0 미만이 되지 않도록




def draw_power_test(calculated_energy=None):
    screen.fill(BLACK)
    
    # 입력 상자와 레이블
    draw_text("Distance:", (620, 35))
    input_box_distance.draw()
    draw_text("Resistance:", (600, 85))
    input_box_resistance.draw()
    fire_button_power.draw()

    # 타겟과 거리 표시
    target_power_test.draw()
    if input_box_distance.get_text():
        distance_text = font.render(input_box_distance.get_text(), True, WHITE)
        screen.blit(distance_text, (target_power_test.rect.x, target_power_test.rect.y - 20))

    # 계산된 에너지 출력
    if calculated_energy is not None:
        energy_text = font.render(f"Energy: {calculated_energy:.2f}", True, WHITE)
        screen.blit(energy_text, (10, 10))

    pygame.display.flip()




# 게임 루프
running = True
calculated_energy = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if game_state == MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.is_clicked(event.pos):
                    game_state = GAME
                elif menu_button_power.is_clicked(event.pos):
                    game_state = POWER_TEST


###### Bullet Penetration test #######
        elif game_state == GAME:
            input_box_speed.handle_event(event)
            input_box_mass.handle_event(event)
            input_box_energy_loss.handle_event(event)
            input_box_targets.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if fire_button.is_clicked(event.pos):
                    try:
                        bullet_speed = float(input_box_speed.get_text())
                        bullet_mass = float(input_box_mass.get_text())
                        energy_loss = float(input_box_energy_loss.get_text())
                        num_targets = int(input_box_targets.get_text())

                        target_width = 50
                        target_height = 100
                        margin = 10
                        targets.clear()
                        for i in range(num_targets):
                            x = 100 + (target_width + margin) * (i % 10)
                            y = 400 + (target_height + margin) * (i // 10)
                            targets.append(Target(x, y, target_width, target_height))
                            for target in targets:
                                target.hit = False

                        bullet.reset(bullet_speed, bullet_mass, energy_loss)
                    except ValueError:
                        pass
########################################

###### Bullet Distance Test ######
        elif game_state == POWER_TEST:
            input_box_distance.handle_event(event)
            input_box_resistance.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
                if fire_button_power.is_clicked(event.pos):
                    try:
                        distance = float(input_box_distance.get_text())
                        resistance = float(input_box_resistance.get_text())
                        bullet_speed = 10
                        bullet_mass = 1
                        calculated_energy = calculate_energy(distance, resistance)
                        print(f"Calculated Energy: {calculated_energy}")  # 콘솔에 에너지 출력
                    except ValueError:
                        # 입력값 오류 처리
                        print("Invalid input") 

######################################

    if game_state == MENU:
        draw_menu()
    elif game_state == GAME:
        # 게임 업데이트 및 렌더링
        screen.fill(BLACK)
        bullet.update(targets)
        bullet.draw()
        for target in targets:
            target.draw()
        input_box_speed.draw()
        input_box_mass.draw()
        input_box_energy_loss.draw()
        input_box_targets.draw()
        fire_button.draw()
         # 입력 상자 옆에 텍스트 추가
        draw_text("Bullet Speed:", (605, 35))
        draw_text("Bullet Mass:", (610, 85))
        draw_text("Targets Armor:", (590, 135))
        draw_text("Targets Number:", (578, 185))        

        hit_targets = len([target for target in targets if target.hit])
        status_text = font.render(f"Hit Targets: {hit_targets}, Energy: {bullet.energy:.2f}", True, WHITE)
        screen.blit(status_text, (10, 10))

        pygame.display.flip()

    if game_state == POWER_TEST:
        # 입력 상자 및 버튼 이벤트 처리
        input_box_distance.handle_event(event)
        input_box_resistance.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if fire_button_power.is_clicked(event.pos):
                try:
                    distance = float(input_box_distance.get_text())
                    resistance = float(input_box_resistance.get_text())
                    calculated_energy = calculate_energy(distance, resistance)
                except ValueError:
                    calculated_energy = "Invalid input"

    if game_state == POWER_TEST:
        draw_power_test(calculated_energy)

    pygame.time.Clock().tick(60)
