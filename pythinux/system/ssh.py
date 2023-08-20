import paramiko
import socket
import traceback
def get_local_ip():
    try:
        # Create a socket object and connect to an external server (8.8.8.8)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except socket.error:
        return "127.0.0.1"
class MySSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        # Replace with your own authentication logic
        if username == "your_username" and password == "your_password":
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True


def start_ssh_server(host, port):
    server = paramiko.Transport((host, port))

    ssh_server = MySSHServer()
    server.add_server_key(paramiko.RSAKey.generate(2048))  # Generate a temporary key for encryption

    try:
        server.start_server(server=ssh_server)

        while not ssh_server.event.is_set():
            channel = server.accept(20)
            if channel is None:
                continue

            try:
                channel.send("Pythinux SSH\n")
                channel.send(f"Welcome {currentUser.username}\n")
                channel.send("To exit, use the `exit` or `quit` commands.\n")
                channel.send(f"{currentUser.username}@{channel.getpeername()[0]} $")

                command = ""
                while True:
                    recv_data = channel.recv(1024)
                    if not recv_data:
                        break
                    recv_str = recv_data.decode('utf-8')
                    command += recv_str

                    if command.endswith("\n"):
                        command = command.strip()
                        if command.lower() in  ["exit","quit"]:
                            break

                        output = main(currentUser, command)
                        channel.send(output)
                        channel.send(f"{currentUser.username}@{channel.getpeername()[0]} $ ")
                        command = ""

            except Exception as e:
                print("Error:", str(e))
                channel.close()
    except:
        print(traceback.format_exc())

if args == ["start"]:
    HOST = get_local_ip()
    PORT = 22222
    print("Starting SSH server...")
    print("Hostname: {}\nPort: {}".format(HOST, PORT))
    start_ssh_server(HOST, PORT)
else:
    div()
    print("ssh: Pythinux SSH Server")
    div()
    print("ssh start: Start the server.")
    div()