from unittest import TestCase

from ai_assistant_parsers_core.parsers.mixins.domain import DomainMixin


FAKE_URLS = [
    "https://cat.spbu.ru/page_1",
    "https://cat.spbu.ru/page_1/",
    "https://cat.spbu.ru/",
    "https://cat.spbu.ru",
]


class TestDomainMixin(TestCase):
    def test_check_with_allowed_domains_paths(self):
        obj = DomainMixin(
            allowed_domains_paths=["pr.spbu.ru"],
            excluded_paths=["/museum/web-sites/"],
        )

        self.assertTrue(obj.check("https://pr.spbu.ru"))
        self.assertTrue(obj.check("https://pr.spbu.ru/"))
        self.assertTrue(obj.check("https://pr.spbu.ru/page_1"))
        self.assertTrue(obj.check("https://pr.spbu.ru/page_1/"))
        self.assertTrue(obj.check("https://pr.spbu.ru/page_2/page_3/page_4"))
        self.assertTrue(obj.check("https://pr.spbu.ru/page_2/page_3/page_4/"))
        self.assertTrue(obj.check("https://pr.spbu.ru/museum/web-sites/page_1"))
        self.assertTrue(obj.check("https://pr.spbu.ru/museum/web-sites/page_1/"))

        self.assertFalse(obj.check("https://pr.spbu.ru/museum/web-sites/"))
        self.assertFalse(obj.check("https://pr.spbu.ru/museum/web-sites"))

        for url in FAKE_URLS:
           self.assertFalse(obj.check(url))

    def test_check_of_main_domain(self):
        obj = DomainMixin(allowed_domains_paths=["spbu.ru"])

        self.assertTrue(obj.check("https://spbu.ru"))
        self.assertTrue(obj.check("https://spbu.ru/"))
        self.assertTrue(obj.check("https://spbu.ru/page_1"))
        self.assertTrue(obj.check("https://spbu.ru/page_1/"))
        self.assertTrue(obj.check("https://spbu.ru/page_2/page_3/page_4"))
        self.assertTrue(obj.check("https://spbu.ru/page_2/page_3/page_4/"))

        for url in FAKE_URLS:
           self.assertFalse(obj.check(url))

    def test_check_with_excluded_paths(self):
        obj = DomainMixin(allowed_domains_paths=["spbu.ru"], excluded_paths=["/museum/web-sites/*"])

        self.assertTrue(obj.check("https://spbu.ru/"))
        self.assertFalse(obj.check("https://spbu.ru/museum/web-sites/"))
        self.assertFalse(obj.check("https://spbu.ru/museum/web-sites/page_1"))
        self.assertFalse(obj.check("https://spbu.ru/museum/web-sites/page_1/page_2"))

        obj = DomainMixin(allowed_domains_paths=["spbu.ru"], excluded_paths=["/museum/web-sites/?*"])

        self.assertTrue(obj.check("https://spbu.ru/"))
        self.assertTrue(obj.check("https://spbu.ru/museum/web-sites/"))
        self.assertFalse(obj.check("https://spbu.ru/museum/web-sites/page_1"))
        self.assertFalse(obj.check("https://spbu.ru/museum/web-sites/page_1/page_2"))

    def test_check_with_included_paths(self):
        obj = DomainMixin(allowed_domains_paths=["spbu.ru"], included_paths=["/museum/web-sites/*"])

        self.assertFalse(obj.check("https://spbu.ru/"))
        self.assertTrue(obj.check("https://spbu.ru/museum/web-sites/"))
        self.assertTrue(obj.check("https://spbu.ru/museum/web-sites/page_1"))
        self.assertTrue(obj.check("https://spbu.ru/museum/web-sites/page_1/page_2"))

        obj = DomainMixin(allowed_domains_paths=["spbu.ru"], included_paths=["/museum/web-sites/?*"])

        self.assertFalse(obj.check("https://spbu.ru/"))
        self.assertFalse(obj.check("https://spbu.ru/museum/web-sites/"))
        self.assertTrue(obj.check("https://spbu.ru/museum/web-sites/page_1"))
        self.assertTrue(obj.check("https://spbu.ru/museum/web-sites/page_1/page_2"))
