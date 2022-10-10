import socket


class IRC:

    irc = socket.socket()

    def __init__(self):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, server, channel, bot_nick_name):
        """Connect to the server channel in arguments

        Args:
            server (string): Server name.
            channel (string): Channel name.
            bot_nick_name (string): Bot nick name.
        """
        print("Connecting to: " + server + "...")

        self.irc.connect((server, 6667))

        # Authentification part.
        self.irc.send(
            bytes(
                "USER "
                + bot_nick_name
                + " "
                + bot_nick_name
                + " "
                + bot_nick_name
                + " "
                + bot_nick_name
                + "\n",
                "UTF-8",
            )
        )
        self.irc.send(bytes("NICK " + bot_nick_name + "\n", "UTF-8"))

        # Wait for authentification and join the channel.
        while 1:
            ircmsg = self.irc.recv(2048).decode("UTF-8")
            ircmsg = ircmsg.strip("nr")
            print(ircmsg)
            if f"MODE {bot_nick_name} +x" in ircmsg:
                print("Changing channel")
                self.irc.send(bytes("JOIN " + channel + "\n", "UTF-8"))
                break

    def join(self, channel):
        """Join a channel

        Args:
            channel (string): Channel name.
        """
        self.irc.send(bytes("JOIN " + channel + "\n", "UTF-8"))

    def quit(self):
        """Quit a server"""
        self.irc.send(bytes("QUIT \n", "UTF-8"))

    def send_msg(self, recipient, msg):
        """Send a message to a user or a channel

        Args:
            recipient (string): User or channel name.
            msg (string): Message to send.
        """
        self.irc.send(bytes("PRIVMSG " + recipient + " :" + msg + "\n", "UTF-8"))

    def get_response(self, bot_nick_name):
        """Get responses from the channel

        Args:
            bot_nick_name (string): Bot nick name.
        """
        while 1:
            resp = self.irc.recv(2040).decode("UTF-8")
            if "PING" in resp:
                print("PONG " + resp.split()[1])
                self.irc.send(bytes("PONG " + resp.split()[1] + "\n", "UTF-8"))
            if "PRIVMSG" in resp:
                username = resp.split("!")[0][1:]
                message = resp.split(f"PRIVMSG {bot_nick_name} :")[1]
                print(f"{username}: {message}")


def main():
    ## IRC Config
    server = ""
    channel = ""
    bot_nick_name = ""

    irc = IRC()
    irc.connect(server, channel, bot_nick_name)

    irc.quit()


if __name__ == "__main__":
    main()
