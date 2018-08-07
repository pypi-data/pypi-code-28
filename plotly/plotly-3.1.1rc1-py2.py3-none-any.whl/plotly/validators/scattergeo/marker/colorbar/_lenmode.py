import _plotly_utils.basevalidators


class LenmodeValidator(_plotly_utils.basevalidators.EnumeratedValidator):

    def __init__(
        self,
        plotly_name='lenmode',
        parent_name='scattergeo.marker.colorbar',
        **kwargs
    ):
        super(LenmodeValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calc',
            role='info',
            values=['fraction', 'pixels'],
            **kwargs
        )
