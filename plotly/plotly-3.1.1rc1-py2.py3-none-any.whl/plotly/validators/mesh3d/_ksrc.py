import _plotly_utils.basevalidators


class KsrcValidator(_plotly_utils.basevalidators.SrcValidator):

    def __init__(self, plotly_name='ksrc', parent_name='mesh3d', **kwargs):
        super(KsrcValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='none',
            role='info',
            **kwargs
        )
