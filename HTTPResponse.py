from socket import socket


class HTTPResponse:
    def __init__(self, conn: socket):
        self.conn: socket = conn

    def send(self, status_code: int, body: str = "") -> None:
        """
        Sends a simple HTTP response.
        """
        response = (
            f"HTTP/1.1 {status_code} {self._get_status_message(status_code)}\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(body)}\r\n"
            "Connection: close\r\n"
            "\r\n"
            f"{body}"
        )
        self.conn.sendall(response.encode())

    def _get_status_message(self, status_code: int) -> str:
        """
        Returns standard HTTP status messages.
        """
        status_messages = {200: "OK", 404: "Not Found", 500: "Internal Server Error"}
        return status_messages.get(status_code, "Unknown")
