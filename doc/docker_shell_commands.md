# Bunch of shell commands 

```shell
docker compose down && docker image rm green_adam-svc; \
docker compose up -d && docker logs greenadam-services
#
docker compose down && docker image rm green_adam-svc
```


```shell
sudo rm -rf green_adam && git clone https://github.com/pr0xtti/green_adam.git
```

```shell
cd green_adam
docker compose up -d && docker logs greenadam-services
```

```shell
docker compose up -d && docker logs greenadam-services -n all 2>&1
```

```shell
git add run.sh && git commit -m "run.sh updated" && git push
```

```shell
docker compose down && docker image rm green_adam-svc && \
cd .. && \
sudo rm -rf green_adam && git clone https://github.com/pr0xtti/green_adam.git && \
cd green_adam && \
docker compose up -d && \
echo "Sleeping ..." && \ 
sleep 3 && \
docker logs greenadam-services -f 2>&1
```

```shell
docker logs greenadam-services -n all 2>&1 | less -S
```