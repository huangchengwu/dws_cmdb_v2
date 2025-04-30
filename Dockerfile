# # 基础镜像由  python:3.9.17-alpine3.18 打包成，替换成基础镜像后，后续打包上传会快一点只是更换层数和增加层数
# FROM  python:3.9.17-alpine3.18
# WORKDIR  /dws_cmdb
 
# RUN  echo "https://mirrors.aliyun.com/alpine/v3.14/main" > /etc/apk/repositories && \
#     echo "https://mirrors.aliyun.com/alpine/v3.14/community" >> /etc/apk/repositories  && \  
#     apk update && apk add build-base dumb-init mariadb-dev  && \
#     pip install --upgrade  pip -i https://mirrors.aliyun.com/pypi/simple/ && \
#     pip install -r requirements.txt  -i https://mirrors.aliyun.com/pypi/simple/ 
# ENTRYPOINT ["/usr/bin/dumb-init", "--"]
# CMD [ "python","manage.py","runserver", "0.0.0.0:8000"]
# CMD ["sh", "-c", "python -m celery -A dws_cmdb worker -l debug & python manage.py runserver 0.0.0.0:8000"]
# #后续打包更换对应层就行 不需要重新搞一遍
FROM huangchengwu6904/hi-app:dws_cmdb-base
ADD dws_cmdb.tar.gz . 
CMD [ "/dws_cmdb/start.sh"]
