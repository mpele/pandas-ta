# -*- coding: utf-8 -*-
from unittest import TestCase, skip
import pandas.testing as pdt
from pandas import DataFrame, Series

import talib as tal

from .config import error_analysis, sample_data, CORRELATION, CORRELATION_THRESHOLD
from .context import pandas_ta


class TestVolatility(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = sample_data
        cls.data.columns = cls.data.columns.str.lower()
        cls.open = cls.data["open"]
        cls.high = cls.data["high"]
        cls.low = cls.data["low"]
        cls.close = cls.data["close"]
        if "volume" in cls.data.columns:
            cls.volume = cls.data["volume"]

    @classmethod
    def tearDownClass(cls):
        del cls.open
        del cls.high
        del cls.low
        del cls.close
        if hasattr(cls, "volume"):
            del cls.volume
        del cls.data

    def setUp(self): pass
    def tearDown(self): pass


    def test_aberration(self):
        """Volatility: Aberration"""
        result = pandas_ta.aberration(self.high, self.low, self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "ABER_5_15")

    def test_accbands(self):
        """Volatility: ACCBANDS"""
        result = pandas_ta.accbands(self.high, self.low, self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "ACCBANDS_20")

    def test_atr(self):
        """Volatility: ATR"""
        result = pandas_ta.atr(self.high, self.low, self.close, talib=False)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "ATRr_14")

        try:
            expected = tal.ATR(self.high, self.low, self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

        result = pandas_ta.atr(self.high, self.low, self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "ATRr_14")

    def test_bbands(self):
        """Volatility: BBANDS"""
        result = pandas_ta.bbands(self.close, talib=False)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "BBANDS_5_2.0")

        try:
            expected = tal.BBANDS(self.close)
            expecteddf = DataFrame({"BBL_5_2.0": expected[2], "BBM_5_2.0": expected[1], "BBU_5_2.0": expected[0]})
            pdt.assert_frame_equal(result, expecteddf)
        except AssertionError:
            try:
                bbl_corr = pandas_ta.utils.df_error_analysis(result.iloc[:, 0], expecteddf.iloc[:,0])
                self.assertGreater(bbl_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result.iloc[:, 0], CORRELATION, ex)

            try:
                bbm_corr = pandas_ta.utils.df_error_analysis(result.iloc[:, 1], expecteddf.iloc[:,1])
                self.assertGreater(bbm_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result.iloc[:, 1], CORRELATION, ex, newline=False)

            try:
                bbu_corr = pandas_ta.utils.df_error_analysis(result.iloc[:, 2], expecteddf.iloc[:,2])
                self.assertGreater(bbu_corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result.iloc[:, 2], CORRELATION, ex, newline=False)

        result = pandas_ta.bbands(self.close, ddof=0)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "BBANDS_5_2.0")

        result = pandas_ta.bbands(self.close, ddof=1)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "BBANDS_5_2.0")

    def test_donchian(self):
        """Volatility: Donchian"""
        result = pandas_ta.donchian(self.high, self.low)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "DC_20_20")

        result = pandas_ta.donchian(self.high, self.low, lower_length=20, upper_length=5)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "DC_20_5")

    def test_hwc(self):
        """Volatility: HWC"""
        result = pandas_ta.hwc(self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "HWC_1")

        result = pandas_ta.hwc(self.close, channel_eval=True)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "HWC_1")

    def test_kc(self):
        """Volatility: KC"""
        result = pandas_ta.kc(self.high, self.low, self.close)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "KCe_20_2")

        result = pandas_ta.kc(self.high, self.low, self.close, mamode="sma")
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "KCs_20_2")

    def test_massi(self):
        """Volatility: MASSI"""
        result = pandas_ta.massi(self.high, self.low)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "MASSI_9_25")

    def test_natr(self):
        """Volatility: NATR"""
        result = pandas_ta.natr(self.high, self.low, self.close, talib=False)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "NATR_14")

        try:
            expected = tal.NATR(self.high, self.low, self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

        result = pandas_ta.natr(self.high, self.low, self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "NATR_14")

    def test_pdist(self):
        """Volatility: PDIST"""
        result = pandas_ta.pdist(self.open, self.high, self.low, self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "PDIST")

    def test_rvi(self):
        """Volatility: RVI"""
        result = pandas_ta.rvi(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "RVI_14")

        result = pandas_ta.rvi(self.close, self.high, self.low, refined=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "RVIr_14")

        result = pandas_ta.rvi(self.close, self.high, self.low, thirds=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "RVIt_14")

    def test_thermo(self):
        """Volatility: THERMO"""
        result = pandas_ta.thermo(self.high, self.low)
        self.assertIsInstance(result, DataFrame)
        self.assertEqual(result.name, "THERMO_20_2_0.5")

    def test_true_range(self):
        """Volatility: True Range"""
        result = pandas_ta.true_range(self.high, self.low, self.close, talib=False)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "TRUERANGE_1")

        try:
            expected = tal.TRANGE(self.high, self.low, self.close)
            pdt.assert_series_equal(result, expected, check_names=False)
        except AssertionError:
            try:
                corr = pandas_ta.utils.df_error_analysis(result, expected)
                self.assertGreater(corr, CORRELATION_THRESHOLD)
            except Exception as ex:
                error_analysis(result, CORRELATION, ex)

        result = pandas_ta.true_range(self.high, self.low, self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "TRUERANGE_1")

    def test_ui(self):
        """Volatility: UI"""
        result = pandas_ta.ui(self.close)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "UI_14")

        result = pandas_ta.ui(self.close, everget=True)
        self.assertIsInstance(result, Series)
        self.assertEqual(result.name, "UIe_14")
