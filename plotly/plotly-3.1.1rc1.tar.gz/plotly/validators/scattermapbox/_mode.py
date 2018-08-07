import _plotly_utils.basevalidators


class ModeValidator(_plotly_utils.basevalidators.FlaglistValidator):

    def __init__(
        self, plotly_name='mode', parent_name='scattermapbox', **kwargs
    ):
        super(ModeValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calc',
            extras=['none'],
            flags=['lines', 'markers', 'text'],
            role='info',
            **kwargs
        )
