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
		title = Label(text="Welcome to Wordle", font_size = '40sp', bold = True)
		btn = Button(text="Start", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
		btn.bind(on_press=self.start_game)
		layout.add_widget(title)
		layout.add_widget(btn)
		self.add_widget(layout)
	
	def start_game(self, instance):
		self.manager.current = "game" # Set the current screen of the ScreenManager to "game" (this screen should exist in the ScreenManager).

class GameScreen(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		grid = MyGridLayout(size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
		self.add_widget(grid)

class WordleApp(App):
	def build(self):
		sm = ScreenManager(transition=FadeTransition()) # Create a ScreenManager with a fade transition effect between screens.
		sm.add_widget(MainMenuScreen(name='menu')) # Add the MainMenuScreen to the ScreenManager and assign it the name 'menu'.
		sm.add_widget(GameScreen(name ='game'))
		return sm


if __name__ == '__main__':
	WordleApp().run()