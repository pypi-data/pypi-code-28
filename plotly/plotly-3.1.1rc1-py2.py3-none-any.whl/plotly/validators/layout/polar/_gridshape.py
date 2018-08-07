import _plotly_utils.basevalidators


class GridshapeValidator(_plotly_utils.basevalidators.EnumeratedValidator):

    def __init__(
        self, plotly_name='gridshape', parent_name='layout.polar', **kwargs
    ):
        super(GridshapeValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='plot',
            role='style',
            values=['circular', 'linear'],
            **kwargs
        )
