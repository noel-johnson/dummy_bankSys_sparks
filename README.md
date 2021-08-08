
# BankSys 

A dummy bank system application with database functionality, done under the intership of [TheSparksFoundation](http://thesparksfoundation.org)


## Deployment
**Make sure to initialize git.**

To deploy this project on Heroku run

1. Login to heroku
```bash
  heroku login
```
2. Create a heroku application
```bash
  heroku create *app-name*
```
3. Push the project to heroku
```bash
  git push heroku main
```
  
## Run Locally

Clone the repo

```bash
  git clone https://github.com/noel-johnson/dummy_bankSys_sparks.git bankSys
  cd bankSys
```

Initialize a python virtual environment
```bash
python3 -m venv env
```

Source the environment
```bash
source env/bin/activate
```    

Install all required dependecies
```bash
pip3 install -r requirements.txt
```

Start the server
```bash
python3 app.py
```
It should by default run on
```http
http://127.0.0.1:5000/ 
```