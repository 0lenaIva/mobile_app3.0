from kivy.app import App
from kivy.uix.screenmanager import(
    Screen,
    ScreenManager
)
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.uix.image import Image
from kivy.clock import Clock#таймер для відкладання виклику функцій
from kivy import platform# визначення платформи

Builder.load_file('medium.kv')

class Menu(Screen):
    def go_game(self):
        self.manager.current = 'game'
        self.manager.transition.direction = 'left'

    def go_settings(self):
        self.manager.current = 'settings'
        self.manager.transition.direction = 'up'

    def exit_app(self):
        App.get_running_app().stop()

class Settings(Screen):
    def go_menu(self):
        self.manager.current = 'menu'
        self.manager.transition.direction = 'down'

class Fish(Image):
    fish_current = None # вид риби
    fish_index = 0
    hp_fish = 0

    def new_fish(self):
        app = App.get_running_app()# силка на додаток
        self.fish_current = app.LEVELS[app.LEVEL][self.fish_index]#витягнути назву риби
        self.source = app.FISHES[self.fish_current]['source']
        self.hp_fish = app.FISHES[self.fish_current]['hp']
        self.opacity = 1

    def defeated(self):
        self.opacity = 0

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return super().on_touch_down(touch)
        if self.opacity == 0:
            return super().on_touch_down(touch)
        
        app = App.get_running_app()
        self.hp_fish -= 1
        game_screen = self.parent
        while game_screen and not isinstance(game_screen, Game):
            game_screen = game_screen.parent

        if game_screen:
            game_screen.score += 1
        
        if self.hp_fish <= 0:
            self.defeated()
            if len(app.LEVELS[app.LEVEL]) > self.fish_index + 1:
                self.fish_index += 1
                Clock.schedule_once(self.new_fish, 1.2)
                #через 1.2с створити нову рибу
            else:
                if game_screen:
                    Clock.schedule_once(game_screen.level_complete, 1.2)
                self.fish_index = 0
        return super().on_touch_down(touch)
    
class Game(Screen):
    score = NumericProperty(0)
    
    def on_pre_enter(self, *args):#викликається перед входом на екран
        self.score=0
        app = App.get_running_app()
        app.LEVEL = 0
        self.ids.level_complete.opacity = 0
        self.ids.fish.fish_index = 0
        return super().on_pre_enter(*args)
    
    def on_enter(self, *args):#викликається після відкриття екрану
        self.start_game()
        return super().on_enter(*args)

    def start_game(self):
        self.ids.fish.new_fish()
    
    def level_complete(self, *args):
        self.ids.level_complete.opacity = 1

    def go_home(self):
        self.manager.current = 'menu'
        self.manager.transition.direction = 'right'

class MediumApp(App):
    LEVEL = 0

    FISHES = {
        "fish1":{
            "source":"fish1.png",
            "hp": 10
        },
        "fish2":{
            "source":"fish2.png",
            "hp": 20
        }
    }

    LEVELS = [
        ["fish1", "fish1", "fish2"]
    ]

    def build(self):
        sm = ScreenManager()
        sm.add_widget(Menu(name='menu'))
        sm.add_widget(Game(name='game'))
        sm.add_widget(Settings(name='settings'))
        return sm

if platform!= 'android':
    Window.size = (450,700)
if __name__ == '__main__':
    MediumApp().run()
