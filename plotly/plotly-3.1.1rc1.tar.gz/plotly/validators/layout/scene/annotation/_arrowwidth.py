import _plotly_utils.basevalidators


class ArrowwidthValidator(_plotly_utils.basevalidators.NumberValidator):

    def __init__(
        self,
        plotly_name='arrowwidth',
        parent_name='layout.scene.annotation',
        **kwargs
    ):
        super(ArrowwidthValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calc',
            min=0.1,
            role='style',
            **kwargs
        )
