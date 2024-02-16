import pytest

import msconsconverter as msconsconverter


def test_license():
    assert msconsconverter.__license__ == "MIT"
