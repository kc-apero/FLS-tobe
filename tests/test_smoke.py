def test_package_importable():
    """Phai la package THAT (co __init__.py), khong phai namespace package rong.

    Ban dau test chi assert fls.__name__ == "fls" -> xanh ngay ca khi chua co
    file nao, vi thu muc rong da la implicit namespace package (PEP 420).
    """
    import fls

    assert fls.__name__ == "fls"
    assert fls.__file__ is not None and fls.__file__.endswith("__init__.py")
