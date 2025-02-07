from unittest import TestCase

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

from anafit.core import Fit


class TestFit(TestCase):
    def setUp(self):
        # Set up simple linear data points
        self.fig, self.ax = plt.subplots()
        self.x = np.arange(0, 10, 1)
        noise = [-1, 1] * 5
        self.y = 2 * self.x + 5 + noise
        self.xy = np.transpose((self.x, self.y))
        (self.line,) = self.ax.plot(self.x, self.y)

        # Expected values from initialisation of Fit object
        self.linear = lambda x, a, b: a * x + b
        self.p_init = (1, 1)
        self.fname = "ax+b"

    def get_expected_fit(self, func, x, y, p):
        popt_expected, pcov_expected = curve_fit(func, x, y, p0=p)
        sigma_expected = np.sqrt(np.diagonal(pcov_expected))

        return popt_expected, pcov_expected, sigma_expected

    def test_init_no_options(self):
        # Test if the Fit object is correctly initialized when no optional arguments
        # are provided

        # When
        fit = Fit(self.line, self.fname)

        # Then
        np.testing.assert_array_almost_equal(fit.xydata, self.xy)
        np.testing.assert_array_almost_equal(
            fit.f(self.x, *self.p_init), self.linear(self.x, *self.p_init)
        )
        self.assertEqual(fit.p, self.p_init)

    def test_init_with_options(self):
        # Test if the Fit object is correctly initialized when both xrange and initial
        # fit coefficients are provided

        # Given
        xrange = (2, 7)
        x = self.x[xrange[0] + 1 : xrange[1]]  # noqa: E203
        y = self.y[xrange[0] + 1 : xrange[1]]  # noqa: E203
        p_init = (2, 2)

        # When
        fit = Fit(self.line, self.fname, xrange=xrange, p=p_init)

        # Then
        np.testing.assert_array_almost_equal(fit.xydata, np.transpose((x, y)))
        np.testing.assert_array_almost_equal(
            fit.f(self.x, *p_init), self.linear(self.x, *p_init)
        )
        self.assertEqual(fit.p, p_init)

    def test_init_with_p_in_function_name(self):
        # Test if the Fit object is correctly initialized when the function name
        # contains the initial fit coefficients

        # Given
        fname = "lambda x, a, b: a*x + b ; (2, 3)"
        p_init = (2, 3)
        popt_expected, pcov_expected, sigma_expected = self.get_expected_fit(
            self.linear,
            self.x,
            self.y,
            p_init,
        )

        # When
        fit = Fit(self.line, fname)

        # Then
        np.testing.assert_array_almost_equal(fit.xydata, self.xy)
        np.testing.assert_array_almost_equal(
            fit.f(self.x, *p_init), self.linear(self.x, *p_init)
        )
        self.assertEqual(fit.p, p_init)

    def test_fit(self):
        # Given
        popt_expected, pcov_expected, sigma_expected = self.get_expected_fit(
            self.linear, self.x, self.y, self.p_init
        )

        # When
        fit = Fit(self.line, self.fname)
        fit.fit()

        # Then
        np.testing.assert_array_almost_equal(fit.popt, popt_expected)
        np.testing.assert_array_almost_equal(fit.pcov, pcov_expected)
        np.testing.assert_array_almost_equal(fit.sigma, sigma_expected)

    def test_xrange_setter(self):
        # Test automatic fitting when xrange is set

        # Given
        fit = Fit(self.line, self.fname)
        xrange = (2, 7)
        x = self.x[xrange[0] + 1 : xrange[1]]  # noqa: E203
        y = self.y[xrange[0] + 1 : xrange[1]]  # noqa: E203
        p_init = (2, 2)
        popt_expected, pcov_expected, sigma_expected = self.get_expected_fit(
            self.linear,
            x,
            y,
            p_init,
        )

        # When
        fit.xrange = xrange

        # Then
        np.testing.assert_array_almost_equal(fit.popt, popt_expected)
        np.testing.assert_array_almost_equal(fit.pcov, pcov_expected)
        np.testing.assert_array_almost_equal(fit.sigma, sigma_expected)

    def test_p_setter(self):
        # Test automatic fitting when p is set

        # Given
        fit = Fit(self.line, self.fname)
        p = (2, 2)
        popt_expected, pcov_expected, sigma_expected = self.get_expected_fit(
            self.linear,
            self.x,
            self.y,
            p,
        )

        # When
        fit.p = p

        # Then
        np.testing.assert_array_almost_equal(fit.popt, popt_expected)
        np.testing.assert_array_almost_equal(fit.pcov, pcov_expected)
        np.testing.assert_array_almost_equal(fit.sigma, sigma_expected)

    def test_fname_setter(self):
        # Test automatic fitting when fname is set

        # Given
        fit = Fit(self.line, self.fname)
        fname = "lambda x, a : a*x + 5 ; (0.5)"

        def linear(x, a):
            return a * x + 5

        p_init = (0.5,)
        pop_expected, pcov_expected, sigma_expected = self.get_expected_fit(
            linear,
            self.x,
            self.y,
            p_init,
        )

        # When
        fit.fname = fname

        # Then
        np.testing.assert_array_almost_equal(
            fit.f(self.x, *p_init), linear(self.x, *p_init)
        )
        np.testing.assert_array_almost_equal(fit.popt, pop_expected)
        np.testing.assert_array_almost_equal(fit.pcov, pcov_expected)
        np.testing.assert_array_almost_equal(fit.sigma, sigma_expected)

    def test_plot(self):
        # Test if the plot method correctly plots the fit and sets the confidence
        # intervals

        # Given
        fit = Fit(self.line, self.fname)
        fit.fit()
        popt_expected, pcov_expected, sigma_expected = self.get_expected_fit(
            self.linear, self.x, self.y, self.p_init
        )
        up_expected = self.linear(self.x, *(popt_expected + sigma_expected))
        low_expected = self.linear(self.x, *(popt_expected - sigma_expected))

        # When
        fit.plot()

        # Then
        np.testing.assert_array_almost_equal(fit.linfit.get_xdata(), self.x)
        np.testing.assert_array_almost_equal(
            fit.linfit.get_ydata(), self.linear(self.x, *popt_expected)
        )
        np.testing.assert_array_almost_equal(fit.upConfidence, up_expected)
        np.testing.assert_array_almost_equal(fit.lowConfidence, low_expected)
        self.assertTrue(fit._linfit.get_visible())
        self.assertFalse(fit._linConfidence.get_visible())
        self.assertFalse(fit._fitbox.get_visible())
        self.assertEqual(
            fit._fitbox.get_text(),
            (
                f"Fit {self.fname} :\n"
                f"{popt_expected[0]:.2f} +/- {sigma_expected[0]:.2f}\n"
                f"{popt_expected[1]:.2f} +/- {sigma_expected[1]:.2f}"
            ),
        )

    def test_plot_show_confidence_and_fitbox(self):
        # Test if the plot method correctly plots the fit, the confidence intervals
        # and the fitbox

        # Given
        fit = Fit(self.line, self.fname)
        fit.fit()
        popt_expected, pcov_expected, sigma_expected = self.get_expected_fit(
            self.linear, self.x, self.y, self.p_init
        )
        up_expected = self.linear(self.x, *(popt_expected + sigma_expected))
        low_expected = self.linear(self.x, *(popt_expected - sigma_expected))

        # When
        fit.plot(showInfo=True, showConf=True)

        # Then
        np.testing.assert_array_almost_equal(fit.linfit.get_xdata(), self.x)
        np.testing.assert_array_almost_equal(
            fit.linfit.get_ydata(), self.linear(self.x, *popt_expected)
        )
        np.testing.assert_array_almost_equal(fit.upConfidence, up_expected)
        np.testing.assert_array_almost_equal(fit.lowConfidence, low_expected)
        self.assertTrue(fit._linfit.get_visible())
        self.assertTrue(fit._linConfidence.get_visible())
        self.assertTrue(fit._fitbox.get_visible())
        self.assertEqual(
            fit._fitbox.get_text(),
            (
                f"Fit {self.fname} :\n"
                f"{popt_expected[0]:.2f} +/- {sigma_expected[0]:.2f}\n"
                f"{popt_expected[1]:.2f} +/- {sigma_expected[1]:.2f}"
            ),
        )

    def test_show_fitInfo(self):
        # Given
        fit = Fit(self.line, self.fname)
        fit.fit()
        fit.plot()

        # When
        fit.show_fitInfo(disp=True)

        # Then
        self.assertTrue(fit._fitbox.get_visible())

    def test_show_confidence(self):
        # Given
        fit = Fit(self.line, self.fname)
        fit.fit()
        fit.plot()

        # When
        fit.show_confidence(disp=True)

        # Then
        self.assertTrue(fit._linConfidence.get_visible())

    def test_repr_no_fit(self):
        # Given
        fit = Fit(self.line, self.fname)

        # When
        fit_repr = str(fit)

        # Then
        self.assertEqual(
            fit_repr,
            (
                f"Fitting function : {self.fname}\n"
                f"Xrange : [{fit.xydata[0, 0]}, {fit.xydata[-1, 0]}]\n"
                f"Initialising parameters : {self.p_init}\n"
                f"Coeff. : None\n"
                f"Uncertainty : None\n"
            ),
        )

    def test_repr_with_fit(self):
        # Given
        fit = Fit(self.line, self.fname)
        fit.fit()

        # When
        fit_repr = str(fit)

        # Then
        self.assertEqual(
            fit_repr,
            (
                f"Fitting function : {self.fname}\n"
                f"Xrange : [{fit.xydata[0, 0]}, {fit.xydata[-1, 0]}]\n"
                f"Initialising parameters : {self.p_init}\n"
                f"Coeff. : {fit.popt}\n"
                f"Uncertainty : {fit.sigma}\n"
            ),
        )
