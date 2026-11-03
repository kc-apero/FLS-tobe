def pytest_addoption(parser):
    parser.addoption("--update-golden", action="store_true",
                     help="ghi lai anh chup DDL/ERD")
