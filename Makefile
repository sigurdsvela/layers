build:
	# pyinstaller -F src/main.py --name layers
	docker build . --tag layers

run:
	docker run -it layers "./setup_testenv.sh"

test:
	docker run -it layers "./run_tests.sh"

clean:
	docker system prune -f

rm:
	docker image rm -f layers

	