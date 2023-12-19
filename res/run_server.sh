#!/usr/bin/env bash

port=$1

response="HTTP/1.1 200 OK
Content-Type: text/plain

Hello, Tessie!"

nc -l -p "${port}" -c <<< "${response}"
