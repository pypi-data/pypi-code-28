import _plotly_utils.basevalidators


class ExponentformatValidator(
    _plotly_utils.basevalidators.EnumeratedValidator
):

    def __init__(
        self,
        plotly_name='exponentformat',
        parent_name='carpet.baxis',
        **kwargs
    ):
        super(ExponentformatValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type='calc',
            role='style',
            values=['none', 'e', 'E', 'power', 'SI', 'B'],
            **kwargs
        )
