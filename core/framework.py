import inspect
from functools import wraps
import time
from datetime import timedelta

class ColoredOutput:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'

    @staticmethod
    def red(text):
        return f"{ColoredOutput.RED}{text}{ColoredOutput.ENDC}"

    @staticmethod
    def green(text):
        return f"{ColoredOutput.GREEN}{text}{ColoredOutput.ENDC}"

    @staticmethod
    def yellow(text):
        return f"{ColoredOutput.YELLOW}{text}{ColoredOutput.ENDC}"

    @staticmethod
    def blue(text):
        return f"{ColoredOutput.BLUE}{text}{ColoredOutput.ENDC}"

class TestResult:
    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.execution_time = timedelta()

    @property
    def pass_rate(self):
        return (self.passed_tests / self.total_tests) * 100 if self.total_tests > 0 else 0
    
class TestCase:
    def __init__(self, cls):
        self.cls = cls
        self.setup_method = None
        self.teardown_method = None
        self.setup_class_method = None
        self.teardown_class_method = None
        self.test_methods = []
        self._parse_methods()

    def _parse_methods(self):
        for name, method in inspect.getmembers(self.cls):
            if hasattr(method, '_test_decorator'):
                if method._test_decorator == 'test':
                    self.test_methods.append(method)
                elif method._test_decorator == 'setup':
                    self.setup_method = method
                elif method._test_decorator == 'teardown':
                    self.teardown_method = method
                elif method._test_decorator == 'setup_class':
                    self.setup_class_method = method
                elif method._test_decorator == 'teardown_class':
                    self.teardown_class_method = method

    def run(self):
        instance = self.cls()
        result = {'total': len(self.test_methods), 'passed': 0, 'failed': 0}
        
        if self.setup_class_method:
            self.setup_class_method(instance)
        
        for test_method in self.test_methods:
            if self.setup_method:
                self.setup_method(instance)
            try:
                test_method(instance)
                result['passed'] += 1
            except Exception as e:
                result['failed'] += 1
                print(f"Test {test_method.__name__} failed: {str(e)}")
            
            if self.teardown_method:
                self.teardown_method(instance)
        
        if self.teardown_class_method:
            self.teardown_class_method(instance)

        return result

def test(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"\033[92m[+] Executing Test: {func.__name__}\033[0m")  # Print test case name in green
        return func(*args, **kwargs)
    wrapper._test_decorator = 'test'
    return wrapper



def setup(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper._test_decorator = 'setup'
    return wrapper

def teardown(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper._test_decorator = 'teardown'
    return wrapper

def setup_class(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper._test_decorator = 'setup_class'
    return wrapper

def teardown_class(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper._test_decorator = 'teardown_class'
    return wrapper

def get_class_package(cls):
    # Get the module of the class
    module = inspect.getmodule(cls)
    
    # Get the full name of the module
    module_name = module.__name__
    
    # Split the module name to get the package
    package = module_name.split('.')[0]
    
    return package

class TestContext:
    def __init__(self):
        self.test_cases = []
        self.test_result = TestResult()

    def scan_and_register(self, package_name):
        import importlib
        import pkgutil
        
        package = importlib.import_module(package_name)
        for _, module_name, _ in pkgutil.iter_modules(package.__path__):
            print(f"package_name:{package_name}, module_name:{module_name}")
            module = importlib.import_module(f'{package_name}.{module_name}')
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, object) and obj != object and get_class_package(obj).startswith(package_name):
                    self.test_cases.append(TestCase(obj))

    def run_tests(self):
        start_time = time.time()
        for test_case in self.test_cases:
            case_result = test_case.run()
            self.test_result.total_tests += case_result['total']
            self.test_result.passed_tests += case_result['passed']
            self.test_result.failed_tests += case_result['failed']
        end_time = time.time()
        self.test_result.execution_time = timedelta(seconds=end_time - start_time)
        self._print_report()

    def _print_report(self):
        print("\n===== ICE Test Report =====")
        print(f"Total tests: {ColoredOutput.blue(self.test_result.total_tests)}")
        print(f"Passed tests: {ColoredOutput.green(self.test_result.passed_tests)}")
        print(f"Failed tests: {ColoredOutput.red(self.test_result.failed_tests)}")
        print(f"Pass rate: {ColoredOutput.yellow(f'{self.test_result.pass_rate:.2f}%')}")
        print(f"Execution time: {ColoredOutput.blue(self.test_result.execution_time)}")
        print("===========================\n")




def ignore(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return None
    wrapper._test_decorator = 'ignore'
    return wrapper

def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                result = func(*args, **kwargs)
                results.append(result)
            return results
        wrapper._test_decorator = 'repeat'
        wrapper._repeat_times = times
        return wrapper
    return decorator


def data(*test_data):
    def decorator(func):
        @wraps(func)
        def wrapper(self):
            results = []
            for data_set in test_data:
                if isinstance(data_set, (list, tuple)):
                    result = func(self, *data_set)
                elif isinstance(data_set, dict):
                    result = func(self, **data_set)
                else:
                    result = func(self, data_set)
                results.append(result)
            return results
        wrapper._test_decorator = 'data'
        wrapper._test_data = test_data
        return wrapper
    return decorator

import time
import functools

def time_test(timeout):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = None
            def run_func():
                nonlocal result
                result = func(*args, **kwargs)
            import threading
            thread = threading.Thread(target=run_func)
            thread.start()
            thread.join(timeout)
            
            if thread.is_alive():
                raise TimeoutError(ColoredOutput.red(f"testcase:{func.__name__} exceeded the time limit of {timeout} seconds"))
            
            end_time = time.time()
            execution_time = end_time - start_time
            print(ColoredOutput.green(f"testcase:{func.__name__} completed in {execution_time:.2f} seconds"))
            return result
        
        wrapper._test_decorator = 'time_test'
        wrapper._timeout = timeout
        return wrapper
    return decorator



