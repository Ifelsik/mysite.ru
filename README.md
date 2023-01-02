# mysite.ru
 My WSGI app  
Командой клонируется репозиторий с приложением  
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
Далее в директории приложения устанавливаются необходимые модули  
` 
pip install -r requirements.txt
`  
Затем устанавливается переменная окружения и запускается приложение  
`
export FLASK_APP=app.py
`  
`
flask run
`  
