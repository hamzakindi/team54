## Run the script using below command
First, set the execution policy:
Set-ExecutionPolicy RemoteSigned -Scope Process
Then run the installation script:
install_prolog.ps1

## Test the installation
swipl --version

## Check the installation by running the ruleset directly by navigating to ruleset directory and running the below command.
swipl test_recommendations.pl

## Test ruleset using below command on prolog ruleset.
get_test_recommendations(0.8, Category, Tests).