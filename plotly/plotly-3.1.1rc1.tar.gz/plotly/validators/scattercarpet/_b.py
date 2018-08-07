import _plotly_utils.basevalidators


class BValidator(_plotly_utils.basevalidators.DataArrayValidator):

    def __init__(self, plotly_name='b', parent_name='scattercarpet', **kwargs):
        super(BValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calc',
            role='data',
            **kwargs
        )
