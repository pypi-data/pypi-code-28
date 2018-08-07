import _plotly_utils.basevalidators


class SimplifyValidator(_plotly_utils.basevalidators.BooleanValidator):

    def __init__(
        self, plotly_name='simplify', parent_name='scatter.line', **kwargs
    ):
        super(SimplifyValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='plot',
            role='info',
            **kwargs
        )
