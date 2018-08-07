import pandas as pd

from fireant import Metric
from fireant.utils import (
    format_dimension_key,
    format_metric_key,
)
from .base import (
    TransformableWidget,
)
from ..references import (
    reference_key,
    reference_label,
)
from ... import formats

HARD_MAX_COLUMNS = 24


class Pandas(TransformableWidget):
    def __init__(self, metric, *metrics: Metric, pivot=(), transpose=False, max_columns=None):
        super(Pandas, self).__init__(metric, *metrics)
        self.pivot = pivot
        self.transpose = transpose
        self.max_columns = min(max_columns, HARD_MAX_COLUMNS) \
            if max_columns is not None \
            else HARD_MAX_COLUMNS

    def transform(self, data_frame, slicer, dimensions, references):
        """
        WRITEME

        :param data_frame:
        :param slicer:
        :param dimensions:
        :param references:
        :return:
        """
        result = data_frame.copy()

        for metric in self.items:
            if any([metric.precision is not None,
                    metric.prefix is not None,
                    metric.suffix is not None]):
                df_key = format_metric_key(metric.key)

                result[df_key] = result[df_key] \
                    .apply(lambda x: formats.metric_display(x, metric.prefix, metric.suffix, metric.precision))

        for dimension in dimensions:
            if dimension.has_display_field:
                result = result.set_index(format_dimension_key(dimension.display_key), append=True)
                result = result.reset_index(format_dimension_key(dimension.key), drop=True)

            if hasattr(dimension, 'display_values'):
                self._replace_display_values_in_index(dimension, result)

        if isinstance(data_frame.index, pd.MultiIndex):
            index_levels = [dimension.display_key
                            if dimension.has_display_field
                            else dimension.key
                            for dimension in dimensions]

            result = result.reorder_levels([format_dimension_key(level)
                                            for level in index_levels])

        result = result[[format_metric_key(reference_key(item, reference))
                         for reference in [None] + references
                         for item in self.items]]

        if dimensions:
            result.index.names = [dimension.label or dimension.key
                                  for dimension in dimensions]

        result.columns = pd.Index([reference_label(item, reference)
                                   for item in self.items
                                   for reference in [None] + references],
                                  name='Metrics')

        return self.pivot_data_frame(result, [d.label or d.key for d in self.pivot], self.transpose)

    @staticmethod
    def pivot_data_frame(data_frame, pivot=(), transpose=False):
        """
        Pivot and transpose the data frame. Dimensions including in the `pivot` arg will be unshifted to columns. If
        `transpose` is True the data frame will be transposed. If there is only index level in the data frame (ie. one
        dimension), and that dimension is pivoted, then the data frame will just be transposed. If there is a single
        metric in the data frame and at least one dimension pivoted, the metrics column level will be dropped for
        simplicity.

        :param data_frame:
            The result set data frame
        :param pivot:
            A list of index keys for `data_frame` of levels to shift
        :param transpose:
            A boolean true or false whether to transpose the data frame.
        :return:
            The shifted/transposed data frame
        """
        if not (pivot or transpose):
            return data_frame

        # NOTE: Don't pivot a single dimension data frame. This turns the data frame into a series and pivots the
        # metrics anyway. Instead, transpose the data frame.
        should_transpose_instead_of_pivot = len(pivot) == len(data_frame.index.names)

        if pivot and not should_transpose_instead_of_pivot:
            data_frame = data_frame.unstack(level=pivot)

        if transpose or should_transpose_instead_of_pivot:
            data_frame = data_frame.transpose()

        # If there are more than one column levels and the last level is a single metric, drop the level
        if isinstance(data_frame.columns, pd.MultiIndex) and 1 == len(data_frame.columns.levels[0]):
            data_frame.name = data_frame.columns.levels[0][0]  # capture the name of the metrics column
            data_frame.columns = data_frame.columns.droplevel(0)  # drop the metrics level

        return data_frame.fillna('')

    def _replace_display_values_in_index(self, dimension, result):
        """
        Replaces the raw values of a (categorical) dimension in the index with their corresponding display values.
        """
        if isinstance(result.index, pd.MultiIndex):
            df_key = format_dimension_key(dimension.key)
            values = [dimension.display_values.get(x, x)
                      for x in result.index.get_level_values(df_key)]
            result.index.set_levels(level=df_key,
                                    levels=values,
                                    inplace=True)
            return result

        values = [dimension.display_values.get(x, x)
                  for x in result.index]
        result.index = pd.Index(values, name=result.index.name)
        return result
