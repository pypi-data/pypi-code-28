import _plotly_utils.basevalidators


class AyValidator(_plotly_utils.basevalidators.NumberValidator):

    def __init__(
        self,
        plotly_name='ay',
        parent_name='layout.scene.annotation',
        **kwargs
    ):
        super(AyValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calc',
            role='info',
            **kwargs
        )
