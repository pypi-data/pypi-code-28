import _plotly_utils.basevalidators


class OutlierwidthValidator(_plotly_utils.basevalidators.NumberValidator):

    def __init__(
        self,
        plotly_name='outlierwidth',
        parent_name='box.marker.line',
        **kwargs
    ):
        super(OutlierwidthValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='style',
            min=0,
            role='style',
            **kwargs
        )
