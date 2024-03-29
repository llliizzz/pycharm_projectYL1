import sqlite3

import pygame

import pygame_menu
from pygame_menu import themes

def startScreen():
    pygame.init()
    surface = pygame.display.set_mode((600, 500), pygame.RESIZABLE)
    pygame.display.set_caption("Starry rain")
    start_menu = pygame_menu.Menu(
        height=500,
        theme=pygame_menu.themes.THEME_BLUE,
        title='Welcome',
        width=600
    )

    class Menu:
        def __init__(self):
            start_menu.add.label('STARRY RAIN')
            start_menu.add.label(' ')
            self.username = start_menu.add.text_input('Name: ', default=(f"user{self.get_id() + 1}"), maxchar=10)
            start_menu.add.button('Hot Keys', self.hot_keys)
            start_menu.add.selector('Difficulty :', [('Easy', 1), ('Normal', 2), ('Hard', 3)],
                                    onchange=self.set_difficulty)
            start_menu.add.button('Play', self.start_the_game)
            start_menu.add.button('Quit', pygame_menu.events.EXIT)
            start_menu.enable()

            self.on_resize()

            global hot_menu
            hot_menu = pygame_menu.Menu('Hot keys', 600, 500, theme=themes.THEME_BLUE)
            hot_menu.add.label(title='Esc - выход из игры')
            hot_menu.add.label(title='Пробел - пауза')

            global loading
            loading = pygame_menu.Menu('Loading the Game...', 600, 500, theme=themes.THEME_DARK)
            loading.add.progress_bar("Progress", progressbar_id="1", default=0, width=200, )

            global arrow
            arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size=(10, 15))

        def start_the_game(self):
            start_menu._open(loading)
            pygame.time.set_timer(update_loading, 30)

            self.name = self.username.get_value()

            id1 = self.get_id()

            connection = sqlite3.connect('starry_rain1.sqlite')
            cursor = connection.cursor()

            cursor.execute("INSERT INTO top VALUES (?,?,?)", (id1 + 1, self.name, 0))

            connection.commit()
            connection.close()

        def set_difficulty(self, value, difficulty):
            print(value)
            print(difficulty)

        def hot_keys(self):
            start_menu._open(hot_menu)

        def on_resize(self):
            window_size = surface.get_size()
            new_w, new_h = window_size[0], window_size[1]
            start_menu.resize(new_w, new_h)

        def get_id(self):
            connection = sqlite3.connect('starry_rain1.sqlite')
            cursor = connection.cursor()
            connection.commit()
            cursor.execute("CREATE TABLE IF NOT EXISTS 'top' (id INTEGER, Username TEXT, Balls INTEGER)")
            connection.commit()
            result_id = cursor.execute("""SELECT id FROM top ORDER BY id DESC limit 1""").fetchall()
            id1 = result_id[0][0]
            return (id1)

    fl = True
    update_loading = pygame.USEREVENT + 0
    Menu()
    # start_menu.mainloop(surface)
    while fl:
        events = pygame.event.get()
        for event in events:
            if event.type == update_loading:
                progress = loading.get_widget("1")
                progress.set_value(progress.get_value() + 1)
                if progress.get_value() == 100:
                    pygame.time.set_timer(update_loading, 0)

                    connection = sqlite3.connect('starry_rain1.sqlite')
                    cursor = connection.cursor()

                    prev_id = cursor.execute("""SELECT id FROM LastState ORDER BY id DESC limit 1""").fetchall()
                    id1 = prev_id[0][0]
                    cursor.execute("INSERT INTO LastState (id, State) VALUES (?, ?)", (id1 + 1, 'GAME'))

                    connection.commit()
                    connection.close()
                    fl = False
                    from new_3 import game
                    game()
            if event.type == pygame.QUIT:
                connection = sqlite3.connect('starry_rain1.sqlite')
                cursor = connection.cursor()

                prev_id = cursor.execute("""SELECT id FROM LastState ORDER BY id DESC limit 1""").fetchall()
                id1 = prev_id[0][0]
                cursor.execute("INSERT INTO LastState (id, State) VALUES (?, ?)", (id1 + 1, 'EXIT'))

                connection.commit()
                connection.close()
                fl = False
            # if event.type == pygame.VIDEORESIZE:
            #     surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            #     Menu.on_resize(Menu)
        # if start_menu.is_enabled():
        #     start_menu.update(events)
        #     start_menu.draw(surface)
        #     if start_menu.get_current().get_selected_widget():
        #         arrow.draw(surface, start_menu.get_current().get_selected_widget())
        surface.fill((25, 0, 50))
        start_menu.update(events)
        start_menu.draw(surface)
        pygame.display.flip()


startScreen()