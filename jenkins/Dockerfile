FROM huangchengwu6904/app:jenkins-cicd
USER jenkins
ENV TZ=Asia/Shanghai 

COPY webshell  /
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD sh -c -x "/usr/local/bin/jenkins.sh & sudo dockerd"


