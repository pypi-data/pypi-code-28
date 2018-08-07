import _plotly_utils.basevalidators


class ShowtickprefixValidator(
    _plotly_utils.basevalidators.EnumeratedValidator
):

    def __init__(
        self,
        plotly_name='showtickprefix',
        parent_name='heatmapgl.colorbar',
        **kwargs
    ):
        super(ShowtickprefixValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calc',
            role='style',
            values=['all', 'first', 'last', 'none'],
            **kwargs
        )
