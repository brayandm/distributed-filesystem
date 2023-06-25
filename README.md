## Docker compose instructions

1 - clone the repository:

```bash
git clone https://github.com/brayandm/distributed-filesystem.git
```

2 - Change to the directory:

```bash
cd distributed-filesystem
```

3 - Copy the .env.example file to .env:

```bash
cp .env.example .env
```

4 - Start docker compose:

```bash
docker compose up
```

5 - Execute the guest python file:

```bash
python guest.py
```

Notes:

- Be careful, the port 9080 must be free for the master node
- The storage of every node is in the folder `./storage/nodeX` where X is the number of the node (the volumes are binded to the host for testing purposes)
- The application also use redis for managing the location of the chunks