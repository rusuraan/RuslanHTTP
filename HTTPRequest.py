from socket import socket


class HTTPRequest:
    def __init__(self, raw_request: bytearray, source: socket):
        self.source: socket = source
        self.method: str = ""
        self.target: str = ""
        self.protocol: str = "HTTP/1.1"  # Targeting HTTP/1.1 only
        self.headers: dict = {}
        self.body: str = ""

        self.parse_request(raw_request)

    def parse_request(self, raw_request: bytearray) -> None:
        """
        Reads a raw HTTP request, and sets the attributes accordingly
        """
        http_message = raw_request.decode()

        lines = http_message.split("\r\n")

        # Parse request line
        request_line = lines[0].split()
        self.method, self.target, self.protocol = request_line

        # Parse headers
        index = 1
        while index < len(lines) and lines[index]:
            key, value = lines[index].split(": ", 1)
            self.headers[key] = value
            index += 1

        # Parse body
        if "" in lines:
            body_index = lines.index("") + 1
            self.body = "\n".join(lines[body_index:]) if body_index < len(lines) else ""


if __name__ == "__main__":
    pass
