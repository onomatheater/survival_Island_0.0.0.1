import pygame
import time

# Инициализация pygame
pygame.init()
done = False

# Установим параметры экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Survival Island")

# Загружаем шрифты
font = pygame.font.Font('fonts/EpilepsySans.ttf', 32)
input_font = pygame.font.Font("fonts/EpilepsySans.ttf", 24)

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Частота кадров
FPS = 60
clock = pygame.time.Clock()

# Сообщения для отображения
messages = [
    "- Hello, World!",
    "- Good evening!",
    "- Good night!",
]

# Переменные для текста
current_message = 0
current_text = ""
char_index = 0
word_delay = 75  # Задержка между словами (мс)
char_delay = 50  # Задержка между буквами (мс)
last_update_time = pygame.time.get_ticks()

# Список строк, которые должны отобразиться
text_lines = []

# Таймеры для угасания старых сообщений
fade_timers = []

# Переменные для ввода текста
input_active = False
user_input = ""
input_rect = pygame.Rect(50, HEIGHT - 40, WIDTH - 100, 32)

# Основной цикл
while not done:
    # Заполняем экран черным цветом
    screen.fill(BLACK)

    # Проверка на закрытие игры
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True
        if event.type == pygame.KEYDOWN and input_active:
            if event.key == pygame.K_RETURN:  # При нажатии Enter подтверждаем ввод
                print(f"User input: {user_input}")  # Выводим введенный текст
                text_lines.append(f"> {user_input}")
                fade_timers.append(pygame.time.get_ticks())  # Начинаем таймер угасания
                user_input = ""  # Очищаем поле ввода
                input_active = False
            elif event.key == pygame.K_BACKSPACE:  # При нажатии Backspace удаляем символ
                user_input = user_input[:-1]
            else:
                user_input += event.unicode  # Добавляем символ в строку ввода

    # Логика отображения текста
    current_time = pygame.time.get_ticks()
    if current_message < len(messages):
        if char_index < len(messages[current_message]):
            if current_time - last_update_time > (char_delay if messages[current_message][char_index] != "-" else word_delay):
                current_text += messages[current_message][char_index]
                char_index += 1
                last_update_time = current_time
        else:
            pygame.time.wait(100)  # Задержка перед следующим сообщением
            text_lines.append(current_text)
            fade_timers.append(current_time)  # Добавляем таймер угасания
            current_message += 1
            current_text = ""  # Очищаем текущий текст для следующего сообщения
            char_index = 0

    # Отображаем текст, смещая его вверх
    y_offset = HEIGHT - 80 - len(text_lines)  # Начальная позиция для отображения (учитывая место для ввода)
    for i, line in enumerate(text_lines):
        # Определяем, насколько старое сообщение должно исчезать
        fade_time = current_time - fade_timers[i]
        alpha = 255
        if fade_time > 5000:  # Если прошло более 5 секунд
            alpha = max(0, 255 - (fade_time - 5000) // 10)  # Плавно исчезает

        rendered_text = font.render(line, True, WHITE)
        rendered_text.set_alpha(alpha)  # Применяем прозрачность
        screen.blit(rendered_text, (50, y_offset))
        y_offset += 40  # Смещаем на высоту строки

    # Поле ввода всегда внизу
    if input_active:
        # Отображаем подсказку
        prompt_text = font.render(" > ", True, GREEN)
        screen.blit(prompt_text, (50, HEIGHT - 40))

        # Отображаем введенный текст
        user_input_text = input_font.render(user_input, True, GREEN)
        screen.blit(user_input_text, (input_rect.x + 40, input_rect.y))

        # Отображаем прямоугольник для поля ввода
        pygame.draw.rect(screen, WHITE, input_rect, 2)

    pygame.display.flip()  # Обновляем экран
    clock.tick(FPS)  # Ограничиваем частоту кадро
