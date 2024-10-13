from core.framework import test
from log.logger import Logger
from api.http import api
from api.mock import mock_api
from asserts.asserts import Assert, HttpAssert

logger = Logger()

class TestLogin:
    @test
    @mock_api(status_code=200, content='登录成功', json_data={
        'success': True,
        'token': '1234567890'
    })
    @api(method='POST', url='https://api_v2.com/login')
    def login(self, status_code, response_content, response_json):
        logger.info('测试登录')
        Assert.equal(status_code, 200)
        logger.info(f"status code: {status_code}")
        logger.info(f"response content: {response_content}")
        if response_json:
            logger.info(f"json response: {response_json}")
        Assert.is_not_none(response_json['token'])
        return {'token': response_json['token']}

    
    @test
    @mock_api(status_code=200,content='登出成功', json_data={'success': True,'message': '登出成功'})
    @api(method='POST', url='https://api_v2.com/logout', headers={'Authorization': 'Bearer ${token}'})
    def logout(self, status_code, response_content, response_json):
        logger.info('测试登出')
        Assert.equal(status_code, 200)
        logger.info(f"status code: {status_code}")
        logger.info(f"response content: {response_content}")