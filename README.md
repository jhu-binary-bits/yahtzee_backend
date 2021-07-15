# yahtzee_backend
This is a repo for the Binary Bits team to develop the back end of a Yahtzee app for Foundations of Software Engineering.

## Setup
1. Download this repository from Github, either:  
    a. Download [Git command line tools](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and clone the repo  
    b. OR click on the green Code dropdown button and download a zip file of the repo  

2. Docker  
    a. [Sign up](https://hub.docker.com/signup) for a free Docker account  
    b. Download the Docker desktop app appropriate for your computer    
    c. If you already had your terminal/command promp running, close and reopen it so that you can use the Docker CLI    

## Managing branches on Github

* Remote branches
    * A remote branch is a branch that has been pushed to Github by someone else, but is not yet merged to master.
    * To pull in a remote branch
        * In your terminal window, navigate to `yahtzee_backend`
        * Type `git switch {existing_branch_name}`, replacing {existing_branch_name} with the name of the remote branch that you want to switch to
* New local branches
    * If you want to develop on top of the master branch or on top of an existing branch, you might want to work on a new local branch.
    * To create a new local branch from master
        * In your terminal window, navigate to `yahtzee_backend`
        * Type `git checkout -b {new_branch_name}`, replacing {new_branch_name} with the name of the new branch you want to create
    * To create a new local branch from an existing branch
        * If the existing branch is not already on your local computer (if it is a remote branch).
            * Type `git switch {existing_branch_name}`
            * If you already see the existing branch on your own computer when you type `git branch`, you don't need to do this step. 
        * Type `git checkout -b {new_branch_name} {existing_branch_name}`. 
            * This will create a new branch, but will include all changes already made in the existing branch.

## Running the App
* Open the terminal/command prompt and navigate to the yahtzee_backend directory
* Run the following commands:
    `docker build -t yahtzee-backend .`  (This builds the Docker container as specified in the Dockerfile)
    `docker run -dp 8081:8081 yahtzee-backend`  (This starts the server in the container)
* Formal tests will be run every time the container is spun up with the `docker run` command

## Developing the App locally, or reviewing changes in a proposed PR
1) Make a new local branch or pull in a remote branch (see instructions above)
2) If you're developing locally, then make your changes
3) If you already had a docker container running the app, you need to stop the container
    * Navigate to the Docker app
    * Navigate to Containers/Apps
    * Any running containers will have a green box on the left side of them
    * Click on the Stop button on the right side of the row with the running container
4) Rebuild the docker container
    * Any changes you've made need to be built into a new docker container.
    * Run `docker build -t yahtzee-backend .` to create the new container
5) Run the container
    * `docker run -dp 8081:8081 yahtzee-backend`
6) Repeat from step 2 as necessary!

* To view logs:
    * Open the Docker App
    * Click on Containers/Apps
