import base64
client_id = "vW1RcAl7Mb0d5gyHNQIAcH110lWoOW2BmWJIero82"
secret = "DZFpuNjRdt5xUEzxXovAp40bU3lQvoMvF3awEStn61RXWE0Ses4RgzHWKJKTvUCHfRkhcBi3ebsEfSjfEO96vo2Sh6pZlxJ6f7KcUbhvqMMPoVxRwv4vfdWEoWMGPeIO"
credential = "{0}:{1}".format(client_id, secret)
print(base64.b64encode(credential.encode("utf-8")))
# export CREDENTIAL=
# curl -X POST -H "Authorization: Basic ${CREDENTIAL}" -H "Cache-Control: no-cache" -H "Content-Type: application/x-www-form-urlencoded" "http://127.0.0.1/o/token/" -d "grant_type=client_credentials"
# curl -X POST \
#     -H "Authorization: Basic ${CREDENTIAL}" \
#     -H "Cache-Control: no-cache" \
#     -H "Content-Type: application/x-www-form-urlencoded" \
#     "http://127.0.0.1/o/token/" \
#     -d "grant_type=client_credentials"