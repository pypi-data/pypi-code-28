import _plotly_utils.basevalidators


class AaxisValidator(_plotly_utils.basevalidators.CompoundValidator):

    def __init__(self, plotly_name='aaxis', parent_name='carpet', **kwargs):
        super(AaxisValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            data_class_str='Aaxis',
            data_docs="""
            arraydtick
                The stride between grid lines along the axis
            arraytick0
                The starting index of grid lines along the axis
            autorange
                Determines whether or not the range of this
                axis is computed in relation to the input data.
                See `rangemode` for more info. If `range` is
                provided, then `autorange` is set to *false*.
            categoryarray
                Sets the order in which categories on this axis
                appear. Only has an effect if `categoryorder`
                is set to *array*. Used with `categoryorder`.
            categoryarraysrc
                Sets the source reference on plot.ly for
                categoryarray .
            categoryorder
                Specifies the ordering logic for the case of
                categorical variables. By default, plotly uses
                *trace*, which specifies the order that is
                present in the data supplied. Set
                `categoryorder` to *category ascending* or
                *category descending* if order should be
                determined by the alphanumerical order of the
                category names. Set `categoryorder` to *array*
                to derive the ordering from the attribute
                `categoryarray`. If a category is not found in
                the `categoryarray` array, the sorting behavior
                for that attribute will be identical to the
                *trace* mode. The unspecified categories will
                follow the categories in `categoryarray`.
            cheatertype

            color
                Sets default for all colors associated with
                this axis all at once: line, font, tick, and
                grid colors. Grid color is lightened by
                blending this with the plot background
                Individual pieces can override this.
            dtick
                The stride between grid lines along the axis
            endline
                Determines whether or not a line is drawn at
                along the final value of this axis. If *true*,
                the end line is drawn on top of the grid lines.
            endlinecolor
                Sets the line color of the end line.
            endlinewidth
                Sets the width (in px) of the end line.
            exponentformat
                Determines a formatting rule for the tick
                exponents. For example, consider the number
                1,000,000,000. If *none*, it appears as
                1,000,000,000. If *e*, 1e+9. If *E*, 1E+9. If
                *power*, 1x10^9 (with 9 in a super script). If
                *SI*, 1G. If *B*, 1B.
            fixedrange
                Determines whether or not this axis is zoom-
                able. If true, then zoom is disabled.
            gridcolor
                Sets the axis line color.
            gridwidth
                Sets the width (in px) of the axis line.
            labelpadding
                Extra padding between label and the axis
            labelprefix
                Sets a axis label prefix.
            labelsuffix
                Sets a axis label suffix.
            linecolor
                Sets the axis line color.
            linewidth
                Sets the width (in px) of the axis line.
            minorgridcolor
                Sets the color of the grid lines.
            minorgridcount
                Sets the number of minor grid ticks per major
                grid tick
            minorgridwidth
                Sets the width (in px) of the grid lines.
            nticks
                Specifies the maximum number of ticks for the
                particular axis. The actual number of ticks
                will be chosen automatically to be less than or
                equal to `nticks`. Has an effect only if
                `tickmode` is set to *auto*.
            range
                Sets the range of this axis. If the axis `type`
                is *log*, then you must take the log of your
                desired range (e.g. to set the range from 1 to
                100, set the range from 0 to 2). If the axis
                `type` is *date*, it should be date strings,
                like date data, though Date objects and unix
                milliseconds will be accepted and converted to
                strings. If the axis `type` is *category*, it
                should be numbers, using the scale where each
                category is assigned a serial number from zero
                in the order it appears.
            rangemode
                If *normal*, the range is computed in relation
                to the extrema of the input data. If *tozero*`,
                the range extends to 0, regardless of the input
                data If *nonnegative*, the range is non-
                negative, regardless of the input data.
            separatethousands
                If "true", even 4-digit integers are separated
            showexponent
                If *all*, all exponents are shown besides their
                significands. If *first*, only the exponent of
                the first tick is shown. If *last*, only the
                exponent of the last tick is shown. If *none*,
                no exponents appear.
            showgrid
                Determines whether or not grid lines are drawn.
                If *true*, the grid lines are drawn at every
                tick mark.
            showline
                Determines whether or not a line bounding this
                axis is drawn.
            showticklabels
                Determines whether axis labels are drawn on the
                low side, the high side, both, or neither side
                of the axis.
            showtickprefix
                If *all*, all tick labels are displayed with a
                prefix. If *first*, only the first tick is
                displayed with a prefix. If *last*, only the
                last tick is displayed with a suffix. If
                *none*, tick prefixes are hidden.
            showticksuffix
                Same as `showtickprefix` but for tick suffixes.
            smoothing

            startline
                Determines whether or not a line is drawn at
                along the starting value of this axis. If
                *true*, the start line is drawn on top of the
                grid lines.
            startlinecolor
                Sets the line color of the start line.
            startlinewidth
                Sets the width (in px) of the start line.
            tick0
                The starting index of grid lines along the axis
            tickangle
                Sets the angle of the tick labels with respect
                to the horizontal. For example, a `tickangle`
                of -90 draws the tick labels vertically.
            tickfont
                Sets the tick font.
            tickformat
                Sets the tick label formatting rule using d3
                formatting mini-languages which are very
                similar to those in Python. For numbers, see: h
                ttps://github.com/d3/d3-format/blob/master/READ
                ME.md#locale_format And for dates see:
                https://github.com/d3/d3-time-
                format/blob/master/README.md#locale_format We
                add one item to d3's date formatter: *%{n}f*
                for fractional seconds with n digits. For
                example, *2016-10-13 09:15:23.456* with
                tickformat *%H~%M~%S.%2f* would display
                *09~15~23.46*
            tickformatstops
                plotly.graph_objs.carpet.aaxis.Tickformatstop
                instance or dict with compatible properties
            tickmode

            tickprefix
                Sets a tick label prefix.
            ticksuffix
                Sets a tick label suffix.
            ticktext
                Sets the text displayed at the ticks position
                via `tickvals`. Only has an effect if
                `tickmode` is set to *array*. Used with
                `tickvals`.
            ticktextsrc
                Sets the source reference on plot.ly for
                ticktext .
            tickvals
                Sets the values at which ticks on this axis
                appear. Only has an effect if `tickmode` is set
                to *array*. Used with `ticktext`.
            tickvalssrc
                Sets the source reference on plot.ly for
                tickvals .
            title
                Sets the title of this axis.
            titlefont
                Sets this axis' title font.
            titleoffset
                An additional amount by which to offset the
                title from the tick labels, given in pixels
            type
                Sets the axis type. By default, plotly attempts
                to determined the axis type by looking into the
                data of the traces that referenced the axis in
                question.""",
            **kwargs
        )
