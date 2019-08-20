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

## Logstash Config
```conf
filter {
  if [type] == "log" {
    grok {
      match => { "message" => "\[%{WORD:log_level}\]\[%{IP:log_ipaddr}\]\[%{TIMESTAMP:log_timestamp}\] %{GREEDYDATA:message}" }
    }
  }
}
```
### Link
https://github.com/elastic/logstash/blob/v1.4.2/patterns/grok-patterns

## Filebeat Config
```
filebeat modules enable system
```
```yml
filebeat.inputs:
- type: syslog
  enabled: true
  paths:
    - /home/logs/*.log
setup.kibana:
  host: "172.17.0.2:5601"
filebeat.config.modules:
  path: ${path.config}/modules.d/*.yml
  reload.enabled: false
setup.template.settings:
  index.number_of_shards: 1
output.logstash:
  enabled: true
  hosts: ["172.17.0.2:5044"]
```
