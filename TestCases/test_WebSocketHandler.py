from Framework.WebSocketHandler import WebSocketHandler
from Framework.LogHandler import *

ws = WebSocketHandler()


def calculate_cube_root(value):
    try:
        if value > 0:
            return round(value ** (1 / 3), 3)
        if value < 0:
            value = -pow(abs(value), float(1) / 3)
            return round(value, 3)
    except Exception as exp:
        print_error_log(f"Error to find the cube root of {value}, EXCEPTION:{exp}")


def test_send_valid_number():
    response = ws.send_value_to_ws(base_url="127.0.0.1", port=8090, value=64, timeout=5.0)
    assert float(response) == calculate_cube_root(64), "Invalidate response, Wrong cube root value send by WebSocket"


def test_send_large_number():
    response = ws.send_value_to_ws(base_url="127.0.0.1", port=8090, value=1540, timeout=5.0)
    assert round(float(response), 3) == calculate_cube_root(
        1540), "Invalidate response, Wrong cube root value send by WebSocket"


def test_send_negative_number():
    response = ws.send_value_to_ws(base_url="127.0.0.1", port=8090, value=-450, timeout=5.0)
    assert round(float(response), 3) == calculate_cube_root(
        -450), "Invalidate response, Wrong cube root value send by WebSocket"


def performance_test():
    status = ws.perform_load_on_ws(base_url="127.0.0.1", port=8090, value=5, num_req=50000, timeout=5.0)
    assert status, "Some request not response properly"


ws.close_ws_connection()
