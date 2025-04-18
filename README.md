# CMP9134-2425-basicWebApp
 A web app for searching for open licence media

 This is a simple full-stack web application composed of a backend and a frontend. It utilizes Flask for the backend API and ReactJS for the frontend interface.

Instructions to launch application on INB labs' PCs
1. Clone the repository
Open a Terminal, the launch the following commands:

git clone https://github.com/francescodelduchetto/CMP9134-2425-basicWebApp
2. Open Visual Studio Code Container
Open VS Code

Click on the blue icon in the bottom left corner image

Select "Open Folder in Container..."

Locate the folder CMP9134-2425-basicWebApp, select it and click Open

Wait until the setup is complete.

3. Install requirements
 The following commands needs to be launched from terminals inside VSCode (click Terminal > New Terminal).

Install Python package requirements:
pip install -r requirements.txt
Install NodeJs and its requirements:
curl -sL https://deb.nodesource.com/setup_22.x -o nodesource_setup.sh
sudo bash nodesource_setup.sh && sudo apt install -y nodejs
cd frontend
npm install
4. Launch backend
Open a new VSCode Terminal and launch the following commands.

cd ../backend
python main.py
5. Launch frontend
On a different terminal, launch:

cd frontend
npm run dev
This will start the development server for the frontend, usually accessible at http://localhost:5173/.

CREDITS:
Adapted from: https://github.com/Pakheria/Basic-Web-Application


