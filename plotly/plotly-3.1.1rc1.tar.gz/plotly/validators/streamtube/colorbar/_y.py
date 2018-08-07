import _plotly_utils.basevalidators


class YValidator(_plotly_utils.basevalidators.NumberValidator):

    def __init__(
        self, plotly_name='y', parent_name='streamtube.colorbar', **kwargs
    ):
        super(YValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='colorbars',
            max=3,
            min=-2,
            role='style',
            **kwargs
        )
