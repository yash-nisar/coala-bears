import json

from coalib.bearlib.abstractions.Linter import linter
from coalib.settings.Setting import typed_list
from dependency_management.requirements.NpmRequirement import NpmRequirement
from dependency_management.requirements.PipRequirement import PipRequirement


@linter(executable='textlint',
        output_format='regex',
        output_regex=r'(?P<line>\d+):(?P<column>\d+)[\s*|✓]*(?P<severity>'
                     r'error|warning)\s+(?P<message>.+?)(?:  .*|\n|$)')
class TextLintBear:
    """
    The pluggable linting tool for text and markdown. It is similar to
    ESLint, but textlint for natural language.
    """

    LANGUAGES = {'HTML', 'Markdown', 'reStructuredText'}
    REQUIREMENTS = {NpmRequirement('textlint', '7.3.0'),
                    NpmRequirement('textlint-plugin-html', '0.1.5'),
                    NpmRequirement('textlint-plugin-rst', '0.1.1'),
                    NpmRequirement('textlint-rule-alex', '1.2.0'),
                    NpmRequirement('textlint-rule-common-misspellings',
                                   '1.0.1'),
                    NpmRequirement('textlint-rule-date-weekday-mismatch',
                                   '1.0.5'),
                    NpmRequirement('textlint-rule-ginger', '2.1.0'),
                    NpmRequirement('textlint-rule-max-comma', '1.0.4'),
                    NpmRequirement('textlint-rule-max-number-of-lines',
                                   '1.0.3'),
                    NpmRequirement('textlint-rule-ng-word', '1.0.0'),
                    NpmRequirement('textlint-rule-no-dead-link', '3.1.1'),
                    NpmRequirement('textlint-rule-no-empty-section', '1.1.0'),
                    NpmRequirement('textlint-rule-no-start-'
                                   'duplicated-conjunction', '1.1.3'),
                    NpmRequirement('textlint-rule-no-todo', '2.0.0'),
                    NpmRequirement('textlint-rule-period-in-list-item',
                                   '0.2.0'),
                    NpmRequirement('textlint-rule-rousseau', '1.4.5'),
                    NpmRequirement('textlint-rule-spellchecker', '2.1.0'),
                    NpmRequirement('textlint-rule-unexpanded-acronym',
                                   '1.2.1'),
                    NpmRequirement('textlint-rule-write-good', '1.6.0'),
                    PipRequirement('docutils-ast-writer', '0.1.2')}
    AUTHORS = {'The coala developers'}
    AUTHORS_EMAILS = {'coala-devel@googlegroups.com'}
    LICENSE = 'AGPL-3.0'
    CAN_DETECT = {'Formatting', 'Grammar', 'Spelling'}
    SEE_MORE = 'https://github.com/textlint/textlint'

    @staticmethod
    def generate_config(filename, file,
                        keyword_todo: bool=None,
                        no_start_duplicated_conjunction: bool=True,
                        no_empty_section: bool=True,
                        check_date_weekday_mismatch: bool=True,
                        check_grammar: bool=True,
                        max_lines_per_file: int=300,
                        max_comma_per_sentence: int=4,
                        check_no_good_words: typed_list(str)=[],
                        period_in_list_item: bool=True,
                        minimum_acronym_length: int=3,
                        maximum_acronym_length: int=5,
                        ignore_acronyms: typed_list(str)=[],
                        check_rousseau: bool=True,
                        check_offensive_expressions: bool=True,
                        check_common_misspellings: bool=True,
                        enable_spellchecker: bool=True,
                        write_good: bool=True,
                        check_invalid_links: bool=True,
                        textlint_config: str='',
                        ):
        """
        :param keyword_todo:
            This rule checks ``- [ ]`` (task lists).
        :param no_start_duplicated_conjunction:
            This rule checks whether your sentence starts with a duplicated
            conjunction.
        :param no_empty_section:
            This rule does not allow to create an empty section.
            For example, there is an empty section ``# Header B`` below:
            ```
            # Header A

            # Header B

            Text.
            ```
        :param check_date_weekday_mismatch:
            This rule finds a mismatch between a date and the corresponding
            weekday.
        :param check_grammar:
            This rule checks your English grammar with Ginger Proofreading.
        :param max_lines_per_file:
            Number of lines allowed per file.
        :param max_comma_per_sentence:
            Number of commas allowed per sentence.
        :param check_no_good_words:
            Set of NG (No Good) words to check for.
        :param period_in_list_item:
            This rule checks whether there is a period in a list item.
        :param minimum_acronym_length:
            Minimum length for the unexpanded acronym.
        :param maximum_acronym_length:
            Maximum length for the unexpanded acronym.
        :param ignore_acronyms:
            A list that contains the acronyms to ignore.
        :param check_rousseau:
            This rule checks English sentence using rousseau, which is a
            lightweight proofreader written in Javascript.
            The rule can check:
            - Passive voice
            - Lexical illusions – cases where a word is repeated
            - 'So' at the beginning of the sentence
            - Adverbs that can weaken meaning: really, very, extremely, etc.
            - Readibility of sentences
            - Simpler expressions
            - Weasel words
            - If a sentence is preceded by a space
            - If there is no space between a sentence and its ending
              punctuation
            - If sentences are starting with uppercase letter
        :param check_offensive_expressions:
            This rule helps you find gender favouring, polarising, race
            related, religion inconsiderate, or other unequal phrasing.
        :param check_common_misspellings:
            This rule helps to find common misspellings from Wikipedia's
            list of common misspellings.
        :param enable_spellchecker:
            This rule checks spellings with native spellcheckers, i.e.
             NSSpellChecker, Hunspell and Windows 8 Spell Check API.
        :param write_good:
            This rule checks your English styles with
            https://github.com/btford/write-good.
        :param check_invalid_links:
            This rule makes sure that every link in the document is
            available.
        """
        if textlint_config:
            return None
        else:
            options = {
                'no-todo': keyword_todo,
                'no-start-duplicated-conjunction':
                    no_start_duplicated_conjunction,
                'no-empty-section': no_empty_section,
                'date-weekday-mismatch': check_date_weekday_mismatch,
                'ginger': check_grammar,
                'max-number-of-lines': {
                    'max': max_lines_per_file
                },
                'max-comma': {
                    'max': max_comma_per_sentence
                },
                'ng-word': {
                    'words': check_no_good_words
                },
                'period-in-list-item': period_in_list_item,
                'unexpanded-acronym': {
                    'min_acronym_len': minimum_acronym_length,
                    'max_acronym_len': maximum_acronym_length,
                    'ignore_acronyms': ignore_acronyms
                },
                'rousseau': check_rousseau,
                'alex': check_offensive_expressions,
                'common-misspellings': check_common_misspellings,
                'spellchecker': enable_spellchecker,
                'write-good': write_good,
                'no-dead-link': check_invalid_links
            }

            default_config = {
                'rules': options,
                'plugins': ['rst', 'html']
            }
            return json.dumps(default_config)

    @staticmethod
    def create_arguments(filename, file, config_file, textlint_config: str=''):
        """
        :param textlint_config:
            The location of the ``.textlintrc`` config file.
        """
        return ('-c',
                textlint_config if textlint_config else config_file,
                filename)
