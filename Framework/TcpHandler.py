import socket
from typing import List

from Framework.LogHandler import *


class TcpHandler:
    """
    This class handle the TCP communication using Socket Communication
    """

    def __init__(self):
        self.socket_obj = None

    def __connect_to_tcp_port(self, base_url: str, port: int, timeout=5.0) -> socket:
        """
        This method is a private method and used to connect with the TCP server.
        Its take base url and port to connect with the TCP socket
        :param base_url: base url for connecting with TCP like localhost, 127.0.0.1
        :param port: Port number in which TCP communicated
        :param timeout: timeout for request
        :exception: Handle two exception
            1. socket.error -> If any error related to socket comes
            2. Exception -> Generic Exception
        :return: socket object
        """
        try:
            # check if connection is already there or not
            if self.socket_obj is not None:
                print_debug_log("Object already there")
                return self.socket_obj
            print_debug_log("Object  not there")
            # creating socket object
            self.socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_obj.settimeout(timeout)
            # connect with given port
            self.socket_obj.connect((base_url, port))
            # return socket object
            return self.socket_obj
        except socket.error as err:
            print_error_log(f"SocketError, EXCEPTION: {err}")
            return None
        except Exception as exp:
            print_error_log(f"Error to connect with TCP socket, EXCEPTION: {exp}")

    def send_value_to_tcp(self, base_url: str, port: int, value: bytes, timeout=5.0) -> str:
        """
        This method is send the data to the given TCP port.
        :param base_url: base url for connecting with TCP like localhost, 127.0.0.1
        :param port: Port number in which TCP communicated
        :param value: Value which need to be send, It should be in bytes format.
            please pass like:
                receive = tcp_handler.send_value_to_tcp(base_url="127.0.0.1", port=9000, value=b'0', timeout=5.0)
                                    or
                receive = tcp_handler.send_value_to_tcp(base_url="127.0.0.1", port=9000, value="0".encode(), timeout=5.0)
        :param timeout: timeout for request
        :exception: Handle two exception
            1. socket.error -> If any error related to socket comes
            2. Exception -> Generic Exception
        :return: Data which is received as response, String format
        """
        try:
            print_debug_log(f"Sending TCU request to url: {base_url}:{port}")
            # send the connection request
            s = self.__connect_to_tcp_port(base_url=base_url, port=port, timeout=timeout)
            if s is not None:
                # send the value to socket
                s.send(value)
                # return the receive data
                return s.recv(1024).decode("utf-8")
        except Exception as exp:
            print_error_log(f"Error to send the {value} to tcp port, EXCEPTION: {exp}")

    def split_receive_value(self, value) -> List:
        """
        This method is used to split the valye into list.
        for eg:
            a = "%4.0&"
            output: ["%", "4", ".", "0", "&"]
        :param value: String value
        :return: List of Char
        """
        try:
            char_list = []
            for char in value:
                char_list.append(char)
            return char_list
        except Exception as exp:
            print_error_log(f"Error to split the value, EXCEPTION:{exp}")

    def close_socket_connection(self):
        """
        This method close the socket connection if open
        :return: None
        """
        try:
            # close the TCP connection
            if self.socket_obj is not None:
                print_info_log(f"Closing TCP connection....")
                self.socket_obj.close()
        except Exception as exp:
            print_error_log(f"Error to close the TCP connection, EXCEPTION: {exp}")

    def perform_load_on_tcp(self, base_url: str, port: int, value: bytes, num_req: int, timeout=5.0):
        """
        This method is used to perform the load on the WebSocket. It will send number of continuous request
        on the provided url. User need to pass the How much requests need to be send.
        :param base_url: User need to provide the base URL to this method for sending the HTTP request. Like localhost, 127.0.0.1 etc.
        :param port: Int, Port number for communication
        :param value: Value which need to be send.
        :param num_req: Number of request which need to be send
        :param timeout: Time out for one request.
        :return: Return true if all the request are fine Otherwise return false.
        """
        try:
            flg = False
            for i in range(0, num_req):
                try:
                    rec = self.send_value_to_tcp(base_url=base_url, port=port, value=value, timeout=timeout)
                    assert rec[0] == "%"
                    assert rec[-1] == "&"
                except AssertionError as err:
                    flg = True
                    print_error_log(f"Error when sending the TCP request, EXCEPTION: {err}")
                except Exception as exp:
                    flg = True
                    print_error_log(f"Error to send the TCU request number: {i}, EXCEPTION: {exp}")
            if flg:
                print_debug_log(f"It seems some request are not send response properly. Please check logs.")
                return False
            return True
        except Exception as exp:
            print_error_log(f"Error to perform load on TCP on port {port}, EXCEPTION: {exp}")
        finally:
            self.close_socket_connection()
