import _plotly_utils.basevalidators


class BaxisValidator(_plotly_utils.basevalidators.CompoundValidator):

    def __init__(
        self, plotly_name='baxis', parent_name='layout.ternary', **kwargs
    ):
        super(BaxisValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            data_class_str='Baxis',
            data_docs="""
            color
                Sets default for all colors associated with
                this axis all at once: line, font, tick, and
                grid colors. Grid color is lightened by
                blending this with the plot background
                Individual pieces can override this.
            dtick
                Sets the step in-between ticks on this axis.
                Use with `tick0`. Must be a positive number, or
                special strings available to *log* and *date*
                axes. If the axis `type` is *log*, then ticks
                are set every 10^(n*dtick) where n is the tick
                number. For example, to set a tick mark at 1,
                10, 100, 1000, ... set dtick to 1. To set tick
                marks at 1, 100, 10000, ... set dtick to 2. To
                set tick marks at 1, 5, 25, 125, 625, 3125, ...
                set dtick to log_10(5), or 0.69897000433. *log*
                has several special values; *L<f>*, where `f`
                is a positive number, gives ticks linearly
                spaced in value (but not position). For example
                `tick0` = 0.1, `dtick` = *L0.5* will put ticks
                at 0.1, 0.6, 1.1, 1.6 etc. To show powers of 10
                plus small digits between, use *D1* (all
                digits) or *D2* (only 2 and 5). `tick0` is
                ignored for *D1* and *D2*. If the axis `type`
                is *date*, then you must convert the time to
                milliseconds. For example, to set the interval
                between ticks to one day, set `dtick` to
                86400000.0. *date* also has special values
                *M<n>* gives ticks spaced by a number of
                months. `n` must be a positive integer. To set
                ticks on the 15th of every third month, set
                `tick0` to *2000-01-15* and `dtick` to *M3*. To
                set ticks every 4 years, set `dtick` to *M48*
            exponentformat
                Determines a formatting rule for the tick
                exponents. For example, consider the number
                1,000,000,000. If *none*, it appears as
                1,000,000,000. If *e*, 1e+9. If *E*, 1E+9. If
                *power*, 1x10^9 (with 9 in a super script). If
                *SI*, 1G. If *B*, 1B.
            gridcolor
                Sets the color of the grid lines.
            gridwidth
                Sets the width (in px) of the grid lines.
            hoverformat
                Sets the hover text formatting rule using d3
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
            layer
                Sets the layer on which this axis is displayed.
                If *above traces*, this axis is displayed above
                all the subplot's traces If *below traces*,
                this axis is displayed below all the subplot's
                traces, but above the grid lines. Useful when
                used together with scatter-like traces with
                `cliponaxis` set to *false* to show markers
                and/or text nodes above this axis.
            linecolor
                Sets the axis line color.
            linewidth
                Sets the width (in px) of the axis line.
            min
                The minimum value visible on this axis. The
                maximum is determined by the sum minus the
                minimum values of the other two axes. The full
                view corresponds to all the minima set to zero.
            nticks
                Specifies the maximum number of ticks for the
                particular axis. The actual number of ticks
                will be chosen automatically to be less than or
                equal to `nticks`. Has an effect only if
                `tickmode` is set to *auto*.
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
                Determines whether or not the tick labels are
                drawn.
            showtickprefix
                If *all*, all tick labels are displayed with a
                prefix. If *first*, only the first tick is
                displayed with a prefix. If *last*, only the
                last tick is displayed with a suffix. If
                *none*, tick prefixes are hidden.
            showticksuffix
                Same as `showtickprefix` but for tick suffixes.
            tick0
                Sets the placement of the first tick on this
                axis. Use with `dtick`. If the axis `type` is
                *log*, then you must take the log of your
                starting tick (e.g. to set the starting tick to
                100, set the `tick0` to 2) except when
                `dtick`=*L<f>* (see `dtick` for more info). If
                the axis `type` is *date*, it should be a date
                string, like date data. If the axis `type` is
                *category*, it should be a number, using the
                scale where each category is assigned a serial
                number from zero in the order it appears.
            tickangle
                Sets the angle of the tick labels with respect
                to the horizontal. For example, a `tickangle`
                of -90 draws the tick labels vertically.
            tickcolor
                Sets the tick color.
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
                plotly.graph_objs.layout.ternary.baxis.Tickform
                atstop instance or dict with compatible
                properties
            ticklen
                Sets the tick length (in px).
            tickmode
                Sets the tick mode for this axis. If *auto*,
                the number of ticks is set via `nticks`. If
                *linear*, the placement of the ticks is
                determined by a starting position `tick0` and a
                tick step `dtick` (*linear* is the default
                value if `tick0` and `dtick` are provided). If
                *array*, the placement of the ticks is set via
                `tickvals` and the tick text is `ticktext`.
                (*array* is the default value if `tickvals` is
                provided).
            tickprefix
                Sets a tick label prefix.
            ticks
                Determines whether ticks are drawn or not. If
                **, this axis' ticks are not drawn. If
                *outside* (*inside*), this axis' are drawn
                outside (inside) the axis lines.
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
            tickwidth
                Sets the tick width (in px).
            title
                Sets the title of this axis.
            titlefont
                Sets this axis' title font.""",
            **kwargs
        )
