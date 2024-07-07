server {
  listen 80;
  server_name ${DOMAIN} www.${DOMAIN} ;

  location /static {
    alias /vol/static;
  }

  location / {
    uwsgi_pass            ${APP_HOST}:${APP_PORT};
    include               /etc/nginx/uwsgi_params;
    client_max_body_size  10M;
    proxy_set_header      X-Forwarded-Proto $scheme;
    return 301 https://$host$request_uri;
  }
}