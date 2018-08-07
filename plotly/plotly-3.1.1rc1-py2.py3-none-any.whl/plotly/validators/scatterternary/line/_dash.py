import _plotly_utils.basevalidators


class DashValidator(_plotly_utils.basevalidators.StringValidator):

    def __init__(
        self, plotly_name='dash', parent_name='scatterternary.line', **kwargs
    ):
        super(DashValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='style',
            role='style',
            values=[
                'solid', 'dot', 'dash', 'longdash', 'dashdot', 'longdashdot'
            ],
            **kwargs
        )
