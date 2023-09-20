import os
from multiprocessing import Process

import pytest


def main(path, dev, install):
    pytest.main(['%s' % path, '--device=%s' % dev, '--install=%s' %install, '--html=report.html', '--self-contained-html', '--capture=sys'])
    # pytest testcase\大回归\小回归\冒烟\ --device emulator-5554  --install 3 --html=report.html --self-contained-html --capture=sys

if __name__ == '__main__':
    # 大回归
    test_case = Process(target=main, args=("E:\proj\\atxAuto\\testcase\\大回归\\小回归\\冒烟", "emulator-5554", "1"))
    test_case.start()
    # test_case.join()
    # 小回归
    # test_case2 = Process(target=main, args=("E:\proj\\atxAuto\\testcase\\大回归\\小回归\\冒烟1", "ZL9LC685V86DNNMN", "2"))
    # test_case2.start()

    test_case.join()
    # test_case2.join()
    # 冒烟
    ...
