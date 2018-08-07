import _plotly_utils.basevalidators


class ShowlegendValidator(_plotly_utils.basevalidators.BooleanValidator):

    def __init__(
        self, plotly_name='showlegend', parent_name='layout', **kwargs
    ):
        super(ShowlegendValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='legend',
            role='info',
            **kwargs
        )
