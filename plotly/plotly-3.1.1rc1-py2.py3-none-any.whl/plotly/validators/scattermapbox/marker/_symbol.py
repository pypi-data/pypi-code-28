import _plotly_utils.basevalidators


class SymbolValidator(_plotly_utils.basevalidators.StringValidator):

    def __init__(
        self,
        plotly_name='symbol',
        parent_name='scattermapbox.marker',
        **kwargs
    ):
        super(SymbolValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            array_ok=True,
            edit_type='calc',
            role='style',
            **kwargs
        )
