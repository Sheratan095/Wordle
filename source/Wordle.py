from kivy.config import Config
Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '340')
Config.set('graphics', 'height', '455')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition

from Globals import *
from Views import MainMenuScreen, GameScreen, VictoryScreen, DefeatScreen


class WordleApp(App):

	def build(self, dictionary_file = "test.txt"):

		self.icon = icon

	 	# Create a ScreenManager with a fade transition effect between screens.
		sm = ScreenManager(transition=FadeTransition())

	 	# Add the MainMenuScreen to the ScreenManager and assign it the name 'menu'.
		mainMenù = MainMenuScreen(name ='menu')
		sm.add_widget(mainMenù)

		gamescreen = GameScreen(name = 'game')
		sm.add_widget(gamescreen)

		mainMenù.set_gamescreen(gamescreen)

		sm.add_widget(VictoryScreen(name = 'victory'))
		sm.add_widget(DefeatScreen(name = 'defeat'))

		return (sm)


if __name__ == '__main__':
	WordleApp().run()