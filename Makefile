build:
	# pyinstaller -F src/main.py --name layers
	docker build . --tag layers

run: clean
	docker run -it layers

test:
	docker run -it layers "./run_tests.sh"
	
clean:
	docker prune

rm:
	docker image rm -f layers

	