FROM       php:7-apache

ENV        API_ENDPOINT="http://localhost:5000/api/"

COPY       . /var/www/html/
