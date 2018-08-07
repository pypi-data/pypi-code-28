import _plotly_utils.basevalidators


class SeparatethousandsValidator(
    _plotly_utils.basevalidators.BooleanValidator
):

    def __init__(
        self,
        plotly_name='separatethousands',
        parent_name='bar.marker.colorbar',
        **kwargs
    ):
        super(SeparatethousandsValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='colorbars',
            role='style',
            **kwargs
        )
