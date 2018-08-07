import _plotly_utils.basevalidators


class XValidator(_plotly_utils.basevalidators.AnyValidator):

    def __init__(self, plotly_name='x', parent_name='layout.image', **kwargs):
        super(XValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='arraydraw',
            role='info',
            **kwargs
        )
