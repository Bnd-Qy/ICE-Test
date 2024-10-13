from core.framework import TestContext

# 运行测试
if __name__ == '__main__':
    test_context=TestContext()
    test_context.scan_and_register('test_case')
    test_context.run_tests()


