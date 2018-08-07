import _plotly_utils.basevalidators


class MarkerValidator(_plotly_utils.basevalidators.CompoundValidator):

    def __init__(
        self,
        plotly_name='marker',
        parent_name='scattergl.unselected',
        **kwargs
    ):
        super(MarkerValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            data_class_str='Marker',
            data_docs="""
            color
                Sets the marker color of unselected points,
                applied only when a selection exists.
            opacity
                Sets the marker opacity of unselected points,
                applied only when a selection exists.
            size
                Sets the marker size of unselected points,
                applied only when a selection exists.""",
            **kwargs
        )
