.PHONY: all env install run clean

# Default target: creates the virtual environment and installs dependencies.
all: env

# Create the virtual environment if it does not exist.
env:
	@if [ ! -d "kivy_env" ]; then \
		echo "Creating virtual environment 'kivy_env'..."; \
		python3 -m venv kivy_env; \
		kivy_env/bin/python -m pip install kivy; \
	fi

# Run the application using Wordle.py.
run:
	kivy_env/bin/python Wordle.py

# Clean up temporary files such as __pycache__ directories.
clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +

fclean: clean
	rm -fr ./kivy_env

re: fclean all
