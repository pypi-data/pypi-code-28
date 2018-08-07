import _plotly_utils.basevalidators


class TicktextsrcValidator(_plotly_utils.basevalidators.SrcValidator):

    def __init__(
        self,
        plotly_name='ticktextsrc',
        parent_name='mesh3d.colorbar',
        **kwargs
    ):
        super(TicktextsrcValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='none',
            role='info',
            **kwargs
        )
