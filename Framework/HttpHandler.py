from typing import Dict
from requests import Response
import requests
from Framework.LogHandler import *


class HttpHandler:
    """
    This class is used to handle the HTTP requests
    """

    def __init__(self):
        pass

    def send_get_request(self, base_url: str, paths: str, port: int, params: Dict, header: dict = None,
                         timeout: float = 5.0) -> Response:
        """
        This method send the GET request to provided base url and port number with parameters.
        :param base_url: String, Base URL of the request like localhost, 127.0.0.1 etc.
        :param paths: String, path in url
        :param port: Int, Port number for communication
        :param params: Dictionary, parameters need to be pass
        :param header: Dictionary, Headers which need to add inside request.
        :param timeout: Timeout for request
        :exception: This method handle two exception
            1. requests.exceptions.Timeout -> For request time out
            2. Exception -> Generic Exception
        :return: Response Object.
        """
        # creating URL
        url = f"http://{base_url}:{port}{paths}"
        try:
            print_debug_log(f"Sending request to: {url}, params: {params}")
            # sending get request with params
            res = requests.get(url, params=params, headers=header, timeout=timeout)
            # return response
            return res
        except requests.exceptions.Timeout as time_out:
            print_error_log(f"GET request for url: {url} timeout, EXCEPTION: {time_out}")
        except Exception as exp:
            print_error_log(f"Error to send the get request to {url}, EXCEPTION: {exp}")

    def send_post_request(self, base_url: str, paths: str, port: int, data: Dict, header=None,
                          timeout: float = 5.0) -> Response:
        """
        This method send the POST request to provided base url and port number with data.
        :param base_url: String, Base URL of the request like localhost, 127.0.0.1 etc.
        :param paths: String, path in url
        :param port: Int, Port number for communication
        :param date: Dictionary, data which need to be send with POST request
        :param header: Dictionary, Headers which need to add inside request.
        :param timeout: Timeout for request
        :exception: This method handle two exception
            1. requests.exceptions.Timeout -> For request time out
            2. Exception -> Generic Exception
        :return: Response Object.
        """
        url = f"http://{base_url}:{port}{paths}"  # creating url
        try:
            # send post request
            res = requests.post(url, data=data, headers=header, timeout=timeout)
            # return response
            return res
        except requests.exceptions.Timeout as time_out:
            print_error_log(f"POST request for url: {url} timeout, EXCEPTION: {time_out}")
        except Exception as exp:
            print_error_log(f"Error yo send the POST request on {url}, EXCEPTION: {exp}")

    def send_delete_request(self, base_url: str, paths: str, port: int, headers=None, timeout: float = 5.0) -> Response:
        """
        This method send the Delete request to provided base url and port number.
        :param base_url: String, Base URL of the request like localhost, 127.0.0.1 etc.
        :param paths: String, path in url
        :param port: Int, Port number for communication
        :param headers: Dictionary, Headers which need to add inside request.
        :param timeout: Timeout for request
        :exception: This method handle two exception
            1. requests.exceptions.Timeout -> For request time out
            2. Exception -> Generic Exception
        :return: Response Object.
        """
        # creating URL
        url = f"http://{base_url}:{port}{paths}"
        try:
            # sending DELETE request
            res = requests.delete(url, headers=headers, timeout=timeout)
            # return response
            return res
        except requests.exceptions.Timeout as time_out:
            print_error_log(f"DELETE request for url: {url} timeout, EXCEPTION: {time_out}")
        except Exception as exp:
            print_error_log(f"Error to send the DELETE request on {url}, EXCEPTION: {exp}")

    def perform_load(self, base_url: str, port: int, paths: str, num_req: int, method: str = "GET", **kwargs):
        """
        This method is used to perform the load on HTTP port. User need to pass the num_req which is a number of request
        :param base_url: Base url of the HTTP
        :param port: HTTP port on which user need to send the request
        :param paths: path of the HTTP request
        :param num_req: Number of request which need to be send
        :param method: HTTP methods like GET POST DELETE
        :param kwargs: Other argument pleas check doc of HTTP methods.
        :return: True if all response are proper otherwise false.
        """
        url = f"http://{base_url}:{port}/{paths}"
        try:
            flg = False
            for i in range(0, num_req):
                try:
                    if method.upper() == "GET":
                        response = self.send_get_request(base_url=base_url, paths=paths, port=port,
                                                         params=kwargs["params"], timeout=kwargs["timeout"])
                        assert response.status_code == 200
                        assert self.isclose(float(response.text), float(kwargs["params"]))
                    if method.upper() == "POST":
                        response = self.send_post_request(base_url=base_url, paths=paths, port=port,
                                                          data=kwargs["data"], timeout=kwargs["timeout"])
                        assert response.status_code == 200
                    if method.upper() == "DELETE":
                        response = self.send_delete_request(base_url=base_url, paths=paths, port=port,
                                                            timeout=kwargs["timeout"])
                        assert response.status_code == 200
                except AssertionError as assert_error:
                    flg = True
                    print_error_log(f"For cycle {i} in performance of HTTP url {url}, EXCEPTION: {assert_error}")
                except Exception as exp:
                    flg = False
                    print_error_log(f"For cycle: {i} in HTTP uRl testing, EXCEPTION: {exp}")
            if flg:
                print_debug_log(f"It seems some request are not send response properly. Please check logs.")
                return False
            return True
        except Exception as exp:
            print_error_log(f"Error to perform the load on HTTP url: {url}, EXCEPTION: {exp}")

    def isclose(self, a, b, rel_tol=1e-09, abs_tol=0.0):
        """
        This method find the close off value of square root.
        :param a: first value
        :param b: second value
        :return: close of value in flot.
        """
        return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)
