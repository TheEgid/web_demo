#web web_django_demo

Настройте Gunicorn таким образом, что бы он запускал ваше Django-приложение по адресу 0.0.0.0:8000 . (старый hello-world скрипт останется работать на порту 8080).  Nginx должен проксировать запросы как в предыдущем задании.

В результате ваше Django приложение должно отдавать по URL вида http://127.0.0.1/question/<123>/  страницы с кодом 200.  Содержимое страницы не имеет значение - главное, что был хотя бы 1 символ. По URL, не указанным в urls.py, ваше приложение должно возвращать код HTTP 404.


_РАБОЧАЯ ПАПКА - /home/box/web


```

git clone https://github.com/TheEgid/web_demo && sudo chmod g+rwx web_demo2

sudo pkill gunicorn 

sudo mv web_demo web

cd web && bash init.sh

sudo nginx -t

```
