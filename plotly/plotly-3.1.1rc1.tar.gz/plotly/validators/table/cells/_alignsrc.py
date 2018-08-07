import _plotly_utils.basevalidators


class AlignsrcValidator(_plotly_utils.basevalidators.SrcValidator):

    def __init__(
        self, plotly_name='alignsrc', parent_name='table.cells', **kwargs
    ):
        super(AlignsrcValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='none',
            role='info',
            **kwargs
        )
