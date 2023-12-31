import sqlite3

import pygame
import pygame_menu
from pygame_menu import themes


# pygame.init()
# surface = pygame.display.set_mode((600, 400), pygame.RESIZABLE)

class Menu():
    def __init__(self):
        # super().__init__()
        pygame.init()
        surface = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
        pygame.display.set_caption("Starry rain")
        self.start_menu = pygame_menu.Menu(
            height=400,
            theme=pygame_menu.themes.THEME_BLUE,
            title='Welcome',
            width=600
        )

        self.start_menu.add.label('STARRY RAIN')
        self.start_menu.add.label(' ')
        # start_menu.add.text_input('Name: ', default='user123', maxchar=10)

        self.username = self.start_menu.add.text_input('Name: ', default=('user' + self.get_id()), maxchar=10)

        self.start_menu.add.button('Hot Keys', self.hot_keys)
        self.start_menu.add.button('Play', self.start_the_game)
        self.start_menu.add.button('Quit', pygame_menu.events.EXIT)
        self.start_menu.enable()
        self.on_resize()
        hot_menu = pygame_menu.Menu('Hot keys', 600, 400, theme=themes.THEME_BLUE)
        hot_menu.add.label(title='Esc - выход из игры')
        hot_menu.add.label(title='Пробел - пауза')
        loading = pygame_menu.Menu('Loading the Game...', 600, 400, theme=themes.THEME_DARK)
        loading.add.progress_bar("Progress", progressbar_id="1", default=0, width=200, )
        arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size=(10, 15))
        update_loading = pygame.USEREVENT + 0

    def start_the_game(self):
        self.start_menu._open(self.loading)
        pygame.time.set_timer(self.update_loading, 30)
        # name = username.get_value()  # имя

        self.name = self.username.get_value()

        connection = sqlite3.connect('starry_rain.sqlite')
        cursor = connection.cursor()
        result_id = cursor.execute("""SELECT id FROM top ORDER BY id DESC limit 1""").fetchall()
        id = result_id[0][0]
        cursor.execute("INSERT INTO top VALUES (?,?,?)", (id + 1, self.name, ''))

        connection.commit()
        connection.close()

    def get_id(self):
        connection = sqlite3.connect('starry_rain.sqlite')
        cursor = connection.cursor()
        result_id = cursor.execute("""SELECT id FROM top ORDER BY id DESC limit 1""").fetchall()
        id = result_id[0][0]

        connection.commit()
        connection.close()
        return (id)

    def hot_keys(self):
        self.start_menu._open(self.hot_menu)

    def on_resize(self):
        window_size = surface.get_size()
        new_w, new_h = window_size[0], window_size[1]
        self.start_menu.resize(new_w, new_h)



# pygame.display.set_caption("Starry rain")
# start_menu = pygame_menu.Menu(
#     height=400,
#     theme=pygame_menu.themes.THEME_BLUE,
#     title='Welcome',
#     width=600
# )
#
# start_menu.add.label('STARRY RAIN')
# start_menu.add.label(' ')
# # start_menu.add.text_input('Name: ', default='user123', maxchar=10)
#
# username = start_menu.add.text_input('Name: ', default=('user' + get_id()), maxchar=10)
#
# start_menu.add.button('Hot Keys', hot_keys)
# start_menu.add.button('Play', start_the_game)
# start_menu.add.button('Quit', pygame_menu.events.EXIT)
# start_menu.enable()
# on_resize()
# hot_menu = pygame_menu.Menu('Hot keys', 600, 400, theme=themes.THEME_BLUE)
# hot_menu.add.label(title='Esc - выход из игры')
# hot_menu.add.label(title='Пробел - пауза')
# loading = pygame_menu.Menu('Loading the Game...', 600, 400, theme=themes.THEME_DARK)
# loading.add.progress_bar("Progress", progressbar_id="1", default=0, width=200, )
# arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size=(10, 15))
# update_loading = pygame.USEREVENT + 0
fl = True
if __name__ == '__main__':
    while fl:
        events = pygame.event.get()
        for event in events:
            if event.type == update_loading:
                progress = loading.get_widget("1")
                progress.set_value(progress.get_value() + 1)
                if progress.get_value() == 100:
                    pygame.time.set_timer(update_loading, 0)
            if event.type == pygame.QUIT:
                fl = False
                # pygame.quit()
                # break
            if event.type == pygame.VIDEORESIZE:
                surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                self.on_resize()
        if start_menu.is_enabled():
            start_menu.update(events)
            start_menu.draw(surface)
            if start_menu.get_current().get_selected_widget():
                arrow.draw(surface, start_menu.get_current().get_selected_widget())
        surface.fill((25, 0, 50))
        start_menu.update(events)
        start_menu.draw(surface)

        pygame.display.flip()
