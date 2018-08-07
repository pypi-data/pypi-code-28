import _plotly_utils.basevalidators


class BorderwidthValidator(_plotly_utils.basevalidators.NumberValidator):

    def __init__(
        self, plotly_name='borderwidth', parent_name='layout.slider', **kwargs
    ):
        super(BorderwidthValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='arraydraw',
            min=0,
            role='style',
            **kwargs
        )
