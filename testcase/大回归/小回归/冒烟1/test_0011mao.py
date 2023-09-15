import logging
import time


def test_001(driver):
    driver.app_start("com.jianshu.haruki")
    time.sleep(3)
    driver(resourceId="com.jianshu.haruki:id/tv_tab_title", text="活动").click()
    driver(resourceId="com.jianshu.haruki:id/tv_tab_title", text="小岛").click()