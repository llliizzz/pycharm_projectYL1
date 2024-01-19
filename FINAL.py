import pygame

import pygame_menu
from pygame_menu import themes

import sqlite3


def finalScreen():
    pygame.init()
    surface = pygame.display.set_mode((600, 500), pygame.RESIZABLE)
    pygame.display.set_caption("Final")
    final_menu = pygame_menu.Menu(
        height=500,
        theme=pygame_menu.themes.THEME_BLUE,
        title='GAME OVER',
        width=600
    )

    class FinalScreen:
        def __init__(self):
            final_menu.add.label('Rating of players:')
            final_menu.add.label(' ')

            self.show_result()

            final_menu.add.button('Try again', self.zanovo)
            final_menu.add.button('Quit', pygame_menu.events.EXIT)
            final_menu.enable()

            self.on_resize()

            global arrow
            arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size=(10, 15))

        def show_result(self):
            connection = sqlite3.connect('starry_rain1.sqlite')
            cursor = connection.cursor()

            cursor.execute("CREATE TABLE IF NOT EXISTS 'top' (id INTEGER, Username TEXT, Balls INTEGER)")

            result = cursor.execute("""SELECT id, Username, Balls FROM top ORDER BY balls DESC limit 3""").fetchall()
            # cursor.execute(f'UPDATE pupils SET balls_test2={self.balls_2} WHERE id={id}')
            connection.commit()
            result_id = cursor.execute("""SELECT id FROM top ORDER BY id DESC limit 1""").fetchall()
            id_last = result_id[0][0]
            #print(result_id)
            connection.commit()
            connection.close()

            fl = True
            for triple in result:
                if triple[0] == id_last:
                    fl = False  # т е последний юзер встречается в тройке лидеров, отдельно не выводим
                    break
            if fl:
                # вывести это 3 тройки на экран(result) + последний результат(last_result)
                connection = sqlite3.connect('starry_rain1.sqlite')
                cursor = connection.cursor()
                final_menu.add.label(f'1: {result[0][1]} - {result[0][2]} points')
                final_menu.add.label(f'2: {result[1][1]} - {result[1][2]} points')
                final_menu.add.label(f'3: {result[2][1]} - {result[2][2]} points')
                # print(result)
                final_menu.add.label('. . .')
                last_result = cursor.execute(f"SELECT id, Username, Balls FROM top WHERE id = {id_last}").fetchall()
                #print(last_result)
                final_menu.add.label(f'Your: {last_result[0][1]} - {last_result[0][2]} points')
                connection.commit()
                connection.close()
            else:
                final_menu.add.label(f'1: {result[0][1]} - {result[0][2]} points')
                final_menu.add.label(f'2: {result[1][1]} - {result[1][2]} points')
                final_menu.add.label(f'3: {result[2][1]} - {result[2][2]} points')

        def zanovo(self):
            from STARTFILE import startScreen
            startScreen()

        def on_resize(self):
            window_size = surface.get_size()
            new_w, new_h = window_size[0], window_size[1]
            final_menu.resize(new_w, new_h)

    fl = True
    update_loading = pygame.USEREVENT + 0
    FinalScreen()
    while fl:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                fl = False
            if event.type == pygame.VIDEORESIZE:
                surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                # FinalScreen.on_resize()
        if final_menu.is_enabled():
            final_menu.update(events)
            final_menu.draw(surface)
            if final_menu.get_current().get_selected_widget():
                arrow.draw(surface, final_menu.get_current().get_selected_widget())
        surface.fill((25, 0, 50))
        final_menu.update(events)
        final_menu.draw(surface)
        pygame.display.flip()


finalScreen()
