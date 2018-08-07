import _plotly_utils.basevalidators


class OffsetsrcValidator(_plotly_utils.basevalidators.SrcValidator):

    def __init__(self, plotly_name='offsetsrc', parent_name='bar', **kwargs):
        super(OffsetsrcValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='none',
            role='info',
            **kwargs
        )
