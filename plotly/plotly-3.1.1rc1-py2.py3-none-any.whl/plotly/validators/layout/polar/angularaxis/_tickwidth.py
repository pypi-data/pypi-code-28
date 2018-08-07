import _plotly_utils.basevalidators


class TickwidthValidator(_plotly_utils.basevalidators.NumberValidator):

    def __init__(
        self,
        plotly_name='tickwidth',
        parent_name='layout.polar.angularaxis',
        **kwargs
    ):
        super(TickwidthValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='plot',
            min=0,
            role='style',
            **kwargs
        )
