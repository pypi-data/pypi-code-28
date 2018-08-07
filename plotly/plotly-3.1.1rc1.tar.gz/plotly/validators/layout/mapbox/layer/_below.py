import _plotly_utils.basevalidators


class BelowValidator(_plotly_utils.basevalidators.StringValidator):

    def __init__(
        self, plotly_name='below', parent_name='layout.mapbox.layer', **kwargs
    ):
        super(BelowValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='plot',
            role='info',
            **kwargs
        )
