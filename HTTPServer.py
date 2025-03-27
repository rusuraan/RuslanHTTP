import os
import socket

from HTTPRequest import HTTPRequest
from HTTPResponse import HTTPResponse
from TCPServer import TCPServer


class HTTPServer(TCPServer):
    def __init__(self, host: str = "127.0.0.1", port: int = 8080):
        super().__init__(host, port)
        self.document_root = "./www"
        os.makedirs(self.document_root, exist_ok=True)

    def handle_connection(self, conn: socket.socket, addr: tuple) -> None:
        """
        Handles the incoming HTTP request.
        """
        raw_request = self.get_raw_request(conn)
        request = HTTPRequest(raw_request, conn)

        self.handle_request(request)

        print(f"Handled connection from {addr}")

    def get_raw_request(self, conn: socket.socket) -> bytearray:
        """
        Reads the entire HTTP request from the socket.
        """
        HTTP_HEADER_END = b"\r\n\r\n"

        raw_request = bytearray()

        while chunk := conn.recv(self.buffer_size):
            raw_request.extend(chunk)
            if HTTP_HEADER_END in raw_request:
                break
        return raw_request

    def handle_request(self, request: HTTPRequest) -> None:
        """
        Fulfills the given HTTP request.
        """
        response = HTTPResponse(request.source)

        # Only handle GET requests
        if request.method != "GET":
            response.send(404, "Method Not Supported")
            return

        # Normalize path
        target = "/index.html" if request.target == "/" else request.target
        file_path = os.path.join(self.document_root, target.lstrip("/"))

        try:
            with open(file_path, "r") as f:
                body = f.read()
            response.send(200, body)
        except FileNotFoundError:
            response.send(404, "File Not Found")
        except Exception:
            response.send(500, "Internal Server Error")


if __name__ == "__main__":
    server = HTTPServer()
    server.start()
