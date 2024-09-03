from yosafe_packages.yosafe_subpackage_1.yosafe_subpackage_1_functions import *
from yosafe_packages.yosafe_subpackage_1.yosafe_subpackage_1_functions_2 import *
from yosafe_packages.yosafe_subpackage_2.yosafe_subpackage_2_functions import *
from yosafe_packages.yosafe_subpackage_3.yosafe_subpackage_3_functions import *

def test_yosafe_packages():
    result = yosafe_get_yosafe_subpackage_1()
    print(result)
    assert "Error" not in result

def test_yosafe_packages_2():
    result = yosafe_get_yosafe_subpackage_2()
    print(result)
    assert "Error" not in result

def test_yosafe_packages_3():
    result = yosafe_get_yosafe_subpackage_3()
    print(result)
    assert "Error" not in result