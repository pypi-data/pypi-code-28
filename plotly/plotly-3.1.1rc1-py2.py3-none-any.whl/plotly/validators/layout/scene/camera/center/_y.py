import _plotly_utils.basevalidators


class YValidator(_plotly_utils.basevalidators.NumberValidator):

    def __init__(
        self,
        plotly_name='y',
        parent_name='layout.scene.camera.center',
        **kwargs
    ):
        super(YValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='camera',
            role='info',
            **kwargs
        )
