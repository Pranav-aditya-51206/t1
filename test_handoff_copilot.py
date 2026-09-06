import unittest

from handoff_copilot import generate_handoff_brief


class HandoffCopilotTests(unittest.TestCase):
    def test_extracts_intent_section_from_checkpoint(self):
        checkpoint = {
            "intent": "Add a Markdown handoff generator.",
            "files_changed": ["handoff_copilot.py"],
            "reasoning": "Keep the output concise.",
        }

        brief = generate_handoff_brief(checkpoint)

        self.assertIn("## Intent\n\n- Add a Markdown handoff generator.", brief)


if __name__ == "__main__":
    unittest.main()
