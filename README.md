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

## Kibana Config
    1. Setting -> Kibana -> Index Patterns

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
    match => { "message" => "%{LOGLEVEL:level} %{IP:ip_addr} %{TIMESTAMP_ISO8601:timestamp} %{GREEDYDATA:description}" }
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
```
filebeat modules enable system
```
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
