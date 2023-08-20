Image optimization and compression server with high durability


How to deploy: on Linux with installed Docker and Docker Compose execute:

```bash
cd image_optimization_service/
docker compose -f docker-compose.yml up -d
```

Testing: enter [docs](http://127.0.0.1/docs#/) and try each of two available methods.
If you are deploying that service in VirtualBox, don't forget to passthrough 80 port.
