import _plotly_utils.basevalidators


class HistfuncValidator(_plotly_utils.basevalidators.EnumeratedValidator):

    def __init__(
        self, plotly_name='histfunc', parent_name='histogram', **kwargs
    ):
        super(HistfuncValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calc',
            role='style',
            values=['count', 'sum', 'avg', 'min', 'max'],
            **kwargs
        )
