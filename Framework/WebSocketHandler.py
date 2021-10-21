import websocket
from websocket import create_connection, _exceptions
from Framework.LogHandler import *


class WebSocketHandler:

    def __init__(self):
        self.ws = None

    def __connect_to_ws(self, base_url: str, port: int, timeout=5.0) -> websocket.WebSocket:
        """
        This method is used to connect with the WebSocket
        :param base_url: String,  Base url for connection
        :param port: Int, Port number
        :param timeout: Timeout for request
        :return: WebSocket Object
        """
        try:
            url = f"ws://{base_url}:{port}"
            if self.ws is not None:
                return self.ws
            return create_connection(url, timeout=timeout)
        except _exceptions.WebSocketTimeoutException as time_out:
            print_error_log(f"WebSocketTimeoutException, Connection not happened after wait for {timeout} seconds, "
                            f"EXCEPTION: {time_out}")
        except Exception as exp:
            print_error_log(f"Error to connect with WebSocket, EXCEPTION: {exp}")

    def send_value_to_ws(self, base_url: str, port: int, value, timeout=5.0):
        """
        This method is used to send and receive the data from WebSocket
        :param base_url: String,  Base url for connection
        :param port: Int, Port number
        :param value: Value in string which need to be send
        :param timeout: Timeout for request
        :return: Response from the WebSocket
        """
        try:
            self.ws = self.__connect_to_ws(base_url, port, timeout)
            if self.ws is not None:
                value = str(value)
                self.ws.send(value)
                return self.ws.recv()
        except Exception as exp:
            print_error_log(f"Error to send the data to WS, EXCEPTION: {exp}")

    def close_ws_connection(self):
        """
        This method is used to close the WS connection
        :return: None
        """
        try:
            if self.ws is not None:
                self.ws.close()
        except Exception as exp:
            print_error_log(f"Error to close the WS connection, EXCEPTION: {exp}")

    def perform_load_on_ws(self, base_url: str, port: int, value: bytes, num_req: int, timeout=5.0):
        """
        This method is used to perform the load on the WebSocket. It will send number of continuous request
         on the provided url. User need to pass the How much requests need to be send.
        :param base_url: User need to provide the base URL to this method for sending the HTTP request. Like localhost, 127.0.0.1 etc.
        :param port: Int, Port number for communication
        :param value: Value which need to be send.
        :param num_req: Number of request which need to be send
        :param timeout: Time out for one request.
        :return: Return true if all the request are fine
        """
        try:
            flg = False
            for i in range(0, num_req):
                try:
                    rec = self.send_value_to_ws(base_url=base_url, port=port, value=value, timeout=timeout)
                    assert float(rec) == self.calculate_cube_root(
                        value), "Invalidate response, Wrong cube root value send by WebSocket"
                except AssertionError as err:
                    flg = True
                    print_error_log(f"Error when sending the WebSocket request number: {i}, EXCEPTION: {err}")
                except Exception as exp:
                    flg = True
                    print_error_log(f"Error to send the WebSocket request number: {i}, EXCEPTION: {exp}")
            self.close_ws_connection()
            if flg:
                print_debug_log(f"It seems some request are not send response properly. Please check logs.")
                return False
            return True
        except Exception as exp:
            print_error_log(f"Error to perform load on TCP on port {port}, EXCEPTION: {exp}")
        finally:
            self.close_ws_connection()

    def calculate_cube_root(self, value):
        """
        Calculate the cube root and return the value
        :param value: Value which cube root.
        :return: cube root of the value
        """
        try:
            if value > 0:
                return round(value ** (1 / 3), 3)
            if value < 0:
                value = -pow(abs(value), float(1) / 3)
                return round(value, 3)
        except Exception as exp:
            print_error_log(f"Error to find the cube root of {value}, EXCEPTION:{exp}")
