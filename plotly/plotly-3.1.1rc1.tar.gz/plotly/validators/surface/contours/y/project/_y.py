import _plotly_utils.basevalidators


class YValidator(_plotly_utils.basevalidators.BooleanValidator):

    def __init__(
        self,
        plotly_name='y',
        parent_name='surface.contours.y.project',
        **kwargs
    ):
        super(YValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calc',
            role='info',
            **kwargs
        )
