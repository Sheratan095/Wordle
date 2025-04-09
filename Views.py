from GridLayout import MyGridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window


# Define a screen for the main menu that inherits from Kivy's Screen class.
# Starting page
class MainMenuScreen(Screen):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		layout = BoxLayout(orientation = 'vertical', spacing = 20, padding = 50)

		title = Label(text="Welcome to Wordle", font_size = '28sp', bold = True)
		layout.add_widget(title)


		btn = Button(text="Start", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
		btn.bind(on_press=self.start_game)
		layout.add_widget(btn)

		self.add_widget(layout)

		Window.bind(on_key_down=self.on_key_down)
	
	def on_key_down(self, window, key, scancode, codepoint, modifiers):
		if (key == 13):
			self.start_game(None)

	def set_gamescreen(self, gamescreen):
		self.gamescreen = gamescreen
	
	def start_game(self, instance):

		# Set the current screen of the ScreenManager to "game" (this screen should exist in the ScreenManager)
		self.manager.current = "game"

		# Call the start_game method of the GameScreen instance to initialize the game.
		self.gamescreen.start_game()

		Window.unbind(on_key_down=self.on_key_down)


class GameScreen(Screen):

	def __init__(self, dictionary, **kwargs):
		super().__init__(**kwargs)

		self.grid = MyGridLayout(dictionary)
		self.add_widget(self.grid)

		self.dictionary = dictionary

	def start_game(self):
		self.target_word = self.dictionary.get_random_word()
		print("target word: ", self.target_word )

		self.grid.start_game(self.target_word)

#------------------------------------------SECONDARY SCREENS------------------------------------------#

class VictoryScreen(Screen):

	def __init__(self, gamescreen, **kwargs):
		super().__init__(**kwargs)

		layout = BoxLayout(orientation = 'vertical', spacing = 20, padding = 50)

		title = Label(text="You win!", font_size = '28sp', bold = True)
		layout.add_widget(title)

		btn = Button(text="Restart", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
		btn.bind(on_press=self.start_game)
		layout.add_widget(btn)

		self.add_widget(layout)

		self.gamescreen = gamescreen

		# Ensure that the key binding happens only when the victory screen is diplayed
		# bind them on enter and unbind them on leave
		self.bind(on_pre_enter=self.on_pre_enter)
		self.bind(on_leave=self.on_leave)

	#This is called when the screen is about to be displayed
	# ensures that key binding happens only when the victory screen is about to be displayed
	def on_pre_enter(self, *args):
			Window.bind(on_key_down=self.on_key_down)

	def on_leave(self, *args):
			Window.unbind(on_key_down=self.on_key_down)

	def on_key_down(self, window, key, scancode, codepoint, modifiers):
		if (key == 13): # Enter key
			self.start_game(None)

	def start_game(self, instance):
		# Set the current screen of the ScreenManager to "game" (this screen should exist in the ScreenManager)
		self.manager.current = "game" 
		self.gamescreen.start_game()


class DefeatScreen(Screen):

	def __init__(self,  gamescreen, **kwargs):
		super().__init__(**kwargs)

		layout = BoxLayout(orientation = 'vertical', spacing = 20, padding = 50)

		title = Label(text="Game over :(", font_size = '28sp', bold = True)
		layout.add_widget(title)

		btn = Button(text="Restart", size_hint=(0.5, 0.2), pos_hint={'center_x': 0.5})
		btn.bind(on_press=self._restart_game)
		layout.add_widget(btn)

		self.add_widget(layout)

		self.gamescreen = gamescreen

		# Ensure that the key binding happens only when the victory screen is diplayed
		# bind them on enter and unbind them on leave
		self.bind(on_pre_enter=self._on_pre_enter)
		self.bind(on_leave=self._on_leave)

	#This is called when the screen is about to be displayed
	# ensures that key binding happens only when the victory screen is about to be displayed
	def _on_pre_enter(self, *args):
		Window.bind(on_key_down=self._on_key_down)

	def _on_leave(self, *args):
			Window.unbind(on_key_down=self._on_key_down)

	def _on_key_down(self, window, key, scancode, codepoint, modifiers):
		if (key == 13):  # Enter key
			self._restart_game(None)

	def _restart_game(self, instance):
		self.manager.current = "game"
		self.gamescreen.start_game()
