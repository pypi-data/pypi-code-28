import _plotly_utils.basevalidators


class RivercolorValidator(_plotly_utils.basevalidators.ColorValidator):

    def __init__(
        self, plotly_name='rivercolor', parent_name='layout.geo', **kwargs
    ):
        super(RivercolorValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='plot',
            role='style',
            **kwargs
        )
