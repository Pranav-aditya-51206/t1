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

    def test_marks_redacted_reasoning_as_incomplete(self):
        checkpoint = {
            "intent": "Add a Markdown handoff generator.",
            "files_changed": ["handoff_copilot.py"],
            "reasoning": "[REDACTED]",
            "unfinished": ["Add CLI support."],
            "risks": ["Checkpoint format may vary."],
            "verification_checklist": ["Run unit tests."],
        }

        brief = generate_handoff_brief(checkpoint)

        self.assertIn("Context: PARTIAL — some fields redacted or missing", brief)
        self.assertIn(
            "## What's Done — Incomplete — data unavailable", brief
        )
        self.assertNotIn("- [REDACTED]", brief)


if __name__ == "__main__":
    unittest.main()
