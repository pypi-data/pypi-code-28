import _plotly_utils.basevalidators


class TValidator(_plotly_utils.basevalidators.NumberValidator):

    def __init__(
        self, plotly_name='t', parent_name='layout.updatemenu.pad', **kwargs
    ):
        super(TValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='arraydraw',
            role='style',
            **kwargs
        )
