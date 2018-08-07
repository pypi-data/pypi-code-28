"""
Beta diversity measures (:mod:`skbio.diversity.beta`)
=====================================================

.. currentmodule:: skbio.diversity.beta

This package provides implementations of beta diversity measures for computing
sample dissimilarity. Users of this package should also explore
``scipy.spatial.distance.pdist``, as it contains implementations of additional
beta diversity metrics with interfaces similar to those provided here.

Functions
---------

.. autosummary::
   :toctree: generated/

    unweighted_unifrac
    weighted_unifrac

"""

# ----------------------------------------------------------------------------
# Copyright (c) 2013--, scikit-bio development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

from skbio.util import TestRunner

from ._unifrac import unweighted_unifrac, weighted_unifrac

__all__ = ["unweighted_unifrac", "weighted_unifrac"]

test = TestRunner(__file__).test
