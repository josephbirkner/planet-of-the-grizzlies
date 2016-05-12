
# This file includes all server-related classes.
# This includes:
# - IServer: Base interface for local and remote servers
# - RemoteServer: The local servers remote deputy. In a network of n hosts,
#   there may be n-1 RemoteServers and 1 local server.
# - LocalServer: The actual server that is responsible for updating the world.

