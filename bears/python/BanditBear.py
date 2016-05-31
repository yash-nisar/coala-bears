from coalib.bearlib.abstractions.Linter import linter
from coalib.settings.Setting import typed_list


@linter(executable='bandit',
        output_format='regex',
        output_regex=r'(?P<message>(?P<origin>(?:B\d+[,-]?)+): .*)')
class PyLintBear:
    """
    Performs security analysis on Python source code, utilizing the ast module
    from the Python standard library.
    """
    LANGUAGES = ("Python", "Python 2", "Python 3")

    @staticmethod
    def create_arguments(filename, file, config_file,
                         bandit_skipped_tests: typed_list(str)=
                         ["B105", "B106", "B107", "B404", "B603", "B606",
                          "B607"]):
        """
        :param bandit_skipped_tests:
            The IDs of the tests bandit shall not perform.
        """
        args = (filename,)

        if bandit_skipped_tests:
            args += ("-s", ",".join(bandit_skipped_tests))

        return args
