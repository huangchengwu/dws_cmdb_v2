version ?= 1 
p ?= 80

celery:
	python3 -m  celery -A dws_cmdb  worker --loglevel=info
install:
	python3 -m pip install -r requirements.txt  -i https://mirrors.aliyun.com/pypi/simple/ 
run:
	python3 manage.py runserver 0.0.0.0:$(p)
up:
	python3 manage.py makemigrations 
	python3 manage.py  migrate
pip:
	python3 -m pip install -r requirements.txt  -i https://mirrors.aliyun.com/pypi/simple/ 
dev:
	cp -rf dws_cmdb/settings.py_dev  dws_cmdb/settings.py
prd:
	cp -rf dws_cmdb/settings.py_prd dws_cmdb/settings.py
k8s:
	cp -rf dws_cmdb/settings.py_k8s dws_cmdb/settings.py

push:
	git add * 
	git commit -m "add"  
	git push -u origin main