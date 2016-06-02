import re

from coalib.bears.LocalBear import LocalBear
from coalib.bearlib.naming_conventions import (
    to_camelcase, to_pascalcase, to_snakecase)
from bears.general.AnnotationBear import AnnotationBear
from coalib.bearlib.languages.LanguageDefinition import LanguageDefinition
from coalib.results.SourceRange import SourceRange
from coalib.results.Diff import Diff
from coalib.results.Result import Result


class CasingBear(LocalBear):

    def run(self,
            filename,
            file,
            dependency_results,
            casing: str,
            language: str):
        """
        Checks whether all identifier names (variables, classes, objects)
        follow a certain naming convention.

        :param filename:           Name of the file that needs to be checked.
        :param file:               File that needs to be checked in the form
                                   of a list of strings.
        :param dependency_results: A dict of dependencies with bear name as
                                   key and results as value
        :param casing:             camelCasing or snake_casing or PascalCasing
        :param language:           The language of the file, which is used to
                                   determine the keywords to ignore.
        """
        casing_convention = {"camel": to_camelcase,
                             "pascal": to_pascalcase,
                             "snake": to_snakecase}

        if casing not in casing_convention:
            self.err("Invalid casing convention provided: " + casing)
            return

        self.convertor = casing_convention[casing]
        coalang = LanguageDefinition(language)

        # TODO: Adapt after coala-analyzer/coala/issues/2200 is solved
        if "keywords" not in coalang or "special_chars" not in coalang:
            self.warn("CasingBear did not run because 'keywords' and "
                      "'special_chars' are necessary fields that are missing "
                      "in the coalang definition for " + language)
            return

        self.keywords = coalang["keywords"]
        self.delim = re.escape(str(coalang["special_chars"]) + " \t\n")

        annotations = dependency_results[AnnotationBear.name][0].contents
        string_results = annotations["strings"]
        results = []
        last_line = 1
        last_column = 1
        text = "".join(file)
        for string_range in string_results:
            results.append(SourceRange.from_values(
                text,
                start_line=last_line,
                start_column=last_column,
                end_line=string_range.start.line,
                end_column=string_range.start.column))
            last_line = string_range.end.line
            last_column = string_range.end.column
        results.append(SourceRange.from_values(
            text,
            start_line=last_line,
            start_column=last_column,
            end_line=len(file),
            end_column=len(file[-1])))

        changes = {}
        for result in results:
            line_number = result.start.line
            while line_number <= result.end.line:
                start = 0 if line_number != result.start.line \
                    else result.start.column
                end = result.end.column if line_number == result.end.line \
                    else len(file[line_number - 1])

                line_changes = self.process(file[line_number - 1][start:end])
                for prev in line_changes:
                    changes[prev] = line_changes[prev]

                line_number += 1

        lines_changed = set()
        result_texts = []
        for prev in changes:
            change = changes[prev]
            diff = Diff(file)
            first_line = -1
            num_changes = 0
            skip_var = False

            for line_number, line in enumerate(file, start=1):
                rep = re.sub("(?P<g1>[\\" + self.delim + "]*)" + prev +
                             "(?P<g2>[\\" + self.delim + "]*)",
                             "\g<g1>" + change + "\g<g2>", line)

                if rep != line:
                    if line_number in lines_changed:
                        skip_var = True
                    lines_changed.add(line_number)
                    diff.change_line(line_number, line, rep)
                    num_changes += 1
                    if first_line == -1:
                        first_line = line_number

            if skip_var:
                continue

            msg = "Change '" + prev + "' to '" + change + "'"
            if num_changes > 1:
                msg += ": " + str(num_changes) + " lines affected"
            result_texts.append(msg)
            vio = "The following name change is suggested:"
            vio += "".join("\n- " + string
                           for string in result_texts)

            yield Result.from_values(
                self,
                vio,
                diffs={filename: diff},
                file=filename,
                line=first_line)
            result_texts = []

    def process(self, content):
        """
        Processes the string by splitting it based on delimiters
        and then identifying the casing changes.

        :param content: The string to be processed
        :return:        A dict with current casing as key and
                        proposed change as value
        """
        splits = re.split("[" + self.delim + "]", content)
        results = {}
        for split in splits:
            if split not in self.keywords:
                if split != self.convertor(split):
                    results[split] = self.convertor(split)
        return results

    @staticmethod
    def get_dependencies():
        return [AnnotationBear]  # pragma: no cover
