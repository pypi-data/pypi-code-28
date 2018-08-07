import _plotly_utils.basevalidators


class TicklenValidator(_plotly_utils.basevalidators.NumberValidator):

    def __init__(
        self,
        plotly_name='ticklen',
        parent_name='layout.scene.yaxis',
        **kwargs
    ):
        super(TicklenValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='plot',
            min=0,
            role='style',
            **kwargs
        )
