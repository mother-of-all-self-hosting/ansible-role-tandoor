# SPDX-FileCopyrightText: 2026 QEDeD
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import re
import unittest
from pathlib import Path


ROLE_VARIABLE_PATTERN = re.compile(r"\b(tandoor_[A-Za-z0-9_]+)\b")
DEFAULT_VARIABLE_PATTERN = re.compile(r"^(tandoor_[A-Za-z0-9_]+):", re.MULTILINE)
REGISTERED_VARIABLE_PATTERN = re.compile(
    r"^\s+register:\s+(tandoor_[A-Za-z0-9_]+)\s*$",
    re.MULTILINE,
)


class UninstallVariableTest(unittest.TestCase):
    def test_uninstall_references_defined_role_variables(self) -> None:
        repository_root = Path(__file__).resolve().parents[1]
        defaults = (repository_root / "defaults/main.yml").read_text(encoding="utf-8")
        uninstall_tasks = (repository_root / "tasks/uninstall.yml").read_text(
            encoding="utf-8"
        )

        defined_variables = set(DEFAULT_VARIABLE_PATTERN.findall(defaults))
        defined_variables.update(REGISTERED_VARIABLE_PATTERN.findall(uninstall_tasks))
        referenced_variables = set(ROLE_VARIABLE_PATTERN.findall(uninstall_tasks))

        self.assertEqual(
            sorted(referenced_variables - defined_variables),
            [],
            "Uninstall tasks reference undefined Tandoor role variables",
        )


if __name__ == "__main__":
    unittest.main()
