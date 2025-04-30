#!/bin/bash
export ID=vW1RcAl7Mb0d5gyHNQIAcH110lWoOW2BmWJIero8
export SECRET=DZFpuNjRdt5xUEzxXovAp40bU3lQvoMvF3awEStn61RXWE0Ses4RgzHWKJKTvUCHfRkhcBi3ebsEfSjfEO96vo2Sh6pZlxJ6f7KcUbhvqMMPoVxRwv4vfdWEoWMGPeIO
# Generate code verifier
code_verifier=$(head /dev/urandom | tr -dc A-Z0-9 | head -c $(($RANDOM % 86 + 43)))

# Calculate code challenge
code_challenge=$(echo -n $code_verifier | openssl dgst -sha256 -binary | base64 | tr -d '=' | tr '+/' '-_')

# Get ID from environment variable
ID=$ID

# Print the resulting URL
printf "http://127.0.0.1/o/authorize/?response_type=code&code_challenge=%s&code_challenge_method=S256&client_id=%s&redirect_uri=http://127.0.0.1/ping\n" "$code_challenge" "$ID"
 
CODE=oMj9H21HxpsTIuOEFq3QxjKaeUty3z

curl -X POST \
    -H "Cache-Control: no-cache" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    "http://127.0.0.1/o/token/" \
    -d "client_id=${ID}" \
    -d "client_secret=${SECRET}" \
    -d "code=${CODE}" \
    -d "code_verifier=${CODE_VERIFIER}" \
    -d "redirect_uri=http://127.0.0.1/ping" \
    -d "grant_type=authorization_code"



