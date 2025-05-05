NAME = Wordle

all: env

# Create the virtual environment if it does not exist.
env:
	@if [ ! -d "kivy_env" ]; then \
		python3 -m venv kivy_env; \
		kivy_env/bin/python -m pip install kivy; \
		echo "$(GREEN)[$(NAME)]:\t Venv created$(RESET)"; \
	fi

# Run the app
run: env
	@echo "$(BLUE)[$(NAME)]:\t RUN$(RESET)"
	kivy_env/bin/python source/Wordle.py

clean:
	@rm -rf source/__pycache__/
	@echo "$(RED)[$(NAME)]:\t CLEAN$(RESET)"

fclean: clean
	@rm -fr ./kivy_env
	@rm -fr build/
	@rm -fr dist/
	@rm -f *.spec
	@echo "$(RED)[$(NAME)]:\t FCLEAN$(RESET)"

re: fclean all

#COLORS

GREEN=\033[0;32m
RED=\033[0;31m
BLUE=\033[0;34m
RESET=\033[0m
