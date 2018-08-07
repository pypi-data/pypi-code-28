import _plotly_utils.basevalidators


class BorderwidthValidator(_plotly_utils.basevalidators.IntegerValidator):

    def __init__(
        self,
        plotly_name='borderwidth',
        parent_name='layout.xaxis.rangeslider',
        **kwargs
    ):
        super(BorderwidthValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='plot',
            min=0,
            role='style',
            **kwargs
        )
