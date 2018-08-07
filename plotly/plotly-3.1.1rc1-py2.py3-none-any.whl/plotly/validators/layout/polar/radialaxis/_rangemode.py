import _plotly_utils.basevalidators


class RangemodeValidator(_plotly_utils.basevalidators.EnumeratedValidator):

    def __init__(
        self,
        plotly_name='rangemode',
        parent_name='layout.polar.radialaxis',
        **kwargs
    ):
        super(RangemodeValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calc',
            role='style',
            values=['tozero', 'nonnegative', 'normal'],
            **kwargs
        )
