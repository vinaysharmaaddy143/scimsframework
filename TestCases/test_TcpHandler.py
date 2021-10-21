from typing import List

from Framework.TcpHandler import TcpHandler
import re
from Framework.LogHandler import *

tcp_handler = TcpHandler()


def test_send_valid_number():
    receive = tcp_handler.send_value_to_tcp(base_url="127.0.0.1", port=9000, value=b'8', timeout=5.0)
    receive = tcp_handler.split_receive_value(receive)
    assert receive[0] == "%"
    assert receive[-1] == "&"
    assert float("".join(receive[1:-1])) == 64.0


def test_send_valid_large_number():
    receive = tcp_handler.send_value_to_tcp(base_url="127.0.0.1", port=9000, value=b'15542', timeout=5.0)
    receive = tcp_handler.split_receive_value(receive)
    assert receive[0] == "%", "% is not in Response"
    assert receive[-1] == "&", "& is not in Response"
    assert float("".join(receive[1:-1])) == pow(15542, 2), "Response not contain the power of 15542"
    print_info_log(f"Response: {float(''.join(receive[1:-1]))}")


def test_send_double_number():
    receive = tcp_handler.send_value_to_tcp(base_url="127.0.0.1", port=9000, value=b'2.2', timeout=5.0)
    receive = tcp_handler.split_receive_value(receive)
    assert receive[0] == "%", "% is not in Response"
    assert receive[-1] == "&", "& is not in Response"
    assert float("".join(receive[1:-1])) != pow(2.2, 2), "Invalid Response, Microservice only take number not double"
    print_info_log(f"Response: {float(''.join(receive[1:-1]))}")


def test_send_string_value():
    receive = tcp_handler.send_value_to_tcp(base_url="127.0.0.1", port=9000, value="10".encode(), timeout=5.0)
    receive = tcp_handler.split_receive_value(receive)
    assert receive[0] == "%", "% is not in Response"
    assert receive[-1] == "&", "& is not in Response"
    assert float(''.join(receive[1:-1])) != pow(10, 2), "Invalid Response," \
                                                        " Microservice only take number not string value"
    print_info_log(f"Response: {float(''.join(receive[1:-1]))}")


def test_send_negative_value():
    receive = tcp_handler.send_value_to_tcp(base_url="127.0.0.1", port=9000, value=b'-18', timeout=5.0)
    receive = tcp_handler.split_receive_value(receive)
    assert receive[0] == "%", "% is not in Response"
    assert receive[-1] == "&", "& is not in Response"
    assert float(''.join(receive[1:-1])) == pow(-18,
                                                2), "Invalid Response, Microservice should send values as power of -18"
    print_info_log(f"Response: {float(''.join(receive[1:-1]))}")


def test_send_zero_value():
    receive = tcp_handler.send_value_to_tcp(base_url="127.0.0.1", port=9000, value=b'0', timeout=5.0)
    receive = tcp_handler.split_receive_value(receive)
    assert receive[0] == "%", "% is not in Response"
    assert receive[-1] == "&", "& is not in Response"
    assert float(''.join(receive[1:-1])) == pow(0,
                                                2), "Invalid Response, Microservice should send values as power of 0"
    print_info_log(f"Response: {float(''.join(receive[1:-1]))}")


def test_invalidate_response():
    receive = tcp_handler.send_value_to_tcp(base_url="127.0.0.1", port=9000, value=b'', timeout=10.0)
    assert receive is None, "Invalid response, Microservice returning value for empty request"


def performance_test():
    status = tcp_handler.perform_load_on_tcp(base_url="127.0.0.1", port=9000, value=b'10', num_req=500000, timeout=10.0)
    assert status, "Some requests not respond properly"


tcp_handler.close_socket_connection()
