Step-by-Step Tutorial for Absolute Beginners
Step 1: Introduction to the Tools
Substep 1: Install Visual Studio Code (VSCode)

Go to the VSCode download page.
Download the installer for your operating system (Windows, macOS, or Linux).
Run the installer and follow the on-screen instructions to complete the installation.
Substep 2: Install Git

Go to the Git download page.
Download the Git installer for your operating system.
Run the installer and follow the on-screen instructions to complete the installation.
Substep 3: Create a GitHub Account

Go to the GitHub sign-up page.
Fill in the required information to create your GitHub account.
Verify your email address to complete the account creation process.
Step 2: Setting Up the Repository
Substep 1: Clone the Repository

Open a terminal or command prompt on your computer.
Run the following command to clone the repository:
bash
git clone https://github.com/hamzakindi/team54.git
Navigate to the cloned repository's directory:
bash
cd team54
Substep 2: Open the Cloned Repository in VSCode

Open Visual Studio Code.
Click on File > Open Folder....
Navigate to the team54 folder and open it.
Substep 3: Install Necessary Extensions in VSCode

Open VSCode.
Go to the Extensions view by clicking on the Extensions icon in the Activity Bar on the side of the window or by pressing Ctrl+Shift+X.
Search for and install the following extensions:
GitLens: An extension for Git supercharged.
Prettier: An extension for code formatting.
Follow-up Steps
Overview of the Project Structure and Files

Provide a brief description of the main files and folders in the project.
Explain the purpose of key files like README.md, package.json, etc.
Guide on Basic Git Commands and How to Make a Commit

Introduce basic Git commands like git status, git add, git commit, and git push.
Provide a simple example of making a change to a file and committing the change.
bash
# Make a change to a file
echo "Hello, World!" > hello.txt

# Check the status of the repository
git status

# Add the changed file to the staging area
git add hello.txt

# Commit the change with a message
git commit -m "Add hello.txt with greeting"

# Push the change to the remote repository
git push
