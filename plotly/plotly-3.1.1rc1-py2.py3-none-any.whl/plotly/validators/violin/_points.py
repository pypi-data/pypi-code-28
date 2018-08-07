import _plotly_utils.basevalidators


class PointsValidator(_plotly_utils.basevalidators.EnumeratedValidator):

    def __init__(self, plotly_name='points', parent_name='violin', **kwargs):
        super(PointsValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calcIfAutorange',
            role='style',
            values=['all', 'outliers', 'suspectedoutliers', False],
            **kwargs
        )
