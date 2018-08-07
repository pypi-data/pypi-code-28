import _plotly_utils.basevalidators


class StartValidator(_plotly_utils.basevalidators.NumberValidator):

    def __init__(
        self,
        plotly_name='start',
        parent_name='contourcarpet.contours',
        **kwargs
    ):
        super(StartValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='plot',
            implied_edits={'^autocontour': False},
            role='style',
            **kwargs
        )
