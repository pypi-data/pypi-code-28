import _plotly_utils.basevalidators


class BtypeValidator(_plotly_utils.basevalidators.EnumeratedValidator):

    def __init__(
        self, plotly_name='btype', parent_name='contourcarpet', **kwargs
    ):
        super(BtypeValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calc+clearAxisTypes',
            role='info',
            values=['array', 'scaled'],
            **kwargs
        )
