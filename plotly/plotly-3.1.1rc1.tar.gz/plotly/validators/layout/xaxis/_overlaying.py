import _plotly_utils.basevalidators


class OverlayingValidator(_plotly_utils.basevalidators.EnumeratedValidator):

    def __init__(
        self, plotly_name='overlaying', parent_name='layout.xaxis', **kwargs
    ):
        super(OverlayingValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='plot',
            role='info',
            values=[
                'free', '/^x([2-9]|[1-9][0-9]+)?$/',
                '/^y([2-9]|[1-9][0-9]+)?$/'
            ],
            **kwargs
        )
