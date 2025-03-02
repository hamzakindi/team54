# Technology Demostrator
This sample project demostrate how you can use ML with Prolog and expose them via fast api. The project also has a Next JS front end application that consume these API.
In this sample app I am using ML model for predicting diabetis and prolog for providing recommendation.
# MedHack Hackathon Pitch
[Pitch Video](https://www.youtube.com/watch?v=psqjuB_8A14)
# Tech Stack Details
This 49 seconds video contains the details about the tech stack.
[Tech Demo Video](https://youtu.be/JL9Dfv04ZhA)

# Python environment
Use seperate python virtual environments for prolog and model fast api code.
I used medhack for model and medhack_prolog for prolog code.

# Running the sample solution
You need to run all three servers in seperate consoles.
## Next JS App
Run this command inside app folder
npm run dev
## Backend
From inside backend folder
python run.py
## Prolog
Run this command inside prolog/fastapi folder
python api_service.py
# Disclaimer
I picked up the datset checked in with my code from Kaggle. [Download link](https://www.kaggle.com/datasets/akshaydattatraykhare/diabetes-dataset). This dataset is in public domain license. [License link](https://creativecommons.org/publicdomain/zero/1.0/)

