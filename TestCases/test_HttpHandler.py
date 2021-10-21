from Framework.HttpHandler import HttpHandler


def send_get_request_with_params(params):
    http_handler = HttpHandler()
    response = http_handler.send_get_request(base_url="127.0.0.1", paths="/number", port=8080, params=params)
    return response


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def test_valid_double_number():
    params = {
        "number": 2.2
    }
    response = send_get_request_with_params(params=params)
    assert response.status_code == 200
    assert isclose(float(response.text), 1.483239697)


def test_pass_int_value():
    params = {
        "number": 2
    }
    response = send_get_request_with_params(params=params)
    assert response.status_code == 200
    assert isclose(float(response.text), 0.0)


def test_pass_string_value():
    params = {
        "number": '2'
    }
    response = send_get_request_with_params(params=params)
    assert response.status_code == 200
    assert "0.0" in response.text


def test_zero_value():
    params = {
        "number": 0.0
    }
    response = send_get_request_with_params(params=params)
    assert response.status_code == 200
    assert float(response.text) == 0.0


def test_pass_negative_value():
    params = {
        "number": -1
    }
    response = send_get_request_with_params(params=params)
    assert response.status_code == 200
    assert response.text == "NaN"


def performance_test():
    params = {
        "number": 20
    }
    http_request = HttpHandler()
    status = http_request.perform_load(base_url="127.0.0.1", port=8080, paths="/number", num_req=50000, params=params,
                                       method="GET", timeout=5.0)
    assert status, "Some request not response proerly"