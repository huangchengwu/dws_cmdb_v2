#!/bin/bash

s="HjxTGYusFvsEGJt7JVU7dyjnw6JsRE7Ac9hwkZia3Ohhj8GyHCrNb28qIhWMxmhz" # 请替换为您实际的密钥
url="http://cmdb.keli.vip/Webhook/?taskdeploy_env=132&task_type=1&select_HostGroup=100"
body=""

expected_signature=$(printf "%s" "$body" | openssl dgst -sha1 -hmac "$s" | awk '{print "sha1=" $2}')

echo $expected_signature

curl -X POST -H "X-Hub-Signature: $expected_signature" -d "$body" "$url"




#用户密码key 时间戳 md5算一下
