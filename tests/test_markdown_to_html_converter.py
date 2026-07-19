from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from markdown_to_html_converter import convert_markdown_report_to_self_contained_html


class MarkdownToHtmlConverterTest(unittest.TestCase):
    def test_heading_links_have_unique_targets(self) -> None:
        markdown = "\n".join(
            [
                "# Report",
                "## Analysis",
                "### Finding",
                "### Finding",
            ]
        )

        result = convert_markdown_report_to_self_contained_html(markdown)

        self.assertIn('<section class="report-section" id="report">', result)
        self.assertIn('<section class="report-section" id="analysis">', result)
        self.assertIn('<h3 id="finding">Finding</h3>', result)
        self.assertIn('<h3 id="finding-2">Finding</h3>', result)
        self.assertIn('<a href="#finding">Finding</a>', result)
        self.assertIn('<a href="#finding-2">Finding</a>', result)


if __name__ == "__main__":
    unittest.main()
