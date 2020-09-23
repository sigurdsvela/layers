build:
	pip3 install pyyaml
	pyinstaller -F src/main.py --name layers

run:
	docker build . --tag layers
	docker run -it layers

clean:
	rm -rf build
	rm -rf dist

	