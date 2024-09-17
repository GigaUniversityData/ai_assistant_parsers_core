from unittest import TestCase

from ai_assistant_parsers_core.parsers.mixins.page import PageMixin


class TestDomainMixin(TestCase):
    def test_check(self):
        obj = PageMixin(allowed_paths=["pr.spbu.ru/page_1/page_2/", "pr.spbu.ru/page_1/page_3/"])

        self.assertTrue(obj.check("https://pr.spbu.ru/page_1/page_2/"))
        self.assertTrue(obj.check("https://pr.spbu.ru/page_1/page_3/"))

        self.assertFalse(obj.check("https://pr.spbu.ru"))
        self.assertFalse(obj.check("https://pr.spbu.ru/"))
        self.assertFalse(obj.check("https://pr.spbu.ru/page_1"))
        self.assertFalse(obj.check("https://pr.spbu.ru/page_1/page_1"))
        self.assertFalse(obj.check("https://pr.spbu.ru/page_2/page_3/page_4"))

        self.assertFalse(obj.check("https://spbu.ru/page_1/page_3/"))
        self.assertFalse(obj.check("https://cat.spbu.ru/page_1/page_3/"))

    def test__check_allowed_paths_error(self):
        with self.assertRaises(ValueError):
            PageMixin(allowed_paths=["pr.spbu.ru/page_1/page_2"])
