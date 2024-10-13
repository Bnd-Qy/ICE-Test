from api.http import api
from api.local_variable import cache_http_response,\
    get_cached_http_response,cache_http_response,cache,cache_ware
from core.framework import test,setup,time_test,teardown,setup_class,teardown_class,ignore,repeat,time_test
from api.parse import JsonParser
from log.logger import Logger

logger = Logger()

__author__='冰点契约'

class TestApi:
    @setup_class
    def init_env(self):
        logger.info('初始化环境')

    @setup
    def setup_method(self):
        logger.info('前置方法')

    @time_test(timeout=1)
    def test_timeout(self):
        logger.info('测试超时')
        time.sleep(2)

    @repeat(times=3)
    def repeat_test(self):
        logger.info('重复测试')

    @test
    @ignore
    @cache
    @api(method='GET', url='https://www.baidu.com')
    def get_users(self, status_code, response_content, response_json):
        logger.info(f"status code: {status_code}")
        logger.info(f"response content: {response_content}")
        if response_json:
            logger.info(f"json response: {response_json}")
        return {'json': response_json}

    @test
    @ignore
    @cache_ware
    def get_users2(self, json=None):
        logger.info(f"cached json data: {json}")
        json_parser=JsonParser(json_data=json)
        logger.info(f"json parser: {json_parser.address.city}")
    

    @ignore
    def ignore_test(self):
        logger.info('忽略测试')

    @teardown
    def teardown_method(self):
        logger.info('后置方法')

    def clean_up(self):
        logger.info('清理环境')
