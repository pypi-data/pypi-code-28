import _plotly_utils.basevalidators


class UsecolormapValidator(_plotly_utils.basevalidators.BooleanValidator):

    def __init__(
        self,
        plotly_name='usecolormap',
        parent_name='surface.contours.z',
        **kwargs
    ):
        super(UsecolormapValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calc',
            role='info',
            **kwargs
        )
