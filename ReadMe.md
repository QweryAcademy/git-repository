Getting Started with Django

1. Intall Python
    verify your python installation:

        python3 -V

    install python from python.org

2. Install a code editor
    We'd be using Visual Studio code - https://code.visualstudio.com

3. Set up version control with git

    3.1 Create a git account
        github.com

    3.1 Generate an RSA key for SSH access to git
        Open a terminal window and enter:

        ssh-keygen

    3.2 Copy your Public RCA 

        cat .ssh/id_rsa.pub

        the key should begin with 'ssh-rsa',
        copy the entire key

    3.2 Add Public RSA key to git for remote access

        Sign in to github
        Click on your user icon and select 'settings'
        Select 'SSH and GPG keys' on the left menu 
        Click on 'New SSH key'
        Paste your SSH key and give it a unique title ("My_Laptop" for example)

4. clone the project from github

        4.1 Copy SSH key and passphrase
            Navigate to the git repo:

            https://github.com/QweryAcademy/git-repository

            select "Clone or Download"

            Select "Use SSH"

            click the copy button to copy the URL to your clipboard

        4.2 Clone the repo into a local folder

            open terminal and navigate to the path you want to create the clone

            Enter the following code: 

            git clone "URL you copied from github without the quotes ofcourse"

5. git commands 

    you can "push" your updated code to the repo or "pull" remote code from the repo to your localhost with the followin commands





