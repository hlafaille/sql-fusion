class ColumnExistsException(Exception):
    pass


class DuplicateDataclassException(Exception):
    pass


class CommandNotFoundException(Exception):
    pass


class ProjectNotFoundException(Exception):
    pass


class CompiledFileNotFoundException(Exception):
    def __init__(self, passed_file_name):
        self.passed_file_name = passed_file_name

    def __str__(self):
        return self.passed_file_name