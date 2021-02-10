import os
import sys

import pygame
import requests

map_request = "http://static-maps.yandex.ru/1.x/"
parms = {
    'll': '135,-25',
    'z': '4',
    'l': 'map'
}
response = requests.get(map_request, params=parms)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

# Запишем полученное изображение в файл.
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))

screen.blit(pygame.image.load(map_file), (0, 0))

running = True

while running:

    screen.blit(pygame.image.load(map_file), (0, 0))
    response = requests.get(map_request, params=parms)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            delta = (18 - int(parms['z'])) // 2
            print(parms['z'], delta)
            if event.key == pygame.K_PAGEUP and int(parms['z']) < 22:
                parms['z'] = str(int(parms['z']) + 1)
            if event.key == pygame.K_PAGEDOWN and 0 < int(parms['z']):
                parms['z'] = str(int(parms['z']) - 1)
            if event.key == pygame.K_LEFT:

                if int(parms['ll'].split(',')[0]) - delta > -180:
                    parms['ll'] = str(int(parms['ll'].split(',')[0]) - delta) + ',' + parms['ll'].split(',')[1]
            if event.key == pygame.K_RIGHT:

                if int(parms['ll'].split(',')[0]) + delta < 180:
                    parms['ll'] = str(int(parms['ll'].split(',')[0]) + delta) + ',' + parms['ll'].split(',')[1]
            if event.key == pygame.K_UP:
                if int(parms['ll'].split(',')[1]) + delta < 90:
                    parms['ll'] = parms['ll'].split(',')[0] + ',' + str((int(parms['ll'].split(',')[1]) + delta))
            if event.key == pygame.K_DOWN:
                if int(parms['ll'].split(',')[1]) - delta > -90:
                    parms['ll'] = parms['ll'].split(',')[0] + ',' + str((int(parms['ll'].split(',')[1]) - delta))
    pygame.display.flip()
pygame.quit()
os.remove(map_file)
