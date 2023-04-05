
Step1: Follow this video to download Node-exporter first >> https://www.youtube.com/watch?v=uCYfDtR9S9k&t=26s

docker run -d \
> --net="host" \
> --pid="host" \
> -v "/:/host:ro,rslave" \
> quay.io/prometheus/node-exporter \
> --path.rootfs=/host


Step 2: Create Prometheus.yml

global:
  scrape_interval: 5s
  external_labels:
    monitor: 'node'
scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['192.168.88.97:9090'] ## IP Address of the localhost
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['192.168.88.97:9100'] ## IP Address of the localhost
      

```
192.168.88.97 is the ip address of our host machine and we get it
by using "ifconfig" command in our terminal.

In my case, i get the following when i use it and scroll to the base wlx.... to 
see the value of the inet address:

 vethcaeb9fb: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet6 fe80::687c:9cff:fe4f:bdd2  prefixlen 64  scopeid 0x20<link>
        ether 6a:7c:9c:4f:bd:d2  txqueuelen 0  (Ethernet)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 494  bytes 88296 (88.2 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

wlx28ee520868b9: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.88.97  netmask 255.255.255.0  broadcast 192.168.88.255
        inet6 fe80::f18f:6018:a20e:987c  prefixlen 64  scopeid 0x20<link>
        ether 28:ee:52:08:68:b9  txqueuelen 1000  (Ethernet)
        RX packets 822150  bytes 955915554 (955.9 MB)
        RX errors 0  dropped 214097  overruns 0  frame 0
        TX packets 470142  bytes 79273897 (79.2 MB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```
      



Step 3: Install Prometheus on docker >> https://hub.docker.com/r/prom/prometheus

Bind-mount your prometheus.yml from the host by running the code below
Ensure you cd into the container containing the prometheus.yml before running this code:

docker run -d --name prometheus -p 9090:9090 -v $PWD/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus


Step 4: Install Grafana from docker website >> https://hub.docker.com/r/grafana/grafana

docker run -d --name=grafana -p 3000:3000 grafana/grafana


When you try to connect prometheus to in Grafana and you get this error: Err reading Prometheus: Post "http://localhost:9090/api/v1/query": dial tcp 127.0.0.1:9090: connect: connection refused, you can just use the docker inspect command to find the IP address of the Prometheus container and then replace the localhost word with it.