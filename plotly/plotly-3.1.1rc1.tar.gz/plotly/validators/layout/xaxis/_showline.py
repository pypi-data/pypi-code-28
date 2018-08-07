import _plotly_utils.basevalidators


class ShowlineValidator(_plotly_utils.basevalidators.BooleanValidator):

    def __init__(
        self, plotly_name='showline', parent_name='layout.xaxis', **kwargs
    ):
        super(ShowlineValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='layoutstyle',
            role='style',
            **kwargs
        )
