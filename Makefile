build:
	# pyinstaller -F src/main.py --name layers
	docker build . --tag layers

run:
	docker run -it layers

test:
	docker run -it layers "./tests/start_tests.sh"

clean:
	rm -rf build
	rm -rf dist

	