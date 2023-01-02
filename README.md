# mysite.ru
 My WSGI app  
<<<<<<< HEAD
Командой клонируется репозиторий с приложением  
=======
Предварительно клонируется репозиторий с приложением  
>>>>>>> 0da30bec812386f731ef30cdf8cab51449be4d02
`
git clone https://github.com/Ifelsik/mysite.ru.git
`  
Для установки предварительно создаётся виртуальная среда  
`
python -m venv env
`  
Для её запуска используется команда (Linux)  
`
source env/bin/activate
`  
<<<<<<< HEAD
Далее в директории приложения устанавливаются необходимые модули  
` 
pip install -r requirements.txt
`  
Затем устанавливается переменная среды и запускается приложение  
`
export FLASK_APP=app.py  
=======
Далее устанавливаются необходимые модули  
`
pip install -r requirements.txt
`  
Затем устанавливается переменная среды и запускается приложение, предварительно перйдя в директорию с приложением  
`
cd mysite.ru
export FLASK_APP=app.py
>>>>>>> 0da30bec812386f731ef30cdf8cab51449be4d02
flask run
`  
