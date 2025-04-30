#!/bin/bash
v=$(date +%s)
echo $v
git clone -b master git@github.com:innet8/dws_cmdb.git dws_cmdb-${v}
unlink  /dws_cmdb && ln -s /dws_cmdb-$v/ dws_cmdb
cd dws_cmdb &&  sh start.sh
