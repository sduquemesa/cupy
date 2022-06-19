import pytest

import numpy

import cupy
from cupy import testing
import cupyx.scipy.special  # NOQA

import scipy.special  # NOQA


@testing.with_requires('scipy')
class TestLogsumexp:

    @testing.for_all_dtypes()
    @testing.numpy_cupy_array_equal(scipy_name='scp')
    def test_large_inputs(self, xp, scp, dtype):
        a = xp.arange(400)
        return scp.special.logsumexp(a)

    @testing.for_all_dtypes()
    @testing.numpy_cupy_array_equal(scipy_name='scp')
    def test_more_large_inputs(self, xp, scp, dtype):
        a = xp.arange(10000)
        return scp.special.logsumexp(a)

    @testing.for_all_dtypes(no_bool=True)
    @testing.numpy_cupy_array_equal(scipy_name='scp')
    def test_large_numbers(self, xp, scp, dtype):
        a = xp.array([1000, 1000], dtype=dtype)
        return scp.special.logsumexp(a)

    @testing.numpy_cupy_array_equal(scipy_name='scp')
    def test_keep_dimensions(self, xp, scp):
        a = xp.array([[100, 1000], [1e10, 1e-10]])
        return scp.special.logsumexp(a, axis=-1, keepdims=True)

    @testing.for_all_dtypes(no_bool=True)
    @testing.numpy_cupy_allclose(scipy_name='scp', rtol=1e-6)
    def test_array_inputs(self, xp, scp, dtype):
        a = testing.shaped_random((1000, 10000), xp, dtype=dtype)
        return scp.special.logsumexp(a)

    @testing.for_all_dtypes(no_bool=True)
    @testing.numpy_cupy_array_equal(scipy_name='scp')
    def test_sign_argument(self, xp, scp, dtype):
        a = xp.array([1, 1, 1], dtype=dtype)
        b = xp.array([1, -1, -1], dtype=dtype)
        return scp.special.logsumexp(a, b=b, return_sign=True)

    @testing.for_all_dtypes(no_bool=True)
    @testing.numpy_cupy_array_equal(scipy_name='scp')
    def test_sign_zero(self, xp, scp, dtype):
        a = xp.array([1, 1], dtype=dtype)
        b = xp.array([1, -1], dtype=dtype)
        return scp.special.logsumexp(a, b=b, return_sign=True)

    @testing.for_all_dtypes(no_bool=True)
    @testing.numpy_cupy_allclose(scipy_name='scp', rtol=1e-6)
    def test_sign_shape(self, xp, scp, dtype):
        a = testing.shaped_random((1, 2, 3, 4), xp, dtype=dtype)
        b = testing.shaped_random((1, 1, 1, 4), xp, dtype=dtype)
        return scp.special.logsumexp(a, b=b, return_sign=True)

    @testing.for_all_dtypes(no_bool=True)
    @testing.numpy_cupy_allclose(scipy_name='scp', rtol=1e-6)
    def test_sign_shape_axis(self, xp, scp, dtype):
        a = testing.shaped_random((1, 2, 3, 4), xp, dtype=dtype)
        b = testing.shaped_random((1, 2, 3, 4), xp, dtype=dtype)
        return scp.special.logsumexp(a, axis=2, b=b, return_sign=True)

    @testing.for_all_dtypes(no_bool=True)
    @testing.numpy_cupy_allclose(scipy_name='scp', rtol=1e-6)
    def test_sign_shape_axis_2d(self, xp, scp, dtype):
        a = testing.shaped_random((1, 2, 3, 4), xp, dtype=dtype)
        b = testing.shaped_random((1, 2, 3, 4), xp, dtype=dtype)
        return scp.special.logsumexp(a, axis=(1, 3), b=b, return_sign=True)

    @testing.for_all_dtypes()
    @testing.numpy_cupy_array_equal(scipy_name='scp')
    def test_b_zero(self, xp, scp, dtype):
        a = xp.array([1, 100000], dtype=dtype)
        b = xp.array([1, 0], dtype=dtype)
        return scp.special.logsumexp(a, b=b)

    @testing.for_all_dtypes()
    @testing.numpy_cupy_array_equal(scipy_name='scp')
    def test_b_shape(self, xp, scp, dtype):
        a = testing.shaped_arange((4, 1, 2, 1), xp, dtype=dtype)
        b = testing.shaped_arange((3, 1, 5), xp, dtype=dtype)
        return scp.special.logsumexp(a, b=b)

    @testing.numpy_cupy_array_equal(scipy_name='scp')
    def test_special_values(self, xp, scp):
        a = xp.array([cupy.inf, -cupy.inf, cupy.nan, -cupy.nan])
        return scp.special.logsumexp(a)

    @testing.for_all_dtypes()
    def test_empty_array_inputs(self, dtype):
        for xp in (scipy, cupy):
            with pytest.raises(ValueError):
                if xp is scipy:
                    a = numpy.array([], dtype=dtype)
                    xp.special.logsumexp(a)
                else:
                    a = xp.array([], dtype=dtype)
                    cupyx.scipy.special.logsumexp(a)
