import unittest
from unittest.mock import MagicMock, PropertyMock, patch

import kernpy as kp


class TestTokenizer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.token_1 = MagicMock(spec=kp.Token)  # Mock Token class

        # Mock the encoding property
        type(cls.token_1).encoding = PropertyMock(return_value="2.bb-_L")

        # Mock the export function
        cls.token_1.export = MagicMock(return_value="2@.@bb@-·_·L")

    def test_ekern_tokenizer_1(self):
        tokenizer = kp.EkernTokenizer()
        token_str = tokenizer.tokenize(self.token_1)
        self.assertEqual('2@.@bb@-·_·L', token_str)
        self.token_1.export.assert_called()

    def test_kern_tokenizer_1(self):
        tokenizer = kp.KernTokenizer()
        token_str = tokenizer.tokenize(self.token_1)
        self.assertEqual('2.bb-_L', token_str)
        self.token_1.export.assert_called()

    def test_bkern_tokenizer_1(self):
        tokenizer = kp.BkernTokenizer()
        token_str = tokenizer.tokenize(self.token_1)
        self.assertEqual('2.bb-', token_str)
        self.token_1.export.assert_called()

    def test_bekern_tokenizer_1(self):
        tokenizer = kp.BekernTokenizer()
        token_str = tokenizer.tokenize(self.token_1)
        self.assertEqual('2@.@bb@-', token_str)
        self.token_1.export.assert_called()

    def test_tokenizer_factory_kern(self):
        tokenizer = kp.TokenizerFactory.create(kp.KernTypeExporter.normalizedKern.value)
        self.assertIsInstance(tokenizer, kp.KernTokenizer)

    def test_tokenizer_factory_ekern(self):
        tokenizer = kp.TokenizerFactory.create(kp.KernTypeExporter.eKern.value)
        self.assertIsInstance(tokenizer, kp.EkernTokenizer)

    def test_tokenizer_factory_bkern(self):
        tokenizer = kp.TokenizerFactory.create(kp.KernTypeExporter.bKern.value)
        self.assertIsInstance(tokenizer, kp.BekernTokenizer)

    def test_tokenizer_factory_raise_error_if_none(self):
        with self.assertRaises(ValueError):
            kp.TokenizerFactory.create(None)

    def test_tokenizer_factory_raise_error_if_invalid(self):
        with self.assertRaises(ValueError):
            kp.TokenizerFactory.create('invalid')
