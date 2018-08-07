import _plotly_utils.basevalidators


class NbinsxValidator(_plotly_utils.basevalidators.IntegerValidator):

    def __init__(
        self, plotly_name='nbinsx', parent_name='histogram2dcontour', **kwargs
    ):
        super(NbinsxValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calc',
            min=0,
            role='style',
            **kwargs
        )
