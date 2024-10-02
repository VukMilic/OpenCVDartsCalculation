# Open CV Darts Calculation
The purpose of this project is to calculate dart points via dart image. One of the biggest issues in the game of darts is that you need to calculate points by manually writing the numbers in every round. That is the reason why this app has been developed. The existing software that already has some kind of automated calculations are pretty expensive. With this application, you will have a minimal cost and enjoy the game equally.

Run all the servers that are written bellow, follow the steps written on the clients side of the app and enjoy the game.

For starting the system you will need to run the following things:
  - inside 'FLASK deo' folder you will need to install FLASK and OpenCV libraries
  - after installation, run command: python app2.py
  - install MongoDB database and create db darts
  - then go to directory 'MEAN deo':
       - go inside frontend directory and run command: ng serve
       - go inside backend directory and run two commands: tsc and then npm run serve

This app requires MEAN (MongoDB, Express, Angular, NodeJS) and also Python with OpenCV and Flask. So, you will need to have installed all of them.
After finishing all steps above, zour app will be running on localhost:4200.
