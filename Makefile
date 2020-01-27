init :
	@echo "Setting up the Docker container"
	sudo docker build -t datacleaner-api:latest .
	@echo "Docker container setup is now complete"
    

test :  
	@echo "Running tests"
	sudo docker run --entrypoint /bin/bash datacleaner-api:latest -c ./runTests.sh


serve :
	@echo "Running the Data Clearner API as a daemon"
	sudo docker run -d -p 5000:5000 datacleaner-api:latest
	@echo "Data Cleaner API is now running as a daemon"
