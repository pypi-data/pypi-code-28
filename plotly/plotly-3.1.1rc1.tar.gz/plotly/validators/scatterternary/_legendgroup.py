import _plotly_utils.basevalidators


class LegendgroupValidator(_plotly_utils.basevalidators.StringValidator):

    def __init__(
        self,
        plotly_name='legendgroup',
        parent_name='scatterternary',
        **kwargs
    ):
        super(LegendgroupValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='style',
            role='info',
            **kwargs
        )
