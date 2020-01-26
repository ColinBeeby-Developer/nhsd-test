init :
	@echo "Setting up the Docker container"
	sudo docker build -t datacleaner-api:latest .
	@echo "Docker container setup is now complete"
    

test :
	@echo "Running tests"
	sudo python -m unittest discover -v
	@echo "Completed running tests"
   

serve :
	@echo "Running the Data Clearner API as a daemon"
	sudo touch /tmp/log.txt
	sudo docker run -d -p 5000:5000 -v /tmp/log.txt:/app/log.txt datacleaner-api:latest
	@echo "Data Cleaner API is now running as a daemon"
