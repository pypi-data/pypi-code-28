import _plotly_utils.basevalidators


class OutlinecolorValidator(_plotly_utils.basevalidators.ColorValidator):

    def __init__(
        self,
        plotly_name='outlinecolor',
        parent_name='layout.mapbox.layer.fill',
        **kwargs
    ):
        super(OutlinecolorValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='plot',
            role='style',
            **kwargs
        )
