import logging


def test_001(driver):
    driver.app_start("com.jianshu.haruki")
    driver(resourceId="com.jianshu.haruki:id/tv_tab_title", text="推荐").click()
    driver(resourceId="com.jianshu.haruki:id/tv_tab_title", text="专题").click()