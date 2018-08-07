import _plotly_utils.basevalidators


class YanchorValidator(_plotly_utils.basevalidators.EnumeratedValidator):

    def __init__(
        self, plotly_name='yanchor', parent_name='layout.annotation', **kwargs
    ):
        super(YanchorValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calcIfAutorange+arraydraw',
            role='info',
            values=['auto', 'top', 'middle', 'bottom'],
            **kwargs
        )
