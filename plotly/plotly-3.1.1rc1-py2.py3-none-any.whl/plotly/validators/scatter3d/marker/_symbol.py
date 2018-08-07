import _plotly_utils.basevalidators


class SymbolValidator(_plotly_utils.basevalidators.EnumeratedValidator):

    def __init__(
        self, plotly_name='symbol', parent_name='scatter3d.marker', **kwargs
    ):
        super(SymbolValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            array_ok=True,
            edit_type='calc',
            role='style',
            values=[
                'circle', 'circle-open', 'square', 'square-open', 'diamond',
                'diamond-open', 'cross', 'x'
            ],
            **kwargs
        )
