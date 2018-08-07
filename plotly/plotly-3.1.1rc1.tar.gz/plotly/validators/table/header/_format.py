import _plotly_utils.basevalidators


class FormatValidator(_plotly_utils.basevalidators.DataArrayValidator):

    def __init__(
        self, plotly_name='format', parent_name='table.header', **kwargs
    ):
        super(FormatValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calc',
            role='data',
            **kwargs
        )
