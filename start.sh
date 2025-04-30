#!/bin/sh
dws_cmdb_dir="/dws_cmdb/"
set -x
cat >/etc/systemd/system/web_result.service <<EOF
[Unit]
Description=web_result
After=network.target

[Service]
ExecStart=/bin/bash -c "cd /usr/local/diancan/  &&  python3.9 -m http.server 7000"
Restart=always
User=root
Group=root

[Install]
WantedBy=multi-user.target

 
EOF
##
cat >/etc/systemd/system/dws_cmdb.service <<EOF
[Unit]
Description=dws_cmdb
After=network.target

[Service]
ExecStart=/bin/bash -c "cd  /dws_cmdb &&  make prd run"
Restart=always
User=root
Group=root

[Install]
WantedBy=multi-user.target

 
EOF

cat >/etc/systemd/system/webshell.service <<EOF
[Unit]
Description=webshell
After=network.target

[Service]
ExecStart=/bin/bash -c "cd  /dws_cmdb/fortress/package/linux &&  ./webshell"
Restart=always
User=root
Group=root

[Install]
WantedBy=multi-user.target

 
EOF
#/usr/local/code-server/src/browser/pages/login.html
#/root/.config/code-server

cat >code-server.service <<EOF

[Unit]

Description=code-server

After=network.target



[Service]

ExecStart=/bin/bash -c "cd /usr/local/code-server/bin/ &&  ./code-server --port 9999 --host 0.0.0.0 --auth password "

Restart=always

User=jenkins
Group=jenkins



[Install]

WantedBy=multi-user.target
EOF

cat >/etc/systemd/system/dws_cmdb-celery.service <<EOF
[Unit]
Description=dws_cmdb-celery
After=network.target

[Service]
ExecStart=/bin/bash -c "cd  /dws_cmdb &&  make celery"
Restart=always
User=root
Group=root

[Install]
WantedBy=multi-user.target

EOF

if [ -d "/data/" ]; then
    echo "持久化启动"
    if [ ! -f "/data/db.sqlite3" ]; then
        echo "第一次启动"
        mv db.sqlite3 /data/db.sqlite3
        ln -s /data/db.sqlite3 ${dws_cmdb_dir}
    else
        echo "启动链接"
        rm db.sqlite3
        ln -s /data/db.sqlite3  ${dws_cmdb_dir}
    fi
else
    echo "无持久化启动"
fi
unlink ${dws_cmdb_dir}uploads
unlink ${dws_cmdb_dir}static/assets/jenkins
rm -rf  ${dws_cmdb_dir}uploads
rm -rf  ${dws_cmdb_dir}static/assets/jenkins
ln -s /var/lib/jenkins/workspace/ ${dws_cmdb_dir}static/assets/jenkins
ln -s /uploads/ ${dws_cmdb_dir}
make up
##

systemctl daemon-reload
systemctl enable dws_cmdb-celery dws_cmdb   web_result
systemctl restart dws_cmdb-celery dws_cmdb webshell  web_result
systemctl status dws_cmdb-celery dws_cmdb webshell web_result
