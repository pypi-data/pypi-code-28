import _plotly_utils.basevalidators


class HovertextValidator(_plotly_utils.basevalidators.StringValidator):

    def __init__(self, plotly_name='hovertext', parent_name='bar', **kwargs):
        super(HovertextValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            array_ok=True,
            edit_type='style',
            role='info',
            **kwargs
        )
