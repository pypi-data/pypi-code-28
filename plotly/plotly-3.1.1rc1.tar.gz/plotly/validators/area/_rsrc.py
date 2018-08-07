import _plotly_utils.basevalidators


class RsrcValidator(_plotly_utils.basevalidators.SrcValidator):

    def __init__(self, plotly_name='rsrc', parent_name='area', **kwargs):
        super(RsrcValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='none',
            role='info',
            **kwargs
        )
