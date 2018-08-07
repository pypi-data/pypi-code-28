import _plotly_utils.basevalidators


class ColorsValidator(_plotly_utils.basevalidators.DataArrayValidator):

    def __init__(
        self, plotly_name='colors', parent_name='pie.marker', **kwargs
    ):
        super(ColorsValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calc',
            role='data',
            **kwargs
        )
