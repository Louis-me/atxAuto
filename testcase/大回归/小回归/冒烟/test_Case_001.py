import os
import time
import pytest

class TestCase(object):
    @pytest.mark.finished
    def test_001(self, driver):
        driver.app_start("com.jianshu.haruki")
        driver(resourceId="com.jianshu.haruki:id/tv_tab_title", text="推荐").click()
        driver(resourceId="com.jianshu.haruki:id/tv_tab_title", text="小岛").click()
    def test1_001(self, driver):
        driver.app_start("com.jianshu.haruki")
        driver(resourceId="com.jianshu.haruki:id/ll_notification1").click()
