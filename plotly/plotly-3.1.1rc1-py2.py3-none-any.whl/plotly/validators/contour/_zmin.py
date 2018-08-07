import _plotly_utils.basevalidators


class ZminValidator(_plotly_utils.basevalidators.NumberValidator):

    def __init__(self, plotly_name='zmin', parent_name='contour', **kwargs):
        super(ZminValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calc',
            implied_edits={'zauto': False},
            role='info',
            **kwargs
        )
