
from core.framework import ColoredOutput

class Assert:
    @staticmethod
    def _fail_message(message):
        return ColoredOutput.red(f"Assertion failed: {message}")

    @staticmethod
    def equal(actual, expected, message=None):
        if actual != expected:
            raise AssertionError(Assert._fail_message(message or f"Expected {expected}, but got {actual}"))

    @staticmethod
    def not_equal(actual, expected, message=None):
        if actual == expected:
            raise AssertionError(Assert._fail_message(message or f"Expected {actual} to be different from {expected}"))

    @staticmethod
    def true(condition, message=None):
        if not condition:
            raise AssertionError(Assert._fail_message(message or "Expected True, but got False"))

    @staticmethod
    def false(condition, message=None):
        if condition:
            raise AssertionError(Assert._fail_message(message or "Expected False, but got True"))

    @staticmethod
    def is_none(value, message=None):
        if value is not None:
            raise AssertionError(Assert._fail_message(message or f"Expected None, but got {value}"))

    @staticmethod
    def is_not_none(value, message=None):
        if value is None:
            raise AssertionError(Assert._fail_message(message or "Expected a non-None value"))

    @staticmethod
    def in_(item, collection, message=None):
        if item not in collection:
            raise AssertionError(Assert._fail_message(message or f"Expected {item} to be in {collection}"))

    @staticmethod
    def not_in(item, collection, message=None):
        if item in collection:
            raise AssertionError(Assert._fail_message(message or f"Expected {item} not to be in {collection}"))

    @staticmethod
    def instance(obj, cls, message=None):
        if not isinstance(obj, cls):
            raise AssertionError(Assert._fail_message(message or f"Expected instance of {cls}, but got {type(obj)}"))

    @staticmethod
    def raises(exception_type, callable_obj, *args, **kwargs):
        try:
            callable_obj(*args, **kwargs)
        except exception_type:
            return
        except Exception as e:
            raise AssertionError(Assert._fail_message(f"Expected {exception_type}, but {type(e)} was raised"))
        else:
            raise AssertionError(Assert._fail_message(f"Expected {exception_type}, but no exception was raised"))


class HttpAssert:
    @staticmethod
    def status_code(response, expected_status_code, message=None):
        if response.status_code != expected_status_code:
            raise AssertionError(Assert._fail_message(message or f"Expected status code {expected_status_code}, but got {response.status_code}"))

    @staticmethod
    def content_type(response, expected_content_type, message=None):
        actual_content_type = response.headers.get('Content-Type')
        if actual_content_type != expected_content_type:
            raise AssertionError(Assert._fail_message(message or f"Expected Content-Type '{expected_content_type}', but got '{actual_content_type}'"))

    @staticmethod
    def json_body(response, expected_json, message=None):
        try:
            actual_json = response.json()
        except ValueError:
            raise AssertionError(Assert._fail_message(message or "Response body is not valid JSON"))
        
        if actual_json != expected_json:
            raise AssertionError(Assert._fail_message(message or f"Expected JSON body {expected_json}, but got {actual_json}"))

    @staticmethod
    def header_present(response, header_name, message=None):
        if header_name not in response.headers:
            raise AssertionError(Assert._fail_message(message or f"Expected header '{header_name}' to be present"))

    @staticmethod
    def header_value(response, header_name, expected_value, message=None):
        actual_value = response.headers.get(header_name)
        if actual_value != expected_value:
            raise AssertionError(Assert._fail_message(message or f"Expected header '{header_name}' to have value '{expected_value}', but got '{actual_value}'"))

    @staticmethod
    def body_contains(response, expected_content, message=None):
        if expected_content not in response.text:
            raise AssertionError(Assert._fail_message(message or f"Expected response body to contain '{expected_content}'"))
