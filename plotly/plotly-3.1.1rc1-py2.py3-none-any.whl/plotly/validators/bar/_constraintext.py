import _plotly_utils.basevalidators


class ConstraintextValidator(_plotly_utils.basevalidators.EnumeratedValidator):

    def __init__(
        self, plotly_name='constraintext', parent_name='bar', **kwargs
    ):
        super(ConstraintextValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calc',
            role='info',
            values=['inside', 'outside', 'both', 'none'],
            **kwargs
        )
