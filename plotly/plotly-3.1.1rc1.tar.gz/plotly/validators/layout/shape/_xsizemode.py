import _plotly_utils.basevalidators


class XsizemodeValidator(_plotly_utils.basevalidators.EnumeratedValidator):

    def __init__(
        self, plotly_name='xsizemode', parent_name='layout.shape', **kwargs
    ):
        super(XsizemodeValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calcIfAutorange+arraydraw',
            role='info',
            values=['scaled', 'pixel'],
            **kwargs
        )
