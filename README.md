# yahtzee_backend
This is a repo for the Binary Bits team to develop the back end of a Yahtzee app for Foundations of Software Engineering.

# Setup
1. Download this repository from Github, either:  
    a. Download [Git command line tools](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and clone the repo  
    b. OR click on the green Code dropdown button and download a zip file of the repo  

2. Docker  
    a. [Sign up](https://hub.docker.com/signup) for a free Docker account  
    b. Download the Docker desktop app appropriate for your computer    
    c. If you already had your terminal/command promp running, close and reopen it so that you can use the Docker CLI    

# Testing the App

# Running the App
* Open the terminal/command prompt and navigate to the yahtzee_backend directory
* Run the following commands  
    `docker build -t yahtzee-backend .`  (This builds the Docker container as specified in the Dockerfile)  
    `docker run -dp 8081:8081 yahtzee-backend`  (This starts the server in the container)
