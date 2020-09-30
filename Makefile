build:
	# pyinstaller -F src/main.py --name layers
	docker build . --tag layers

run:
	docker run -it --mount type=bind,src=$(shell pwd),target=/home/docker/layers layers

test:
	docker run -it layers "./run_tests.sh"

clean:
	docker system prune -f

rm:
	docker image rm -f layers

	