
server {
  listen 80;
  server_name "__DEVOPS_API_FQDN__";
  client_max_body_size 5G;

  access_log $log_dir/backend.devops.access.log devops_format;
  error_log ./logs/backend.devops.error.log;

  #设置通用变量
  include set.conf;
  
#  ### ssl config begin ###
#  listen 443 ssl;
#  include ./conf/devops.ssl;
#  # force https-redirects
#  if ($scheme = http) {
#  return 301 https://$server_name$request_uri;
#  }
#  ### ssl config end ###

  location / {
    return 404;
  }

  #将错误统一处理成json格式返回
  include error.json.handler.conf;
  include error.json.conf;

  #网关验证逻辑
  include auth.conf;

  # user层服务分发
  location ~ /([^/]+)/api/user/(.*) {
    header_filter_by_lua_file 'conf/lua/cors_filter.lua';
  	auth_request /auth/user;
  	auth_request_set $bk_token $sent_http_x_devops_bk_token;
  	set $access_type 'user';
  	set $service $1;
  	set $path $2;
  	set $target '';
  	access_by_lua_file 'conf/lua/router_srv.lua';
  	proxy_set_header X-Real-IP $remote_addr;
  	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
  	proxy_set_header X-DEVOPS-RID $uuid;
  	proxy_set_header X-DEVOPS-BK-TOKEN $bk_token;
  
  	proxy_http_version 1.1;
  	# 反向代理到目标ip，端口，路径和参数
  	proxy_pass http://$target/api/user/$path?$args;
  }
}
