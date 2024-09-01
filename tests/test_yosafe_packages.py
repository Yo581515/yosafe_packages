from yosafe_packages import yosafe_subpackage_1
from yosafe_packages import yosafe_subpackage_2
from yosafe_packages import yosafe_subpackage_3


def test_yosafe_packages():
    assert yosafe_subpackage_1.yosafe_add(1, 2) == 3
    assert yosafe_subpackage_2.yosafe_sub(2, 1) == 1
    assert yosafe_subpackage_3.yosafe_mul(2, 3) == 6
