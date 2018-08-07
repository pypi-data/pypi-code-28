import _plotly_utils.basevalidators


class ZerolineValidator(_plotly_utils.basevalidators.BooleanValidator):

    def __init__(
        self, plotly_name='zeroline', parent_name='layout.yaxis', **kwargs
    ):
        super(ZerolineValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='ticks',
            role='style',
            **kwargs
        )
