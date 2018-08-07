import _plotly_utils.basevalidators


class DurationValidator(_plotly_utils.basevalidators.NumberValidator):

    def __init__(
        self,
        plotly_name='duration',
        parent_name='layout.slider.transition',
        **kwargs
    ):
        super(DurationValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='arraydraw',
            min=0,
            role='info',
            **kwargs
        )
