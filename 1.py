import os
import sys
from geocoder import get_coordinates, geocode
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
screen = pygame.display.set_mode((600, 600))
input_box = pygame.Rect(0, 450, 600, 150)
screen.blit(pygame.image.load(map_file), (0, 0))
color_inactive = pygame.Color('white')
color_active = pygame.Color('red')
color = color_inactive
running = True
active = False
font = pygame.font.Font(None, 32)
text = ''
while running:

    screen.fill((0, 0, 0))
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
            if active:
                if event.key == pygame.K_RETURN:
                    active = False

                    parms['ll'] = str(int(get_coordinates(text)[0])) + ',' + str(int(get_coordinates(text)[1]))
                    parms['pt'] = parms['ll'] + ',flag'

                    text = geocode(text)['metaDataProperty']['GeocoderMetaData']['Address']['formatted']
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    if len(text) < 20:
                        text += event.unicode
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
            if event.key == pygame.K_KP1:
                parms['l'] = 'map'
            if event.key == pygame.K_KP2:
                parms['l'] = 'sat'
            if event.key == pygame.K_KP3:
                parms['l'] = 'sat,skl'
            if event.key == pygame.K_TAB:
                parms['pt'] = ''
                text = ''
        if event.type == pygame.MOUSEBUTTONDOWN:

            if input_box.collidepoint(event.pos):

                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
    txt_surface = font.render(text, True, color)
    screen.blit(txt_surface, (input_box.x + 10, input_box.y + 10))

    pygame.draw.rect(screen, color, input_box, 2)
    pygame.display.flip()
pygame.quit()
os.remove(map_file)
#
