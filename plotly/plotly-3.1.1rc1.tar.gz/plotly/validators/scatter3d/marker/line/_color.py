import _plotly_utils.basevalidators


class ColorValidator(_plotly_utils.basevalidators.ColorValidator):

    def __init__(
        self,
        plotly_name='color',
        parent_name='scatter3d.marker.line',
        **kwargs
    ):
        super(ColorValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            array_ok=True,
            edit_type='calc',
            role='style',
            colorscale_path='scatter3d.marker.line.colorscale',
            **kwargs
        )
