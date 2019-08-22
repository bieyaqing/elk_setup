# ELK Setup

## Docker link:
https://elk-docker.readthedocs.io/

## Docker compose
```yml
ubuntu:
  image: ubuntu
  stdin_open: true
  tty: true

elk:
  image: sebp/elk
  ports:
    - "5601:5601"
    - "9200:9200"
    - "5044:5044"
```
### Commands
```
docker-compose up elk
docker-compose up ubuntu
```
```
docker run -p 5601:5601 -p 9200:9200 -p 5044:5044 -it --ulimit nofile=1024:65536 --name elk sebp/elk
```

## Kibana Config
    1. Setting -> Kibana -> Index Patterns
    2. Create index pattern
    3. filebeat* -> do not use filter -> Create


## Logstash Config
### /etc/logstash/*
```conf
input {
  beats {
    port => 5044
    ssl => false
    ssl_certificate => "/etc/pki/tls/certs/logstash-beats.crt"
    ssl_key => "/etc/pki/tls/private/logstash-beats.key"
  }
}
```
```conf
filter {
  grok {
    match => { "message" => "%{LOGLEVEL:level} %{TIMESTAMP_ISO8601:timestamp} %{IP:ip_addr} %{WORD:port} %{GREEDYDATA:description}" }
  }
  date {
    match => [ "timestamp", "YYYY-MM-DD'T'HH:mm:ss.SSS" ]
  }
}
```
```conf
filter {
  grok {
    match => { "message" => "%{LOGLEVEL:level} %{TIMESTAMP_ISO8601:timestamp} %{IP:ip_addr} %{PROG:port} %{WORD:method} %{URIPATHPARAM:path} %{USERNAME:user} %{PATH:code_path} %{GREEDYDATA:data}" }
  }
  date {
    match => [ "timestamp", "YYYY-MM-DD'T'HH:mm:ss.SSS" ]
  }
}
```
```conf
output {
  elasticsearch {
    hosts => ["localhost:9200"]
    manage_template => false
    index => "%{[@metadata][beat]}-%{+YYYY.MM.dd}"
  }
}
```
### Link
https://github.com/elastic/logstash/blob/v1.4.2/patterns/grok-patterns

## Filebeat Config
<!-- ```
filebeat modules enable system
``` -->
### /etc/filebeat/filebeat.yml
```yml
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /home/logs/*.log
#setup.kibana:
  #host: "172.17.0.2:5601"
filebeat.config.modules:
  path: ${path.config}/modules.d/*.yml
  reload.enabled: false
setup.template.settings:
  index.number_of_shards: 1
output.logstash:
  enabled: true
  hosts: ["172.17.0.2:5044"]
```
```
filebeat setup --template -E output.logstash.enabled=false -E 'output.elasticsearch.hosts=["172.17.0.2:9200"]'
```
