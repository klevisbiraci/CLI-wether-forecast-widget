# CLI-wether-forecast-widget
Simple CLI wether forecast app using the meteosource api.
Get your own api key for free by signin up at: www.meteosource.com and place it at sample.env.
Link for the api documentation: www.meteosource.com/documentation.

## requirements:

- python version 3.11.4
- curses module
- dotenv module

you can use pip to install both the modules

## setup:
you can use pyinstaller to create an executable just make sure you install the required modules first.
Modules should be available globally.
```
pip install pyinstaller
pyinstaller /path/to/main.py
```
the executable should be in the dist directory

note: the terminal font size should be 10 or smaller  

## screenshots:
- current wether feature
  
![current](https://github.com/klevisbiraci/CLI-wether-forecast-widget/assets/126258692/1a3de03e-f6bf-43ae-a23a-ef05207e5479)

- hourly forecast feature
  
![hourly](https://github.com/klevisbiraci/CLI-wether-forecast-widget/assets/126258692/e424a3dc-743e-4e7d-ad7b-f26ab253a071)

- daily forecast
  
![daily](https://github.com/klevisbiraci/CLI-wether-forecast-widget/assets/126258692/a32e09d7-e7b1-4d12-af7d-d8b7afb89042)
note: the text its not stuck in a wierd way it is supposed to move i just couldnt be bothered uploading a gif :p 
