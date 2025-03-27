import socket

from HTTPRequest import HTTPRequest
from TCPServer import TCPServer


class HTTPServer(TCPServer):
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
        pass


if __name__ == "__main__":
    server = HTTPServer()
    server.start()
