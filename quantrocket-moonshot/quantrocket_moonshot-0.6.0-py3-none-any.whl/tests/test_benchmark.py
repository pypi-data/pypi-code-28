# Copyright 2018 QuantRocket LLC - All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# To run: python3 -m unittest discover -s tests/ -p test_*.py -t . -v

import os
import unittest
from unittest.mock import patch
import glob
import pandas as pd
from moonshot import Moonshot
from moonshot.exceptions import MoonshotError, MoonshotParameterError
from moonshot.cache import TMP_DIR

class BenchmarkTestCase(unittest.TestCase):
    """
    Test cases for including benchmarks in backtests.
    """

    def tearDown(self):
        """
        Remove cached files.
        """
        for file in glob.glob("{0}/moonshot*.pkl".format(TMP_DIR)):
            os.remove(file)

    def test_complain_if_no_price_fields_for_benchmark(self):
        """
        Tests error handling when there are no suitable price fields for the
        benchmark (this would be an unusual error condition because not
        having price fields will lead to other issues too).
        """
        class BuyAndHold(Moonshot):
            """
            A basic test strategy that buys and holds.
            """
            CODE = "buy-and-hold"
            BENCHMARK = 12345

            def prices_to_signals(self, prices):
                signals = pd.DataFrame(1,
                                       index=prices.loc["Volume"].index,
                                       columns=prices.loc["Volume"].columns)
                return signals

            def positions_to_gross_returns(self, positions, prices):
                return pd.DataFrame(0, index=positions.index, columns=positions.columns)

        def mock_get_historical_prices(*args, **kwargs):

            dt_idx = pd.DatetimeIndex(["2018-05-01","2018-05-02","2018-05-03"])
            fields = ["Volume"]
            idx = pd.MultiIndex.from_product([fields, dt_idx], names=["Field", "Date"])

            prices = pd.DataFrame(
                {
                    12345: [
                        # Volume
                        5000,
                        16000,
                        8800
                    ],
                    23456: [
                        # Volume
                        15000,
                        14000,
                        28800
                    ],
                 },
                index=idx
            )

            master_fields = ["Timezone"]
            idx = pd.MultiIndex.from_product((master_fields, [dt_idx[0]]), names=["Field", "Date"])
            securities = pd.DataFrame(
                {
                    12345: [
                        "America/New_York"
                    ],
                    23456: [
                        "America/New_York"
                    ]
                },
                index=idx
            )

            return pd.concat((prices, securities))

        with patch("moonshot.strategies.base.get_historical_prices", new=mock_get_historical_prices):

            with self.assertRaises(MoonshotParameterError) as cm:
                BuyAndHold().backtest()

        self.assertIn("Cannot extract BENCHMARK 12345 from buy-and-hold without one of Close, Open, Bid, Ask, High, Low", repr(cm.exception))

    def test_complain_if_benchmark_conid_missing(self):
        """
        Tests error handling when a benchmark is specified that is not in the
        data.
        """

        class BuyBelow10(Moonshot):
            """
            A basic test strategy that buys below 10.
            """
            CODE = 'buy-below-10'
            BENCHMARK = 99999

            def prices_to_signals(self, prices):
                signals = prices.loc["Close"] < 10
                return signals.astype(int)

        def mock_get_historical_prices(*args, **kwargs):

            dt_idx = pd.DatetimeIndex(["2018-05-01","2018-05-02","2018-05-03", "2018-05-04"])
            fields = ["Close","Volume"]
            idx = pd.MultiIndex.from_product([fields, dt_idx], names=["Field", "Date"])

            prices = pd.DataFrame(
                {
                    12345: [
                        # Close
                        9,
                        11,
                        10.50,
                        9.99,
                        # Volume
                        5000,
                        16000,
                        8800,
                        9900
                    ],
                    23456: [
                        # Close
                        9.89,
                        11,
                        8.50,
                        10.50,
                        # Volume
                        15000,
                        14000,
                        28800,
                        17000

                    ],
                 },
                index=idx
            )

            master_fields = ["Timezone"]
            idx = pd.MultiIndex.from_product((master_fields, [dt_idx[0]]), names=["Field", "Date"])
            securities = pd.DataFrame(
                {
                    12345: [
                        "America/New_York"
                    ],
                    23456: [
                        "America/New_York"
                    ]
                },
                index=idx
            )
            return pd.concat((prices, securities))

        with patch("moonshot.strategies.base.get_historical_prices", new=mock_get_historical_prices):

            with self.assertRaises(MoonshotError) as cm:
                BuyBelow10().backtest()

        self.assertIn("buy-below-10 BENCHMARK ConId 99999 is not in backtest data", repr(cm.exception))

    def test_benchmark_eod(self):
        """
        Tests that the results DataFrame contains Benchmark prices when a
        Benchmark ConId is specified.
        """

        class BuyBelow10(Moonshot):
            """
            A basic test strategy that buys below 10.
            """
            CODE = 'buy-below-10'
            BENCHMARK = 23456

            def prices_to_signals(self, prices):
                signals = prices.loc["Close"] < 10
                return signals.astype(int)

        def mock_get_historical_prices(*args, **kwargs):

            dt_idx = pd.DatetimeIndex(["2018-05-01","2018-05-02","2018-05-03", "2018-05-04"])
            fields = ["Close","Volume"]
            idx = pd.MultiIndex.from_product([fields, dt_idx], names=["Field", "Date"])

            prices = pd.DataFrame(
                {
                    12345: [
                        # Close
                        9,
                        11,
                        10.50,
                        9.99,
                        # Volume
                        5000,
                        16000,
                        8800,
                        9900
                    ],
                    23456: [
                        # Close
                        9.89,
                        11,
                        8.50,
                        10.50,
                        # Volume
                        15000,
                        14000,
                        28800,
                        17000

                    ],
                 },
                index=idx
            )

            master_fields = ["Timezone"]
            idx = pd.MultiIndex.from_product((master_fields, [dt_idx[0]]), names=["Field", "Date"])
            securities = pd.DataFrame(
                {
                    12345: [
                        "America/New_York"
                    ],
                    23456: [
                        "America/New_York"
                    ]
                },
                index=idx
            )
            return pd.concat((prices, securities))

        with patch("moonshot.strategies.base.get_historical_prices", new=mock_get_historical_prices):

            results = BuyBelow10().backtest()

        self.assertSetEqual(
            set(results.index.get_level_values("Field")),
            {'Commission',
             'AbsExposure',
             'Signal',
             'Return',
             'Slippage',
             'NetExposure',
             'Trade',
             'AbsWeight',
             'Weight',
             'Benchmark'}
        )

        results = results.where(results.notnull(), "nan")

        benchmarks = results.loc["Benchmark"].reset_index()
        benchmarks.loc[:, "Date"] = benchmarks.Date.dt.strftime("%Y-%m-%dT%H:%M:%S%z")
        self.assertDictEqual(
            benchmarks.to_dict(orient="list"),
            {'Date': [
                '2018-05-01T00:00:00',
                '2018-05-02T00:00:00',
                '2018-05-03T00:00:00',
                '2018-05-04T00:00:00'],
             12345: ["nan",
                     "nan",
                     "nan",
                     "nan"],
             23456: [9.89,
                     11.0,
                     8.5,
                     10.5]}
        )

    def test_complain_if_intraday_and_no_benchmark_time(self):
        """
        Tests error handling for an intraday strategy when no BENCHMARK_TIME
        is specified.
        """

        class ShortAbove10Intraday(Moonshot):
            """
            A basic test strategy thatshorts above 10 and holds intraday.
            """
            CODE = "short-above-10"
            BENCHMARK = 12345

            def prices_to_signals(self, prices):
                morning_prices = prices.loc["Open"].xs("09:30:00", level="Time")
                short_signals = morning_prices > 10
                return -short_signals.astype(int)

            def signals_to_target_weights(self, signals, prices):
                weights = self.allocate_fixed_weights(signals, 0.25)
                return weights

            def target_weights_to_positions(self, weights, prices):
                # enter on same day
                positions = weights.copy()
                return positions

            def positions_to_gross_returns(self, positions, prices):
                # hold from 10:00-16:00
                closes = prices.loc["Close"]
                entry_prices = closes.xs("09:30:00", level="Time")
                exit_prices = closes.xs("15:30:00", level="Time")
                pct_changes = (exit_prices - entry_prices) / entry_prices
                gross_returns = pct_changes * positions
                return gross_returns

        def mock_get_historical_prices(*args, **kwargs):

            dt_idx = pd.DatetimeIndex(["2018-05-01","2018-05-02","2018-05-03"])
            fields = ["Close","Open"]
            times = ["09:30:00", "15:30:00"]
            idx = pd.MultiIndex.from_product(
                [fields, dt_idx, times], names=["Field", "Date", "Time"])

            prices = pd.DataFrame(
                {
                    12345: [
                        # Close
                        9.6,
                        10.45,
                        10.12,
                        15.45,
                        8.67,
                        12.30,
                        # Open
                        9.88,
                        10.34,
                        10.23,
                        16.45,
                        8.90,
                        11.30,
                    ],
                    23456: [
                        # Close
                        10.56,
                        12.01,
                        10.50,
                        9.80,
                        13.40,
                        14.50,
                        # Open
                        9.89,
                        11,
                        8.50,
                        10.50,
                        14.10,
                        15.60
                    ],
                 },
                index=idx
            )

            master_fields = ["Timezone"]
            idx = pd.MultiIndex.from_product(
                (master_fields, [dt_idx[0]], [times[0]]), names=["Field", "Date", "Time"])
            securities = pd.DataFrame(
                {
                    12345: [
                        "America/New_York"
                    ],
                    23456: [
                        "America/New_York"
                    ]
                },
                index=idx
            )
            return pd.concat((prices, securities))

        with patch("moonshot.strategies.base.get_historical_prices", new=mock_get_historical_prices):

            with self.assertRaises(MoonshotParameterError) as cm:
                ShortAbove10Intraday().backtest()

        self.assertIn((
            "Cannot extract BENCHMARK 12345 from short-above-10 because prices contains intraday "
            "prices but no BENCHMARK_TIME specified"), repr(cm.exception))

    def test_complain_if_benchmark_time_not_in_data(self):
        """
        Tests error handling for an intraday strategy when BENCHMARK_TIME is
        specified but is not in the data.
        """

        class ShortAbove10Intraday(Moonshot):
            """
            A basic test strategy thatshorts above 10 and holds intraday.
            """
            CODE = "short-above-10"
            BENCHMARK = 12345
            BENCHMARK_TIME = "15:45:00"

            def prices_to_signals(self, prices):
                morning_prices = prices.loc["Open"].xs("09:30:00", level="Time")
                short_signals = morning_prices > 10
                return -short_signals.astype(int)

            def signals_to_target_weights(self, signals, prices):
                weights = self.allocate_fixed_weights(signals, 0.25)
                return weights

            def target_weights_to_positions(self, weights, prices):
                # enter on same day
                positions = weights.copy()
                return positions

            def positions_to_gross_returns(self, positions, prices):
                # hold from 10:00-16:00
                closes = prices.loc["Close"]
                entry_prices = closes.xs("09:30:00", level="Time")
                exit_prices = closes.xs("15:30:00", level="Time")
                pct_changes = (exit_prices - entry_prices) / entry_prices
                gross_returns = pct_changes * positions
                return gross_returns

        def mock_get_historical_prices(*args, **kwargs):

            dt_idx = pd.DatetimeIndex(["2018-05-01","2018-05-02","2018-05-03"])
            fields = ["Close","Open"]
            times = ["09:30:00", "15:30:00"]
            idx = pd.MultiIndex.from_product(
                [fields, dt_idx, times], names=["Field", "Date", "Time"])

            prices = pd.DataFrame(
                {
                    12345: [
                        # Close
                        9.6,
                        10.45,
                        10.12,
                        15.45,
                        8.67,
                        12.30,
                        # Open
                        9.88,
                        10.34,
                        10.23,
                        16.45,
                        8.90,
                        11.30,
                    ],
                    23456: [
                        # Close
                        10.56,
                        12.01,
                        10.50,
                        9.80,
                        13.40,
                        14.50,
                        # Open
                        9.89,
                        11,
                        8.50,
                        10.50,
                        14.10,
                        15.60
                    ],
                 },
                index=idx
            )

            master_fields = ["Timezone"]
            idx = pd.MultiIndex.from_product(
                (master_fields, [dt_idx[0]], [times[0]]), names=["Field", "Date", "Time"])
            securities = pd.DataFrame(
                {
                    12345: [
                        "America/New_York"
                    ],
                    23456: [
                        "America/New_York"
                    ]
                },
                index=idx
            )
            return pd.concat((prices, securities))

        with patch("moonshot.strategies.base.get_historical_prices", new=mock_get_historical_prices):

            with self.assertRaises(MoonshotError) as cm:
                ShortAbove10Intraday().backtest()

        self.assertIn(
            "short-above-10 BENCHMARK_TIME 15:45:00 is not in backtest data", repr(cm.exception))

    def test_benchmark_intraday(self):
        """
        Tests that the results DataFrame contains Benchmark prices when a
        Benchmark ConId is specified on an intraday strategy.
        """

        class ShortAbove10Intraday(Moonshot):
            """
            A basic test strategy that shorts above 10 and holds intraday.
            """
            CODE = "short-above-10"
            BENCHMARK = 12345
            BENCHMARK_TIME = "15:30:00"

            def prices_to_signals(self, prices):
                morning_prices = prices.loc["Open"].xs("09:30:00", level="Time")
                short_signals = morning_prices > 10
                return -short_signals.astype(int)

            def signals_to_target_weights(self, signals, prices):
                weights = self.allocate_fixed_weights(signals, 0.25)
                return weights

            def target_weights_to_positions(self, weights, prices):
                # enter on same day
                positions = weights.copy()
                return positions

            def positions_to_gross_returns(self, positions, prices):
                # hold from 10:00-16:00
                closes = prices.loc["Close"]
                entry_prices = closes.xs("09:30:00", level="Time")
                exit_prices = closes.xs("15:30:00", level="Time")
                pct_changes = (exit_prices - entry_prices) / entry_prices
                gross_returns = pct_changes * positions
                return gross_returns

        def mock_get_historical_prices(*args, **kwargs):

            dt_idx = pd.DatetimeIndex(["2018-05-01","2018-05-02","2018-05-03"])
            fields = ["Close","Open"]
            times = ["09:30:00", "15:30:00"]
            idx = pd.MultiIndex.from_product(
                [fields, dt_idx, times], names=["Field", "Date", "Time"])

            prices = pd.DataFrame(
                {
                    12345: [
                        # Close
                        9.6,
                        10.45,
                        10.12,
                        15.45,
                        8.67,
                        12.30,
                        # Open
                        9.88,
                        10.34,
                        10.23,
                        16.45,
                        8.90,
                        11.30,
                    ],
                    23456: [
                        # Close
                        10.56,
                        12.01,
                        10.50,
                        9.80,
                        13.40,
                        14.50,
                        # Open
                        9.89,
                        11,
                        8.50,
                        10.50,
                        14.10,
                        15.60
                    ],
                 },
                index=idx
            )

            master_fields = ["Timezone"]
            idx = pd.MultiIndex.from_product(
                (master_fields, [dt_idx[0]], [times[0]]), names=["Field", "Date", "Time"])
            securities = pd.DataFrame(
                {
                    12345: [
                        "America/New_York"
                    ],
                    23456: [
                        "America/New_York"
                    ]
                },
                index=idx
            )
            return pd.concat((prices, securities))

        with patch("moonshot.strategies.base.get_historical_prices", new=mock_get_historical_prices):

            results = ShortAbove10Intraday().backtest()

        results = results.where(results.notnull(), "nan")

        benchmarks = results.loc["Benchmark"].reset_index()
        benchmarks.loc[:, "Date"] = benchmarks.Date.dt.strftime("%Y-%m-%dT%H:%M:%S%z")
        self.assertDictEqual(
            benchmarks.to_dict(orient="list"),
            {'Date': [
                '2018-05-01T00:00:00',
                '2018-05-02T00:00:00',
                '2018-05-03T00:00:00'],
             12345: [10.45,
                     15.45,
                     12.30],
             23456: ["nan",
                     "nan",
                     "nan"]}
        )
