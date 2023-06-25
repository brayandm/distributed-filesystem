from client import Client

client = Client("http://localhost", 9080)

# Store a file
print(client.store_file("test.txt", "hello world"))

# Get a file
print(client.get_file("test.txt"))

# Get the size of a file
print(client.get_size("test.txt"))

# Delete a file
print(client.delete_file("test.txt"))

# Upload a file
print(client.upload_file("example.txt"))

# Get a file
print(client.get_file("example.txt"))

# Get the size of a file
print(client.get_size("example.txt"))

# Delete a file
print(client.delete_file("example.txt"))
