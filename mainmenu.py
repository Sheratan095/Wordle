from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '340')
Config.set('graphics', 'height', '405')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from app import MyGridLayout

# Define a screen for the main menu that inherits from Kivy's Screen class.
class MainMenuScreen(Screen):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		layout = BoxLayout(orientation = 'vertical', spacing = 20, padding = 50)
		title = Label(text="Welcome to Wordle", font_size = '28sp', bold = True)
		btn = Button(text="Start", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
		btn.bind(on_press=self.start_game)
		layout.add_widget(title)
		layout.add_widget(btn)
		self.add_widget(layout)
	
	def set_gamescreen(self, gamescreen):
		self.gamescreen = gamescreen
	
	def start_game(self, instance):
		self.manager.current = "game" # Set the current screen of the ScreenManager to "game" (this screen should exist in the ScreenManager).s
		self.gamescreen.start_game() # Call the start_game method of the GameScreen instance to initialize the game.

class GameScreen(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.grid = MyGridLayout()
		self.add_widget(self.grid)

	def start_game(self):
		self.grid.start_game()
		print("starting")


class VictoryScreen(Screen):
	def __init__(self, gamescreen, **kwargs):
		super().__init__(**kwargs)
		layout = BoxLayout(orientation = 'vertical', spacing = 20, padding = 50)
		title = Label(text="You win!", font_size = '28sp', bold = True)
		btn = Button(text="Restart", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
		btn.bind(on_press=self.start_game)
		layout.add_widget(title)
		layout.add_widget(btn)
		self.add_widget(layout)
		self.gamescreen = gamescreen

	def start_game(self, instance):
		self.manager.current = "game" # Set the current screen of the ScreenManager to "game" (this screen should exist in the ScreenManager).s
		self.gamescreen.start_game()

class DefeatScreen(Screen):
	def __init__(self,  gamescreen, **kwargs):
		super().__init__(**kwargs)
		layout = BoxLayout(orientation = 'vertical', spacing = 20, padding = 50)
		title = Label(text="Game over :(", font_size = '28sp', bold = True)
		btn = Button(text="Restart", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
		btn.bind(on_press=self.restart_game)
		layout.add_widget(title)
		layout.add_widget(btn)
		self.add_widget(layout)
		self.gamescreen = gamescreen

	def restart_game(self, instance):
		self.manager.current = "game"
		self.gamescreen.start_game()

class WordleApp(App):
	def build(self):
		sm = ScreenManager(transition=FadeTransition()) # Create a ScreenManager with a fade transition effect between screens.

		mainMenù = MainMenuScreen(name ='menu')
		sm.add_widget(mainMenù) # Add the MainMenuScreen to the ScreenManager and assign it the name 'menu'.

		gamescreen = GameScreen(name = 'game')
		sm.add_widget(gamescreen)

		mainMenù.set_gamescreen(gamescreen)

		sm.add_widget(VictoryScreen(gamescreen, name = 'victory'))
		sm.add_widget(DefeatScreen(gamescreen, name = 'defeat'))
		return sm


if __name__ == '__main__':
	WordleApp().run()