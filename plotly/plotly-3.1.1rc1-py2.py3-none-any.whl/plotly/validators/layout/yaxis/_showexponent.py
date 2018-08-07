import _plotly_utils.basevalidators


class ShowexponentValidator(_plotly_utils.basevalidators.EnumeratedValidator):

    def __init__(
        self, plotly_name='showexponent', parent_name='layout.yaxis', **kwargs
    ):
        super(ShowexponentValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='ticks',
            role='style',
            values=['all', 'first', 'last', 'none'],
            **kwargs
        )
