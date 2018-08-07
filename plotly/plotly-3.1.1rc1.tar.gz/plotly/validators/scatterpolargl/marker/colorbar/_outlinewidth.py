import _plotly_utils.basevalidators


class OutlinewidthValidator(_plotly_utils.basevalidators.NumberValidator):

    def __init__(
        self,
        plotly_name='outlinewidth',
        parent_name='scatterpolargl.marker.colorbar',
        **kwargs
    ):
        super(OutlinewidthValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calc',
            min=0,
            role='style',
            **kwargs
        )
