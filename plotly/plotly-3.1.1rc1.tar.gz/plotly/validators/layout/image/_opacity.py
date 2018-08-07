import _plotly_utils.basevalidators


class OpacityValidator(_plotly_utils.basevalidators.NumberValidator):

    def __init__(
        self, plotly_name='opacity', parent_name='layout.image', **kwargs
    ):
        super(OpacityValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='arraydraw',
            max=1,
            min=0,
            role='info',
            **kwargs
        )
