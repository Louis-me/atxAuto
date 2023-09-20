# conftest.py
import logging
import threading

import pytest
from py._xmlgen import html
import uiautomator2 as u2
import time
import base64


def pytest_addoption(parser):
    #
    parser.addoption("--device", action="store", default="default device", help="None")
    # 1表示升级安装apk，2表示卸载后重新安装,3表示不做任何处理
    parser.addoption("--install", action="store", default="default install", help="None")


@pytest.fixture(scope="session")
def device(request):
    return request.config.getoption("--device")


def pytest_configure(config):
    # 在 pytest_configure 钩子函数中获取自定义选项的值
    install = config.getoption("--install")
    # 可以将获取到的数据存储在全局变量中，供其他钩子函数或测试中使用
    global install_type_s
    install_type_s = install


@pytest.fixture(scope='session', autouse=True)
def driver(device):
    logging.info("device=%s" % device)
    logging.info("install=%s" % install_type_s)

    d = u2.connect_usb(device)
    d.set_fastinput_ime(True)

    pkg = "com.jianshu.haruki"
    d.app_stop(pkg)
    apk_path = r"E:\proj\atxAuto\apk\com.jianshu.haruki_6.6.1_2023006061.apk"
    # 唤醒屏幕并上滑动解锁 手机设置不用密码锁
    scree_on(d)
    # 安装apk逻辑
    install_apk_flag(install_type_s, d, pkg, apk_path)
    # driver = d.session(pkg)
    # 返回数据
    yield d
    # 实现用例后置
    d.app_stop(pkg)


def install_apk_flag(install=3, d=None, pkg="", path=""):
    """

    :param install: 1,2,3
    :param d:
    :param pkg:
    :param path: apk path
    :return:
    """

    if install == "1":
        update_install(d, path)

    elif install == "2":
        uninstall_apk(d, pkg, path)

    else:
        print("不做任何处理")


def scree_on(d):
    """
    安卓唤醒屏幕和解锁
    :param d:
    :return:
    """
    device_info = d.info
    # 检查设备是否已被唤醒
    if device_info['screenOn']:
        logging.info("设备已唤醒")
    else:
        logging.info("设备未唤醒")
        # 唤醒屏幕
        d.press("power")
        time.sleep(2)
    app_cur = d.app_current()
    if app_cur["activity"].find("Launcher") > -1:
        logging.info("设备已经解锁不需要进行解锁操作")
    else:
        logging.info("开始进行解锁操作")
        # 执行向上滑动操作
        width, height = d.window_size()
        start_x = width // 2
        start_y = height * 3 // 4
        end_x = width // 2
        end_y = height // 4
        d.swipe(start_x, start_y, end_x, end_y)
        time.sleep(2)


def install_apk_(d, path):
    d.app_install(path)


def uninstall_apk(dr, pkg, path):
    try:
        dr.app_uninstall(pkg)
        time.sleep(3)
        logging.info("卸载应用成功")

    except Exception as e:
        logging.info("卸载应用失败")

    try:
        threading.Thread(target=install_apk_, args=(), kwargs={"d": dr, "path": path}).start()
        time.sleep(5)
        logging.info("----安装应用成功--------")

        num = 5
        while num > 0:
            time.sleep(1)
            # 安装app出现的提示
            logging.info("----弹框开始--------")

            if dr(resourceId="com.android.packageinstaller:id/two_buttons_layout").exists():
                dr(resourceId="com.android.packageinstaller:id/two_buttons_layout").click()
                logging.info("点击继续安装")
                time.sleep(2)
                dr.app_start(pkg)
                time.sleep(1)
            logging.info("弹框检查")
            if dr(resourceId="com.android.systemui:id/notification_allow").exists():
                dr(resourceId="com.android.systemui:id/notification_allow").click()
            if dr(resourceId="com.jianshu.haruki:id/tv_ok").exists():
                dr(resourceId="com.jianshu.haruki:id/tv_ok").click()
            num -= 1
    except Exception as e:
        logging.error(str(e))


def update_install(d, path):
    """
    直接覆盖安装
    :return:
    """

    threading.Thread(target=install_apk_, args=(), kwargs={"d": d, "path": path}).start()
    time.sleep(3)
    logging.info("----覆盖安装成功--------")
    # 安装app出现的提示
    num = 5
    while num > 0:
        time.sleep(1)
        logging.info("等待点击继续安装")
        try:
            if d(resourceId="com.android.packageinstaller:id/two_buttons_layout").exists():
                d(resourceId="com.android.packageinstaller:id/two_buttons_layout").click()
                num = 0
                logging.info("点击继续安装成功")
        except Exception as e:
            pass
        num -= 1


@pytest.mark.optionalhook
def pytest_html_results_summary(prefix):
    """
    #添加summary内容
    """
    prefix.extend([html.p("所属部门: 测试组")])
    prefix.extend([html.p("框架设计: XXX")])

    # @pytest.hookimpl(hookwrapper=True)
    # def pytest_runtest_makereport(item):
    """
    当测试失败的时候，自动截图，展示到html报告中
    :param item:
    """

    # pytest_html = item.config.pluginmanager.getplugin('html')
    # outcome = yield
    # report = outcome.get_result()
    #
    # report.description = str(item.function.__doc__)
    # extra = getattr(report, 'extra', [])
    #
    # if report.when == 'call' or report.when == "setup":
    #     xfail = hasattr(report, 'wasxfail')
    #     if (report.skipped and xfail) or (report.failed and not xfail):
    #         screen_img = _capture_screenshot()
    #         if screen_img:
    #             html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:1024px;height:768px;" ' \
    #                    'onclick="window.open(this.src)" align="right"/></div>' % screen_img
    #             extra.append(pytest_html.extras.html(html))
    #     report.extra = extra


def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('Description'))  # 表头添加Description
    cells.pop(-1)  # 删除link


def pytest_html_results_table_row(report, cells):
    """新增用例描述内容，来自于用例的注释"""
    cells.insert(1, html.td(report.description))  # 用例的描述
    cells.pop(-1)  # 删除link


def pytest_html_results_table_html(report, data):
    """
    去除执行成功用例的log输出
    """
    if report.passed:
        del data[:]
        data.append(html.div('通过的用例未捕获日志输出.', class_='empty log'))
    pass


def pytest_html_report_title(report):
    report.title = "pytest示例项目测试报告"


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    '''收集测试结果'''
    # print(terminalreporter.stats)
    passed = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    failed = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    error = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    # skipped = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    # print('成功率：%.2f' % (len(terminalreporter.stats.get('passed', []))/terminalreporter._numcollected*100)+'%')
    # terminalreporter._sessionstarttime 会话开始时间
    duration = time.time() - terminalreporter._sessionstarttime


def _capture_screenshot():
    """
    截图保存为base64
    :return:
    """
    # return _driver.get_screenshot_as_base64()
    return None
