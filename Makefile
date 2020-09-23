build:
	mkdir build
	cp main.py build/main.pyx
	cython --embed -I./ -o build/main.c setup.py
	gcc -I/usr/local/Cellar/python@3.7/3.7.9/Frameworks/Python.framework/Versions/Current/include/python3.7m -o build/layers build/main.c

	# docker build . --tag layers

run:
	docker run -it layers

clean:
	rm -rf build

	