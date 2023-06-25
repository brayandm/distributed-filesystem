## Docker compose instructions

1 - Copy the .env.example file to .env:

```bash
cp .env.example .env
```

2 - Start docker compose:

```bash
docker compose up
```

3 - Execute the guest python file:

```bash
python guest.py
```

Notes:

- Be careful, the port 9080 must be free for the master node
- The storage of every node is in the folder `./storage/nodeX` where X is the number of the node (the volumes are binded to the host for testing purposes)
- The application also use redis for managing the location of the chunks