from plotly.basedatatypes import BaseLayoutHierarchyType
import copy


class YAxis(BaseLayoutHierarchyType):

    # anchor
    # ------
    @property
    def anchor(self):
        """
        If set to an opposite-letter axis id (e.g. `x2`, `y`), this
        axis is bound to the corresponding opposite-letter axis. If set
        to *free*, this axis' position is determined by `position`.
    
        The 'anchor' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                ['free']
          - A string that matches one of the following regular expressions:
                ['^x([2-9]|[1-9][0-9]+)?$', '^y([2-9]|[1-9][0-9]+)?$']

        Returns
        -------
        Any
        """
        return self['anchor']

    @anchor.setter
    def anchor(self, val):
        self['anchor'] = val

    # automargin
    # ----------
    @property
    def automargin(self):
        """
        Determines whether long tick labels automatically grow the
        figure margins.
    
        The 'automargin' property must be specified as a bool
        (either True, or False)

        Returns
        -------
        bool
        """
        return self['automargin']

    @automargin.setter
    def automargin(self, val):
        self['automargin'] = val

    # autorange
    # ---------
    @property
    def autorange(self):
        """
        Determines whether or not the range of this axis is computed in
        relation to the input data. See `rangemode` for more info. If
        `range` is provided, then `autorange` is set to *false*.
    
        The 'autorange' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                [True, False, 'reversed']

        Returns
        -------
        Any
        """
        return self['autorange']

    @autorange.setter
    def autorange(self, val):
        self['autorange'] = val

    # calendar
    # --------
    @property
    def calendar(self):
        """
        Sets the calendar system to use for `range` and `tick0` if this
        is a date axis. This does not set the calendar for interpreting
        data on this axis, that's specified in the trace or via the
        global `layout.calendar`
    
        The 'calendar' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                ['gregorian', 'chinese', 'coptic', 'discworld',
                'ethiopian', 'hebrew', 'islamic', 'julian', 'mayan',
                'nanakshahi', 'nepali', 'persian', 'jalali', 'taiwan',
                'thai', 'ummalqura']

        Returns
        -------
        Any
        """
        return self['calendar']

    @calendar.setter
    def calendar(self, val):
        self['calendar'] = val

    # categoryarray
    # -------------
    @property
    def categoryarray(self):
        """
        Sets the order in which categories on this axis appear. Only
        has an effect if `categoryorder` is set to *array*. Used with
        `categoryorder`.
    
        The 'categoryarray' property is an array that may be specified as a tuple,
        list, numpy array, or pandas Series

        Returns
        -------
        numpy.ndarray
        """
        return self['categoryarray']

    @categoryarray.setter
    def categoryarray(self, val):
        self['categoryarray'] = val

    # categoryarraysrc
    # ----------------
    @property
    def categoryarraysrc(self):
        """
        Sets the source reference on plot.ly for  categoryarray .
    
        The 'categoryarraysrc' property must be specified as a string or
        as a plotly.grid_objs.Column object

        Returns
        -------
        str
        """
        return self['categoryarraysrc']

    @categoryarraysrc.setter
    def categoryarraysrc(self, val):
        self['categoryarraysrc'] = val

    # categoryorder
    # -------------
    @property
    def categoryorder(self):
        """
        Specifies the ordering logic for the case of categorical
        variables. By default, plotly uses *trace*, which specifies the
        order that is present in the data supplied. Set `categoryorder`
        to *category ascending* or *category descending* if order
        should be determined by the alphanumerical order of the
        category names. Set `categoryorder` to *array* to derive the
        ordering from the attribute `categoryarray`. If a category is
        not found in the `categoryarray` array, the sorting behavior
        for that attribute will be identical to the *trace* mode. The
        unspecified categories will follow the categories in
        `categoryarray`.
    
        The 'categoryorder' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                ['trace', 'category ascending', 'category descending',
                'array']

        Returns
        -------
        Any
        """
        return self['categoryorder']

    @categoryorder.setter
    def categoryorder(self, val):
        self['categoryorder'] = val

    # color
    # -----
    @property
    def color(self):
        """
        Sets default for all colors associated with this axis all at
        once: line, font, tick, and grid colors. Grid color is
        lightened by blending this with the plot background Individual
        pieces can override this.
    
        The 'color' property is a color and may be specified as:
          - A hex string (e.g. '#ff0000')
          - An rgb/rgba string (e.g. 'rgb(255,0,0)')
          - An hsl/hsla string (e.g. 'hsl(0,100%,50%)')
          - An hsv/hsva string (e.g. 'hsv(0,100%,100%)')
          - A named CSS color:
                aliceblue, antiquewhite, aqua, aquamarine, azure,
                beige, bisque, black, blanchedalmond, blue,
                blueviolet, brown, burlywood, cadetblue,
                chartreuse, chocolate, coral, cornflowerblue,
                cornsilk, crimson, cyan, darkblue, darkcyan,
                darkgoldenrod, darkgray, darkgrey, darkgreen,
                darkkhaki, darkmagenta, darkolivegreen, darkorange,
                darkorchid, darkred, darksalmon, darkseagreen,
                darkslateblue, darkslategray, darkslategrey,
                darkturquoise, darkviolet, deeppink, deepskyblue,
                dimgray, dimgrey, dodgerblue, firebrick,
                floralwhite, forestgreen, fuchsia, gainsboro,
                ghostwhite, gold, goldenrod, gray, grey, green,
                greenyellow, honeydew, hotpink, indianred, indigo,
                ivory, khaki, lavender, lavenderblush, lawngreen,
                lemonchiffon, lightblue, lightcoral, lightcyan,
                lightgoldenrodyellow, lightgray, lightgrey,
                lightgreen, lightpink, lightsalmon, lightseagreen,
                lightskyblue, lightslategray, lightslategrey,
                lightsteelblue, lightyellow, lime, limegreen,
                linen, magenta, maroon, mediumaquamarine,
                mediumblue, mediumorchid, mediumpurple,
                mediumseagreen, mediumslateblue, mediumspringgreen,
                mediumturquoise, mediumvioletred, midnightblue,
                mintcream, mistyrose, moccasin, navajowhite, navy,
                oldlace, olive, olivedrab, orange, orangered,
                orchid, palegoldenrod, palegreen, paleturquoise,
                palevioletred, papayawhip, peachpuff, peru, pink,
                plum, powderblue, purple, red, rosybrown,
                royalblue, saddlebrown, salmon, sandybrown,
                seagreen, seashell, sienna, silver, skyblue,
                slateblue, slategray, slategrey, snow, springgreen,
                steelblue, tan, teal, thistle, tomato, turquoise,
                violet, wheat, white, whitesmoke, yellow,
                yellowgreen

        Returns
        -------
        str
        """
        return self['color']

    @color.setter
    def color(self, val):
        self['color'] = val

    # constrain
    # ---------
    @property
    def constrain(self):
        """
        If this axis needs to be compressed (either due to its own
        `scaleanchor` and `scaleratio` or those of the other axis),
        determines how that happens: by increasing the *range*
        (default), or by decreasing the *domain*.
    
        The 'constrain' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                ['range', 'domain']

        Returns
        -------
        Any
        """
        return self['constrain']

    @constrain.setter
    def constrain(self, val):
        self['constrain'] = val

    # constraintoward
    # ---------------
    @property
    def constraintoward(self):
        """
        If this axis needs to be compressed (either due to its own
        `scaleanchor` and `scaleratio` or those of the other axis),
        determines which direction we push the originally specified
        plot area. Options are *left*, *center* (default), and *right*
        for x axes, and *top*, *middle* (default), and *bottom* for y
        axes.
    
        The 'constraintoward' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                ['left', 'center', 'right', 'top', 'middle', 'bottom']

        Returns
        -------
        Any
        """
        return self['constraintoward']

    @constraintoward.setter
    def constraintoward(self, val):
        self['constraintoward'] = val

    # domain
    # ------
    @property
    def domain(self):
        """
        Sets the domain of this axis (in plot fraction).
    
        The 'domain' property is an info array that may be specified as a
        list or tuple of 2 elements where:
    
    (0) The 'domain[0]' property is a number and may be specified as:
          - An int or float in the interval [0, 1]
    (1) The 'domain[1]' property is a number and may be specified as:
          - An int or float in the interval [0, 1]

        Returns
        -------
        list
        """
        return self['domain']

    @domain.setter
    def domain(self, val):
        self['domain'] = val

    # dtick
    # -----
    @property
    def dtick(self):
        """
        Sets the step in-between ticks on this axis. Use with `tick0`.
        Must be a positive number, or special strings available to
        *log* and *date* axes. If the axis `type` is *log*, then ticks
        are set every 10^(n*dtick) where n is the tick number. For
        example, to set a tick mark at 1, 10, 100, 1000, ... set dtick
        to 1. To set tick marks at 1, 100, 10000, ... set dtick to 2.
        To set tick marks at 1, 5, 25, 125, 625, 3125, ... set dtick to
        log_10(5), or 0.69897000433. *log* has several special values;
        *L<f>*, where `f` is a positive number, gives ticks linearly
        spaced in value (but not position). For example `tick0` = 0.1,
        `dtick` = *L0.5* will put ticks at 0.1, 0.6, 1.1, 1.6 etc. To
        show powers of 10 plus small digits between, use *D1* (all
        digits) or *D2* (only 2 and 5). `tick0` is ignored for *D1* and
        *D2*. If the axis `type` is *date*, then you must convert the
        time to milliseconds. For example, to set the interval between
        ticks to one day, set `dtick` to 86400000.0. *date* also has
        special values *M<n>* gives ticks spaced by a number of months.
        `n` must be a positive integer. To set ticks on the 15th of
        every third month, set `tick0` to *2000-01-15* and `dtick` to
        *M3*. To set ticks every 4 years, set `dtick` to *M48*
    
        The 'dtick' property accepts values of any type

        Returns
        -------
        Any
        """
        return self['dtick']

    @dtick.setter
    def dtick(self, val):
        self['dtick'] = val

    # exponentformat
    # --------------
    @property
    def exponentformat(self):
        """
        Determines a formatting rule for the tick exponents. For
        example, consider the number 1,000,000,000. If *none*, it
        appears as 1,000,000,000. If *e*, 1e+9. If *E*, 1E+9. If
        *power*, 1x10^9 (with 9 in a super script). If *SI*, 1G. If
        *B*, 1B.
    
        The 'exponentformat' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                ['none', 'e', 'E', 'power', 'SI', 'B']

        Returns
        -------
        Any
        """
        return self['exponentformat']

    @exponentformat.setter
    def exponentformat(self, val):
        self['exponentformat'] = val

    # fixedrange
    # ----------
    @property
    def fixedrange(self):
        """
        Determines whether or not this axis is zoom-able. If true, then
        zoom is disabled.
    
        The 'fixedrange' property must be specified as a bool
        (either True, or False)

        Returns
        -------
        bool
        """
        return self['fixedrange']

    @fixedrange.setter
    def fixedrange(self, val):
        self['fixedrange'] = val

    # gridcolor
    # ---------
    @property
    def gridcolor(self):
        """
        Sets the color of the grid lines.
    
        The 'gridcolor' property is a color and may be specified as:
          - A hex string (e.g. '#ff0000')
          - An rgb/rgba string (e.g. 'rgb(255,0,0)')
          - An hsl/hsla string (e.g. 'hsl(0,100%,50%)')
          - An hsv/hsva string (e.g. 'hsv(0,100%,100%)')
          - A named CSS color:
                aliceblue, antiquewhite, aqua, aquamarine, azure,
                beige, bisque, black, blanchedalmond, blue,
                blueviolet, brown, burlywood, cadetblue,
                chartreuse, chocolate, coral, cornflowerblue,
                cornsilk, crimson, cyan, darkblue, darkcyan,
                darkgoldenrod, darkgray, darkgrey, darkgreen,
                darkkhaki, darkmagenta, darkolivegreen, darkorange,
                darkorchid, darkred, darksalmon, darkseagreen,
                darkslateblue, darkslategray, darkslategrey,
                darkturquoise, darkviolet, deeppink, deepskyblue,
                dimgray, dimgrey, dodgerblue, firebrick,
                floralwhite, forestgreen, fuchsia, gainsboro,
                ghostwhite, gold, goldenrod, gray, grey, green,
                greenyellow, honeydew, hotpink, indianred, indigo,
                ivory, khaki, lavender, lavenderblush, lawngreen,
                lemonchiffon, lightblue, lightcoral, lightcyan,
                lightgoldenrodyellow, lightgray, lightgrey,
                lightgreen, lightpink, lightsalmon, lightseagreen,
                lightskyblue, lightslategray, lightslategrey,
                lightsteelblue, lightyellow, lime, limegreen,
                linen, magenta, maroon, mediumaquamarine,
                mediumblue, mediumorchid, mediumpurple,
                mediumseagreen, mediumslateblue, mediumspringgreen,
                mediumturquoise, mediumvioletred, midnightblue,
                mintcream, mistyrose, moccasin, navajowhite, navy,
                oldlace, olive, olivedrab, orange, orangered,
                orchid, palegoldenrod, palegreen, paleturquoise,
                palevioletred, papayawhip, peachpuff, peru, pink,
                plum, powderblue, purple, red, rosybrown,
                royalblue, saddlebrown, salmon, sandybrown,
                seagreen, seashell, sienna, silver, skyblue,
                slateblue, slategray, slategrey, snow, springgreen,
                steelblue, tan, teal, thistle, tomato, turquoise,
                violet, wheat, white, whitesmoke, yellow,
                yellowgreen

        Returns
        -------
        str
        """
        return self['gridcolor']

    @gridcolor.setter
    def gridcolor(self, val):
        self['gridcolor'] = val

    # gridwidth
    # ---------
    @property
    def gridwidth(self):
        """
        Sets the width (in px) of the grid lines.
    
        The 'gridwidth' property is a number and may be specified as:
          - An int or float in the interval [0, inf]

        Returns
        -------
        int|float
        """
        return self['gridwidth']

    @gridwidth.setter
    def gridwidth(self, val):
        self['gridwidth'] = val

    # hoverformat
    # -----------
    @property
    def hoverformat(self):
        """
        Sets the hover text formatting rule using d3 formatting mini-
        languages which are very similar to those in Python. For
        numbers, see: https://github.com/d3/d3-format/blob/master/READM
        E.md#locale_format And for dates see:
        https://github.com/d3/d3-time-
        format/blob/master/README.md#locale_format We add one item to
        d3's date formatter: *%{n}f* for fractional seconds with n
        digits. For example, *2016-10-13 09:15:23.456* with tickformat
        *%H~%M~%S.%2f* would display *09~15~23.46*
    
        The 'hoverformat' property is a string and must be specified as:
          - A string
          - A number that will be converted to a string

        Returns
        -------
        str
        """
        return self['hoverformat']

    @hoverformat.setter
    def hoverformat(self, val):
        self['hoverformat'] = val

    # layer
    # -----
    @property
    def layer(self):
        """
        Sets the layer on which this axis is displayed. If *above
        traces*, this axis is displayed above all the subplot's traces
        If *below traces*, this axis is displayed below all the
        subplot's traces, but above the grid lines. Useful when used
        together with scatter-like traces with `cliponaxis` set to
        *false* to show markers and/or text nodes above this axis.
    
        The 'layer' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                ['above traces', 'below traces']

        Returns
        -------
        Any
        """
        return self['layer']

    @layer.setter
    def layer(self, val):
        self['layer'] = val

    # linecolor
    # ---------
    @property
    def linecolor(self):
        """
        Sets the axis line color.
    
        The 'linecolor' property is a color and may be specified as:
          - A hex string (e.g. '#ff0000')
          - An rgb/rgba string (e.g. 'rgb(255,0,0)')
          - An hsl/hsla string (e.g. 'hsl(0,100%,50%)')
          - An hsv/hsva string (e.g. 'hsv(0,100%,100%)')
          - A named CSS color:
                aliceblue, antiquewhite, aqua, aquamarine, azure,
                beige, bisque, black, blanchedalmond, blue,
                blueviolet, brown, burlywood, cadetblue,
                chartreuse, chocolate, coral, cornflowerblue,
                cornsilk, crimson, cyan, darkblue, darkcyan,
                darkgoldenrod, darkgray, darkgrey, darkgreen,
                darkkhaki, darkmagenta, darkolivegreen, darkorange,
                darkorchid, darkred, darksalmon, darkseagreen,
                darkslateblue, darkslategray, darkslategrey,
                darkturquoise, darkviolet, deeppink, deepskyblue,
                dimgray, dimgrey, dodgerblue, firebrick,
                floralwhite, forestgreen, fuchsia, gainsboro,
                ghostwhite, gold, goldenrod, gray, grey, green,
                greenyellow, honeydew, hotpink, indianred, indigo,
                ivory, khaki, lavender, lavenderblush, lawngreen,
                lemonchiffon, lightblue, lightcoral, lightcyan,
                lightgoldenrodyellow, lightgray, lightgrey,
                lightgreen, lightpink, lightsalmon, lightseagreen,
                lightskyblue, lightslategray, lightslategrey,
                lightsteelblue, lightyellow, lime, limegreen,
                linen, magenta, maroon, mediumaquamarine,
                mediumblue, mediumorchid, mediumpurple,
                mediumseagreen, mediumslateblue, mediumspringgreen,
                mediumturquoise, mediumvioletred, midnightblue,
                mintcream, mistyrose, moccasin, navajowhite, navy,
                oldlace, olive, olivedrab, orange, orangered,
                orchid, palegoldenrod, palegreen, paleturquoise,
                palevioletred, papayawhip, peachpuff, peru, pink,
                plum, powderblue, purple, red, rosybrown,
                royalblue, saddlebrown, salmon, sandybrown,
                seagreen, seashell, sienna, silver, skyblue,
                slateblue, slategray, slategrey, snow, springgreen,
                steelblue, tan, teal, thistle, tomato, turquoise,
                violet, wheat, white, whitesmoke, yellow,
                yellowgreen

        Returns
        -------
        str
        """
        return self['linecolor']

    @linecolor.setter
    def linecolor(self, val):
        self['linecolor'] = val

    # linewidth
    # ---------
    @property
    def linewidth(self):
        """
        Sets the width (in px) of the axis line.
    
        The 'linewidth' property is a number and may be specified as:
          - An int or float in the interval [0, inf]

        Returns
        -------
        int|float
        """
        return self['linewidth']

    @linewidth.setter
    def linewidth(self, val):
        self['linewidth'] = val

    # mirror
    # ------
    @property
    def mirror(self):
        """
        Determines if the axis lines or/and ticks are mirrored to the
        opposite side of the plotting area. If *true*, the axis lines
        are mirrored. If *ticks*, the axis lines and ticks are
        mirrored. If *false*, mirroring is disable. If *all*, axis
        lines are mirrored on all shared-axes subplots. If *allticks*,
        axis lines and ticks are mirrored on all shared-axes subplots.
    
        The 'mirror' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                [True, 'ticks', False, 'all', 'allticks']

        Returns
        -------
        Any
        """
        return self['mirror']

    @mirror.setter
    def mirror(self, val):
        self['mirror'] = val

    # nticks
    # ------
    @property
    def nticks(self):
        """
        Specifies the maximum number of ticks for the particular axis.
        The actual number of ticks will be chosen automatically to be
        less than or equal to `nticks`. Has an effect only if
        `tickmode` is set to *auto*.
    
        The 'nticks' property is a integer and may be specified as:
          - An int (or float that will be cast to an int)
            in the interval [0, 9223372036854775807]

        Returns
        -------
        int
        """
        return self['nticks']

    @nticks.setter
    def nticks(self, val):
        self['nticks'] = val

    # overlaying
    # ----------
    @property
    def overlaying(self):
        """
        If set a same-letter axis id, this axis is overlaid on top of
        the corresponding same-letter axis. If *false*, this axis does
        not overlay any same-letter axes.
    
        The 'overlaying' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                ['free']
          - A string that matches one of the following regular expressions:
                ['^x([2-9]|[1-9][0-9]+)?$', '^y([2-9]|[1-9][0-9]+)?$']

        Returns
        -------
        Any
        """
        return self['overlaying']

    @overlaying.setter
    def overlaying(self, val):
        self['overlaying'] = val

    # position
    # --------
    @property
    def position(self):
        """
        Sets the position of this axis in the plotting space (in
        normalized coordinates). Only has an effect if `anchor` is set
        to *free*.
    
        The 'position' property is a number and may be specified as:
          - An int or float in the interval [0, 1]

        Returns
        -------
        int|float
        """
        return self['position']

    @position.setter
    def position(self, val):
        self['position'] = val

    # range
    # -----
    @property
    def range(self):
        """
        Sets the range of this axis. If the axis `type` is *log*, then
        you must take the log of your desired range (e.g. to set the
        range from 1 to 100, set the range from 0 to 2). If the axis
        `type` is *date*, it should be date strings, like date data,
        though Date objects and unix milliseconds will be accepted and
        converted to strings. If the axis `type` is *category*, it
        should be numbers, using the scale where each category is
        assigned a serial number from zero in the order it appears.
    
        The 'range' property is an info array that may be specified as a
        list or tuple of 2 elements where:
    
    (0) The 'range[0]' property accepts values of any type
    (1) The 'range[1]' property accepts values of any type

        Returns
        -------
        list
        """
        return self['range']

    @range.setter
    def range(self, val):
        self['range'] = val

    # rangemode
    # ---------
    @property
    def rangemode(self):
        """
        If *normal*, the range is computed in relation to the extrema
        of the input data. If *tozero*`, the range extends to 0,
        regardless of the input data If *nonnegative*, the range is
        non-negative, regardless of the input data.
    
        The 'rangemode' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                ['normal', 'tozero', 'nonnegative']

        Returns
        -------
        Any
        """
        return self['rangemode']

    @rangemode.setter
    def rangemode(self, val):
        self['rangemode'] = val

    # scaleanchor
    # -----------
    @property
    def scaleanchor(self):
        """
        If set to another axis id (e.g. `x2`, `y`), the range of this
        axis changes together with the range of the corresponding axis
        such that the scale of pixels per unit is in a constant ratio.
        Both axes are still zoomable, but when you zoom one, the other
        will zoom the same amount, keeping a fixed midpoint.
        `constrain` and `constraintoward` determine how we enforce the
        constraint. You can chain these, ie `yaxis: {scaleanchor: *x*},
        xaxis2: {scaleanchor: *y*}` but you can only link axes of the
        same `type`. The linked axis can have the opposite letter (to
        constrain the aspect ratio) or the same letter (to match scales
        across subplots). Loops (`yaxis: {scaleanchor: *x*}, xaxis:
        {scaleanchor: *y*}` or longer) are redundant and the last
        constraint encountered will be ignored to avoid possible
        inconsistent constraints via `scaleratio`.
    
        The 'scaleanchor' property is an enumeration that may be specified as:
          - A string that matches one of the following regular expressions:
                ['^x([2-9]|[1-9][0-9]+)?$', '^y([2-9]|[1-9][0-9]+)?$']

        Returns
        -------
        Any
        """
        return self['scaleanchor']

    @scaleanchor.setter
    def scaleanchor(self, val):
        self['scaleanchor'] = val

    # scaleratio
    # ----------
    @property
    def scaleratio(self):
        """
        If this axis is linked to another by `scaleanchor`, this
        determines the pixel to unit scale ratio. For example, if this
        value is 10, then every unit on this axis spans 10 times the
        number of pixels as a unit on the linked axis. Use this for
        example to create an elevation profile where the vertical scale
        is exaggerated a fixed amount with respect to the horizontal.
    
        The 'scaleratio' property is a number and may be specified as:
          - An int or float in the interval [0, inf]

        Returns
        -------
        int|float
        """
        return self['scaleratio']

    @scaleratio.setter
    def scaleratio(self, val):
        self['scaleratio'] = val

    # separatethousands
    # -----------------
    @property
    def separatethousands(self):
        """
        If "true", even 4-digit integers are separated
    
        The 'separatethousands' property must be specified as a bool
        (either True, or False)

        Returns
        -------
        bool
        """
        return self['separatethousands']

    @separatethousands.setter
    def separatethousands(self, val):
        self['separatethousands'] = val

    # showexponent
    # ------------
    @property
    def showexponent(self):
        """
        If *all*, all exponents are shown besides their significands.
        If *first*, only the exponent of the first tick is shown. If
        *last*, only the exponent of the last tick is shown. If *none*,
        no exponents appear.
    
        The 'showexponent' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                ['all', 'first', 'last', 'none']

        Returns
        -------
        Any
        """
        return self['showexponent']

    @showexponent.setter
    def showexponent(self, val):
        self['showexponent'] = val

    # showgrid
    # --------
    @property
    def showgrid(self):
        """
        Determines whether or not grid lines are drawn. If *true*, the
        grid lines are drawn at every tick mark.
    
        The 'showgrid' property must be specified as a bool
        (either True, or False)

        Returns
        -------
        bool
        """
        return self['showgrid']

    @showgrid.setter
    def showgrid(self, val):
        self['showgrid'] = val

    # showline
    # --------
    @property
    def showline(self):
        """
        Determines whether or not a line bounding this axis is drawn.
    
        The 'showline' property must be specified as a bool
        (either True, or False)

        Returns
        -------
        bool
        """
        return self['showline']

    @showline.setter
    def showline(self, val):
        self['showline'] = val

    # showspikes
    # ----------
    @property
    def showspikes(self):
        """
        Determines whether or not spikes (aka droplines) are drawn for
        this axis. Note: This only takes affect when hovermode =
        closest
    
        The 'showspikes' property must be specified as a bool
        (either True, or False)

        Returns
        -------
        bool
        """
        return self['showspikes']

    @showspikes.setter
    def showspikes(self, val):
        self['showspikes'] = val

    # showticklabels
    # --------------
    @property
    def showticklabels(self):
        """
        Determines whether or not the tick labels are drawn.
    
        The 'showticklabels' property must be specified as a bool
        (either True, or False)

        Returns
        -------
        bool
        """
        return self['showticklabels']

    @showticklabels.setter
    def showticklabels(self, val):
        self['showticklabels'] = val

    # showtickprefix
    # --------------
    @property
    def showtickprefix(self):
        """
        If *all*, all tick labels are displayed with a prefix. If
        *first*, only the first tick is displayed with a prefix. If
        *last*, only the last tick is displayed with a suffix. If
        *none*, tick prefixes are hidden.
    
        The 'showtickprefix' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                ['all', 'first', 'last', 'none']

        Returns
        -------
        Any
        """
        return self['showtickprefix']

    @showtickprefix.setter
    def showtickprefix(self, val):
        self['showtickprefix'] = val

    # showticksuffix
    # --------------
    @property
    def showticksuffix(self):
        """
        Same as `showtickprefix` but for tick suffixes.
    
        The 'showticksuffix' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                ['all', 'first', 'last', 'none']

        Returns
        -------
        Any
        """
        return self['showticksuffix']

    @showticksuffix.setter
    def showticksuffix(self, val):
        self['showticksuffix'] = val

    # side
    # ----
    @property
    def side(self):
        """
        Determines whether a x (y) axis is positioned at the *bottom*
        (*left*) or *top* (*right*) of the plotting area.
    
        The 'side' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                ['top', 'bottom', 'left', 'right']

        Returns
        -------
        Any
        """
        return self['side']

    @side.setter
    def side(self, val):
        self['side'] = val

    # spikecolor
    # ----------
    @property
    def spikecolor(self):
        """
        Sets the spike color. If undefined, will use the series color
    
        The 'spikecolor' property is a color and may be specified as:
          - A hex string (e.g. '#ff0000')
          - An rgb/rgba string (e.g. 'rgb(255,0,0)')
          - An hsl/hsla string (e.g. 'hsl(0,100%,50%)')
          - An hsv/hsva string (e.g. 'hsv(0,100%,100%)')
          - A named CSS color:
                aliceblue, antiquewhite, aqua, aquamarine, azure,
                beige, bisque, black, blanchedalmond, blue,
                blueviolet, brown, burlywood, cadetblue,
                chartreuse, chocolate, coral, cornflowerblue,
                cornsilk, crimson, cyan, darkblue, darkcyan,
                darkgoldenrod, darkgray, darkgrey, darkgreen,
                darkkhaki, darkmagenta, darkolivegreen, darkorange,
                darkorchid, darkred, darksalmon, darkseagreen,
                darkslateblue, darkslategray, darkslategrey,
                darkturquoise, darkviolet, deeppink, deepskyblue,
                dimgray, dimgrey, dodgerblue, firebrick,
                floralwhite, forestgreen, fuchsia, gainsboro,
                ghostwhite, gold, goldenrod, gray, grey, green,
                greenyellow, honeydew, hotpink, indianred, indigo,
                ivory, khaki, lavender, lavenderblush, lawngreen,
                lemonchiffon, lightblue, lightcoral, lightcyan,
                lightgoldenrodyellow, lightgray, lightgrey,
                lightgreen, lightpink, lightsalmon, lightseagreen,
                lightskyblue, lightslategray, lightslategrey,
                lightsteelblue, lightyellow, lime, limegreen,
                linen, magenta, maroon, mediumaquamarine,
                mediumblue, mediumorchid, mediumpurple,
                mediumseagreen, mediumslateblue, mediumspringgreen,
                mediumturquoise, mediumvioletred, midnightblue,
                mintcream, mistyrose, moccasin, navajowhite, navy,
                oldlace, olive, olivedrab, orange, orangered,
                orchid, palegoldenrod, palegreen, paleturquoise,
                palevioletred, papayawhip, peachpuff, peru, pink,
                plum, powderblue, purple, red, rosybrown,
                royalblue, saddlebrown, salmon, sandybrown,
                seagreen, seashell, sienna, silver, skyblue,
                slateblue, slategray, slategrey, snow, springgreen,
                steelblue, tan, teal, thistle, tomato, turquoise,
                violet, wheat, white, whitesmoke, yellow,
                yellowgreen

        Returns
        -------
        str
        """
        return self['spikecolor']

    @spikecolor.setter
    def spikecolor(self, val):
        self['spikecolor'] = val

    # spikedash
    # ---------
    @property
    def spikedash(self):
        """
        Sets the dash style of lines. Set to a dash type string
        (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or
        *longdashdot*) or a dash length list in px (eg
        *5px,10px,2px,2px*).
    
        The 'spikedash' property is a string and must be specified as:
          - One of the following strings:
                ['solid', 'dot', 'dash', 'longdash', 'dashdot',
                'longdashdot']
          - A number that will be converted to a string

        Returns
        -------
        str
        """
        return self['spikedash']

    @spikedash.setter
    def spikedash(self, val):
        self['spikedash'] = val

    # spikemode
    # ---------
    @property
    def spikemode(self):
        """
        Determines the drawing mode for the spike line If *toaxis*, the
        line is drawn from the data point to the axis the  series is
        plotted on. If *across*, the line is drawn across the entire
        plot area, and supercedes *toaxis*. If *marker*, then a marker
        dot is drawn on the axis the series is plotted on
    
        The 'spikemode' property is a flaglist and may be specified
        as a string containing:
          - Any combination of ['toaxis', 'across', 'marker'] joined with '+' characters
            (e.g. 'toaxis+across')

        Returns
        -------
        Any
        """
        return self['spikemode']

    @spikemode.setter
    def spikemode(self, val):
        self['spikemode'] = val

    # spikesnap
    # ---------
    @property
    def spikesnap(self):
        """
        Determines whether spikelines are stuck to the cursor or to the
        closest datapoints.
    
        The 'spikesnap' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                ['data', 'cursor']

        Returns
        -------
        Any
        """
        return self['spikesnap']

    @spikesnap.setter
    def spikesnap(self, val):
        self['spikesnap'] = val

    # spikethickness
    # --------------
    @property
    def spikethickness(self):
        """
        Sets the width (in px) of the zero line.
    
        The 'spikethickness' property is a number and may be specified as:
          - An int or float

        Returns
        -------
        int|float
        """
        return self['spikethickness']

    @spikethickness.setter
    def spikethickness(self, val):
        self['spikethickness'] = val

    # tick0
    # -----
    @property
    def tick0(self):
        """
        Sets the placement of the first tick on this axis. Use with
        `dtick`. If the axis `type` is *log*, then you must take the
        log of your starting tick (e.g. to set the starting tick to
        100, set the `tick0` to 2) except when `dtick`=*L<f>* (see
        `dtick` for more info). If the axis `type` is *date*, it should
        be a date string, like date data. If the axis `type` is
        *category*, it should be a number, using the scale where each
        category is assigned a serial number from zero in the order it
        appears.
    
        The 'tick0' property accepts values of any type

        Returns
        -------
        Any
        """
        return self['tick0']

    @tick0.setter
    def tick0(self, val):
        self['tick0'] = val

    # tickangle
    # ---------
    @property
    def tickangle(self):
        """
        Sets the angle of the tick labels with respect to the
        horizontal. For example, a `tickangle` of -90 draws the tick
        labels vertically.
    
        The 'tickangle' property is a angle (in degrees) that may be
        specified as a number between -180 and 180. Numeric values outside this
        range are converted to the equivalent value
        (e.g. 270 is converted to -90).

        Returns
        -------
        int|float
        """
        return self['tickangle']

    @tickangle.setter
    def tickangle(self, val):
        self['tickangle'] = val

    # tickcolor
    # ---------
    @property
    def tickcolor(self):
        """
        Sets the tick color.
    
        The 'tickcolor' property is a color and may be specified as:
          - A hex string (e.g. '#ff0000')
          - An rgb/rgba string (e.g. 'rgb(255,0,0)')
          - An hsl/hsla string (e.g. 'hsl(0,100%,50%)')
          - An hsv/hsva string (e.g. 'hsv(0,100%,100%)')
          - A named CSS color:
                aliceblue, antiquewhite, aqua, aquamarine, azure,
                beige, bisque, black, blanchedalmond, blue,
                blueviolet, brown, burlywood, cadetblue,
                chartreuse, chocolate, coral, cornflowerblue,
                cornsilk, crimson, cyan, darkblue, darkcyan,
                darkgoldenrod, darkgray, darkgrey, darkgreen,
                darkkhaki, darkmagenta, darkolivegreen, darkorange,
                darkorchid, darkred, darksalmon, darkseagreen,
                darkslateblue, darkslategray, darkslategrey,
                darkturquoise, darkviolet, deeppink, deepskyblue,
                dimgray, dimgrey, dodgerblue, firebrick,
                floralwhite, forestgreen, fuchsia, gainsboro,
                ghostwhite, gold, goldenrod, gray, grey, green,
                greenyellow, honeydew, hotpink, indianred, indigo,
                ivory, khaki, lavender, lavenderblush, lawngreen,
                lemonchiffon, lightblue, lightcoral, lightcyan,
                lightgoldenrodyellow, lightgray, lightgrey,
                lightgreen, lightpink, lightsalmon, lightseagreen,
                lightskyblue, lightslategray, lightslategrey,
                lightsteelblue, lightyellow, lime, limegreen,
                linen, magenta, maroon, mediumaquamarine,
                mediumblue, mediumorchid, mediumpurple,
                mediumseagreen, mediumslateblue, mediumspringgreen,
                mediumturquoise, mediumvioletred, midnightblue,
                mintcream, mistyrose, moccasin, navajowhite, navy,
                oldlace, olive, olivedrab, orange, orangered,
                orchid, palegoldenrod, palegreen, paleturquoise,
                palevioletred, papayawhip, peachpuff, peru, pink,
                plum, powderblue, purple, red, rosybrown,
                royalblue, saddlebrown, salmon, sandybrown,
                seagreen, seashell, sienna, silver, skyblue,
                slateblue, slategray, slategrey, snow, springgreen,
                steelblue, tan, teal, thistle, tomato, turquoise,
                violet, wheat, white, whitesmoke, yellow,
                yellowgreen

        Returns
        -------
        str
        """
        return self['tickcolor']

    @tickcolor.setter
    def tickcolor(self, val):
        self['tickcolor'] = val

    # tickfont
    # --------
    @property
    def tickfont(self):
        """
        Sets the tick font.
    
        The 'tickfont' property is an instance of Tickfont
        that may be specified as:
          - An instance of plotly.graph_objs.layout.yaxis.Tickfont
          - A dict of string/value properties that will be passed
            to the Tickfont constructor
    
            Supported dict properties:
                
                color
    
                family
                    HTML font family - the typeface that will be
                    applied by the web browser. The web browser
                    will only be able to apply a font if it is
                    available on the system which it operates.
                    Provide multiple font families, separated by
                    commas, to indicate the preference in which to
                    apply fonts if they aren't available on the
                    system. The plotly service (at https://plot.ly
                    or on-premise) generates images on a server,
                    where only a select number of fonts are
                    installed and supported. These include *Arial*,
                    *Balto*, *Courier New*, *Droid Sans*,, *Droid
                    Serif*, *Droid Sans Mono*, *Gravitas One*, *Old
                    Standard TT*, *Open Sans*, *Overpass*, *PT Sans
                    Narrow*, *Raleway*, *Times New Roman*.
                size

        Returns
        -------
        plotly.graph_objs.layout.yaxis.Tickfont
        """
        return self['tickfont']

    @tickfont.setter
    def tickfont(self, val):
        self['tickfont'] = val

    # tickformat
    # ----------
    @property
    def tickformat(self):
        """
        Sets the tick label formatting rule using d3 formatting mini-
        languages which are very similar to those in Python. For
        numbers, see: https://github.com/d3/d3-format/blob/master/READM
        E.md#locale_format And for dates see:
        https://github.com/d3/d3-time-
        format/blob/master/README.md#locale_format We add one item to
        d3's date formatter: *%{n}f* for fractional seconds with n
        digits. For example, *2016-10-13 09:15:23.456* with tickformat
        *%H~%M~%S.%2f* would display *09~15~23.46*
    
        The 'tickformat' property is a string and must be specified as:
          - A string
          - A number that will be converted to a string

        Returns
        -------
        str
        """
        return self['tickformat']

    @tickformat.setter
    def tickformat(self, val):
        self['tickformat'] = val

    # tickformatstops
    # ---------------
    @property
    def tickformatstops(self):
        """
        The 'tickformatstops' property is a tuple of instances of
        Tickformatstop that may be specified as:
          - A list or tuple of instances of plotly.graph_objs.layout.yaxis.Tickformatstop
          - A list or tuple of dicts of string/value properties that
            will be passed to the Tickformatstop constructor
    
            Supported dict properties:
                
                dtickrange
                    range [*min*, *max*], where *min*, *max* -
                    dtick values which describe some zoom level, it
                    is possible to omit *min* or *max* value by
                    passing *null*
                enabled
                    Determines whether or not this stop is used. If
                    `false`, this stop is ignored even within its
                    `dtickrange`.
                name
                    When used in a template, named items are
                    created in the output figure in addition to any
                    items the figure already has in this array. You
                    can modify these items in the output figure by
                    making your own item with `templateitemname`
                    matching this `name` alongside your
                    modifications (including `visible: false` or
                    `enabled: false` to hide it). Has no effect
                    outside of a template.
                templateitemname
                    Used to refer to a named item in this array in
                    the template. Named items from the template
                    will be created even without a matching item in
                    the input figure, but you can modify one by
                    making an item with `templateitemname` matching
                    its `name`, alongside your modifications
                    (including `visible: false` or `enabled: false`
                    to hide it). If there is no template or no
                    matching item, this item will be hidden unless
                    you explicitly show it with `visible: true`.
                value
                    string - dtickformat for described zoom level,
                    the same as *tickformat*

        Returns
        -------
        tuple[plotly.graph_objs.layout.yaxis.Tickformatstop]
        """
        return self['tickformatstops']

    @tickformatstops.setter
    def tickformatstops(self, val):
        self['tickformatstops'] = val

    # ticklen
    # -------
    @property
    def ticklen(self):
        """
        Sets the tick length (in px).
    
        The 'ticklen' property is a number and may be specified as:
          - An int or float in the interval [0, inf]

        Returns
        -------
        int|float
        """
        return self['ticklen']

    @ticklen.setter
    def ticklen(self, val):
        self['ticklen'] = val

    # tickmode
    # --------
    @property
    def tickmode(self):
        """
        Sets the tick mode for this axis. If *auto*, the number of
        ticks is set via `nticks`. If *linear*, the placement of the
        ticks is determined by a starting position `tick0` and a tick
        step `dtick` (*linear* is the default value if `tick0` and
        `dtick` are provided). If *array*, the placement of the ticks
        is set via `tickvals` and the tick text is `ticktext`. (*array*
        is the default value if `tickvals` is provided).
    
        The 'tickmode' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                ['auto', 'linear', 'array']

        Returns
        -------
        Any
        """
        return self['tickmode']

    @tickmode.setter
    def tickmode(self, val):
        self['tickmode'] = val

    # tickprefix
    # ----------
    @property
    def tickprefix(self):
        """
        Sets a tick label prefix.
    
        The 'tickprefix' property is a string and must be specified as:
          - A string
          - A number that will be converted to a string

        Returns
        -------
        str
        """
        return self['tickprefix']

    @tickprefix.setter
    def tickprefix(self, val):
        self['tickprefix'] = val

    # ticks
    # -----
    @property
    def ticks(self):
        """
        Determines whether ticks are drawn or not. If **, this axis'
        ticks are not drawn. If *outside* (*inside*), this axis' are
        drawn outside (inside) the axis lines.
    
        The 'ticks' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                ['outside', 'inside', '']

        Returns
        -------
        Any
        """
        return self['ticks']

    @ticks.setter
    def ticks(self, val):
        self['ticks'] = val

    # ticksuffix
    # ----------
    @property
    def ticksuffix(self):
        """
        Sets a tick label suffix.
    
        The 'ticksuffix' property is a string and must be specified as:
          - A string
          - A number that will be converted to a string

        Returns
        -------
        str
        """
        return self['ticksuffix']

    @ticksuffix.setter
    def ticksuffix(self, val):
        self['ticksuffix'] = val

    # ticktext
    # --------
    @property
    def ticktext(self):
        """
        Sets the text displayed at the ticks position via `tickvals`.
        Only has an effect if `tickmode` is set to *array*. Used with
        `tickvals`.
    
        The 'ticktext' property is an array that may be specified as a tuple,
        list, numpy array, or pandas Series

        Returns
        -------
        numpy.ndarray
        """
        return self['ticktext']

    @ticktext.setter
    def ticktext(self, val):
        self['ticktext'] = val

    # ticktextsrc
    # -----------
    @property
    def ticktextsrc(self):
        """
        Sets the source reference on plot.ly for  ticktext .
    
        The 'ticktextsrc' property must be specified as a string or
        as a plotly.grid_objs.Column object

        Returns
        -------
        str
        """
        return self['ticktextsrc']

    @ticktextsrc.setter
    def ticktextsrc(self, val):
        self['ticktextsrc'] = val

    # tickvals
    # --------
    @property
    def tickvals(self):
        """
        Sets the values at which ticks on this axis appear. Only has an
        effect if `tickmode` is set to *array*. Used with `ticktext`.
    
        The 'tickvals' property is an array that may be specified as a tuple,
        list, numpy array, or pandas Series

        Returns
        -------
        numpy.ndarray
        """
        return self['tickvals']

    @tickvals.setter
    def tickvals(self, val):
        self['tickvals'] = val

    # tickvalssrc
    # -----------
    @property
    def tickvalssrc(self):
        """
        Sets the source reference on plot.ly for  tickvals .
    
        The 'tickvalssrc' property must be specified as a string or
        as a plotly.grid_objs.Column object

        Returns
        -------
        str
        """
        return self['tickvalssrc']

    @tickvalssrc.setter
    def tickvalssrc(self, val):
        self['tickvalssrc'] = val

    # tickwidth
    # ---------
    @property
    def tickwidth(self):
        """
        Sets the tick width (in px).
    
        The 'tickwidth' property is a number and may be specified as:
          - An int or float in the interval [0, inf]

        Returns
        -------
        int|float
        """
        return self['tickwidth']

    @tickwidth.setter
    def tickwidth(self, val):
        self['tickwidth'] = val

    # title
    # -----
    @property
    def title(self):
        """
        Sets the title of this axis.
    
        The 'title' property is a string and must be specified as:
          - A string
          - A number that will be converted to a string

        Returns
        -------
        str
        """
        return self['title']

    @title.setter
    def title(self, val):
        self['title'] = val

    # titlefont
    # ---------
    @property
    def titlefont(self):
        """
        Sets this axis' title font.
    
        The 'titlefont' property is an instance of Titlefont
        that may be specified as:
          - An instance of plotly.graph_objs.layout.yaxis.Titlefont
          - A dict of string/value properties that will be passed
            to the Titlefont constructor
    
            Supported dict properties:
                
                color
    
                family
                    HTML font family - the typeface that will be
                    applied by the web browser. The web browser
                    will only be able to apply a font if it is
                    available on the system which it operates.
                    Provide multiple font families, separated by
                    commas, to indicate the preference in which to
                    apply fonts if they aren't available on the
                    system. The plotly service (at https://plot.ly
                    or on-premise) generates images on a server,
                    where only a select number of fonts are
                    installed and supported. These include *Arial*,
                    *Balto*, *Courier New*, *Droid Sans*,, *Droid
                    Serif*, *Droid Sans Mono*, *Gravitas One*, *Old
                    Standard TT*, *Open Sans*, *Overpass*, *PT Sans
                    Narrow*, *Raleway*, *Times New Roman*.
                size

        Returns
        -------
        plotly.graph_objs.layout.yaxis.Titlefont
        """
        return self['titlefont']

    @titlefont.setter
    def titlefont(self, val):
        self['titlefont'] = val

    # type
    # ----
    @property
    def type(self):
        """
        Sets the axis type. By default, plotly attempts to determined
        the axis type by looking into the data of the traces that
        referenced the axis in question.
    
        The 'type' property is an enumeration that may be specified as:
          - One of the following enumeration values:
                ['-', 'linear', 'log', 'date', 'category']

        Returns
        -------
        Any
        """
        return self['type']

    @type.setter
    def type(self, val):
        self['type'] = val

    # visible
    # -------
    @property
    def visible(self):
        """
        A single toggle to hide the axis while preserving interaction
        like dragging. Default is true when a cheater plot is present
        on the axis, otherwise false
    
        The 'visible' property must be specified as a bool
        (either True, or False)

        Returns
        -------
        bool
        """
        return self['visible']

    @visible.setter
    def visible(self, val):
        self['visible'] = val

    # zeroline
    # --------
    @property
    def zeroline(self):
        """
        Determines whether or not a line is drawn at along the 0 value
        of this axis. If *true*, the zero line is drawn on top of the
        grid lines.
    
        The 'zeroline' property must be specified as a bool
        (either True, or False)

        Returns
        -------
        bool
        """
        return self['zeroline']

    @zeroline.setter
    def zeroline(self, val):
        self['zeroline'] = val

    # zerolinecolor
    # -------------
    @property
    def zerolinecolor(self):
        """
        Sets the line color of the zero line.
    
        The 'zerolinecolor' property is a color and may be specified as:
          - A hex string (e.g. '#ff0000')
          - An rgb/rgba string (e.g. 'rgb(255,0,0)')
          - An hsl/hsla string (e.g. 'hsl(0,100%,50%)')
          - An hsv/hsva string (e.g. 'hsv(0,100%,100%)')
          - A named CSS color:
                aliceblue, antiquewhite, aqua, aquamarine, azure,
                beige, bisque, black, blanchedalmond, blue,
                blueviolet, brown, burlywood, cadetblue,
                chartreuse, chocolate, coral, cornflowerblue,
                cornsilk, crimson, cyan, darkblue, darkcyan,
                darkgoldenrod, darkgray, darkgrey, darkgreen,
                darkkhaki, darkmagenta, darkolivegreen, darkorange,
                darkorchid, darkred, darksalmon, darkseagreen,
                darkslateblue, darkslategray, darkslategrey,
                darkturquoise, darkviolet, deeppink, deepskyblue,
                dimgray, dimgrey, dodgerblue, firebrick,
                floralwhite, forestgreen, fuchsia, gainsboro,
                ghostwhite, gold, goldenrod, gray, grey, green,
                greenyellow, honeydew, hotpink, indianred, indigo,
                ivory, khaki, lavender, lavenderblush, lawngreen,
                lemonchiffon, lightblue, lightcoral, lightcyan,
                lightgoldenrodyellow, lightgray, lightgrey,
                lightgreen, lightpink, lightsalmon, lightseagreen,
                lightskyblue, lightslategray, lightslategrey,
                lightsteelblue, lightyellow, lime, limegreen,
                linen, magenta, maroon, mediumaquamarine,
                mediumblue, mediumorchid, mediumpurple,
                mediumseagreen, mediumslateblue, mediumspringgreen,
                mediumturquoise, mediumvioletred, midnightblue,
                mintcream, mistyrose, moccasin, navajowhite, navy,
                oldlace, olive, olivedrab, orange, orangered,
                orchid, palegoldenrod, palegreen, paleturquoise,
                palevioletred, papayawhip, peachpuff, peru, pink,
                plum, powderblue, purple, red, rosybrown,
                royalblue, saddlebrown, salmon, sandybrown,
                seagreen, seashell, sienna, silver, skyblue,
                slateblue, slategray, slategrey, snow, springgreen,
                steelblue, tan, teal, thistle, tomato, turquoise,
                violet, wheat, white, whitesmoke, yellow,
                yellowgreen

        Returns
        -------
        str
        """
        return self['zerolinecolor']

    @zerolinecolor.setter
    def zerolinecolor(self, val):
        self['zerolinecolor'] = val

    # zerolinewidth
    # -------------
    @property
    def zerolinewidth(self):
        """
        Sets the width (in px) of the zero line.
    
        The 'zerolinewidth' property is a number and may be specified as:
          - An int or float

        Returns
        -------
        int|float
        """
        return self['zerolinewidth']

    @zerolinewidth.setter
    def zerolinewidth(self, val):
        self['zerolinewidth'] = val

    # property parent name
    # --------------------
    @property
    def _parent_path_str(self):
        return 'layout'

    # Self properties description
    # ---------------------------
    @property
    def _prop_descriptions(self):
        return """\
        anchor
            If set to an opposite-letter axis id (e.g. `x2`, `y`),
            this axis is bound to the corresponding opposite-letter
            axis. If set to *free*, this axis' position is
            determined by `position`.
        automargin
            Determines whether long tick labels automatically grow
            the figure margins.
        autorange
            Determines whether or not the range of this axis is
            computed in relation to the input data. See `rangemode`
            for more info. If `range` is provided, then `autorange`
            is set to *false*.
        calendar
            Sets the calendar system to use for `range` and `tick0`
            if this is a date axis. This does not set the calendar
            for interpreting data on this axis, that's specified in
            the trace or via the global `layout.calendar`
        categoryarray
            Sets the order in which categories on this axis appear.
            Only has an effect if `categoryorder` is set to
            *array*. Used with `categoryorder`.
        categoryarraysrc
            Sets the source reference on plot.ly for  categoryarray
            .
        categoryorder
            Specifies the ordering logic for the case of
            categorical variables. By default, plotly uses *trace*,
            which specifies the order that is present in the data
            supplied. Set `categoryorder` to *category ascending*
            or *category descending* if order should be determined
            by the alphanumerical order of the category names. Set
            `categoryorder` to *array* to derive the ordering from
            the attribute `categoryarray`. If a category is not
            found in the `categoryarray` array, the sorting
            behavior for that attribute will be identical to the
            *trace* mode. The unspecified categories will follow
            the categories in `categoryarray`.
        color
            Sets default for all colors associated with this axis
            all at once: line, font, tick, and grid colors. Grid
            color is lightened by blending this with the plot
            background Individual pieces can override this.
        constrain
            If this axis needs to be compressed (either due to its
            own `scaleanchor` and `scaleratio` or those of the
            other axis), determines how that happens: by increasing
            the *range* (default), or by decreasing the *domain*.
        constraintoward
            If this axis needs to be compressed (either due to its
            own `scaleanchor` and `scaleratio` or those of the
            other axis), determines which direction we push the
            originally specified plot area. Options are *left*,
            *center* (default), and *right* for x axes, and *top*,
            *middle* (default), and *bottom* for y axes.
        domain
            Sets the domain of this axis (in plot fraction).
        dtick
            Sets the step in-between ticks on this axis. Use with
            `tick0`. Must be a positive number, or special strings
            available to *log* and *date* axes. If the axis `type`
            is *log*, then ticks are set every 10^(n*dtick) where n
            is the tick number. For example, to set a tick mark at
            1, 10, 100, 1000, ... set dtick to 1. To set tick marks
            at 1, 100, 10000, ... set dtick to 2. To set tick marks
            at 1, 5, 25, 125, 625, 3125, ... set dtick to
            log_10(5), or 0.69897000433. *log* has several special
            values; *L<f>*, where `f` is a positive number, gives
            ticks linearly spaced in value (but not position). For
            example `tick0` = 0.1, `dtick` = *L0.5* will put ticks
            at 0.1, 0.6, 1.1, 1.6 etc. To show powers of 10 plus
            small digits between, use *D1* (all digits) or *D2*
            (only 2 and 5). `tick0` is ignored for *D1* and *D2*.
            If the axis `type` is *date*, then you must convert the
            time to milliseconds. For example, to set the interval
            between ticks to one day, set `dtick` to 86400000.0.
            *date* also has special values *M<n>* gives ticks
            spaced by a number of months. `n` must be a positive
            integer. To set ticks on the 15th of every third month,
            set `tick0` to *2000-01-15* and `dtick` to *M3*. To set
            ticks every 4 years, set `dtick` to *M48*
        exponentformat
            Determines a formatting rule for the tick exponents.
            For example, consider the number 1,000,000,000. If
            *none*, it appears as 1,000,000,000. If *e*, 1e+9. If
            *E*, 1E+9. If *power*, 1x10^9 (with 9 in a super
            script). If *SI*, 1G. If *B*, 1B.
        fixedrange
            Determines whether or not this axis is zoom-able. If
            true, then zoom is disabled.
        gridcolor
            Sets the color of the grid lines.
        gridwidth
            Sets the width (in px) of the grid lines.
        hoverformat
            Sets the hover text formatting rule using d3 formatting
            mini-languages which are very similar to those in
            Python. For numbers, see: https://github.com/d3/d3-form
            at/blob/master/README.md#locale_format And for dates
            see: https://github.com/d3/d3-time-
            format/blob/master/README.md#locale_format We add one
            item to d3's date formatter: *%{n}f* for fractional
            seconds with n digits. For example, *2016-10-13
            09:15:23.456* with tickformat *%H~%M~%S.%2f* would
            display *09~15~23.46*
        layer
            Sets the layer on which this axis is displayed. If
            *above traces*, this axis is displayed above all the
            subplot's traces If *below traces*, this axis is
            displayed below all the subplot's traces, but above the
            grid lines. Useful when used together with scatter-like
            traces with `cliponaxis` set to *false* to show markers
            and/or text nodes above this axis.
        linecolor
            Sets the axis line color.
        linewidth
            Sets the width (in px) of the axis line.
        mirror
            Determines if the axis lines or/and ticks are mirrored
            to the opposite side of the plotting area. If *true*,
            the axis lines are mirrored. If *ticks*, the axis lines
            and ticks are mirrored. If *false*, mirroring is
            disable. If *all*, axis lines are mirrored on all
            shared-axes subplots. If *allticks*, axis lines and
            ticks are mirrored on all shared-axes subplots.
        nticks
            Specifies the maximum number of ticks for the
            particular axis. The actual number of ticks will be
            chosen automatically to be less than or equal to
            `nticks`. Has an effect only if `tickmode` is set to
            *auto*.
        overlaying
            If set a same-letter axis id, this axis is overlaid on
            top of the corresponding same-letter axis. If *false*,
            this axis does not overlay any same-letter axes.
        position
            Sets the position of this axis in the plotting space
            (in normalized coordinates). Only has an effect if
            `anchor` is set to *free*.
        range
            Sets the range of this axis. If the axis `type` is
            *log*, then you must take the log of your desired range
            (e.g. to set the range from 1 to 100, set the range
            from 0 to 2). If the axis `type` is *date*, it should
            be date strings, like date data, though Date objects
            and unix milliseconds will be accepted and converted to
            strings. If the axis `type` is *category*, it should be
            numbers, using the scale where each category is
            assigned a serial number from zero in the order it
            appears.
        rangemode
            If *normal*, the range is computed in relation to the
            extrema of the input data. If *tozero*`, the range
            extends to 0, regardless of the input data If
            *nonnegative*, the range is non-negative, regardless of
            the input data.
        scaleanchor
            If set to another axis id (e.g. `x2`, `y`), the range
            of this axis changes together with the range of the
            corresponding axis such that the scale of pixels per
            unit is in a constant ratio. Both axes are still
            zoomable, but when you zoom one, the other will zoom
            the same amount, keeping a fixed midpoint. `constrain`
            and `constraintoward` determine how we enforce the
            constraint. You can chain these, ie `yaxis:
            {scaleanchor: *x*}, xaxis2: {scaleanchor: *y*}` but you
            can only link axes of the same `type`. The linked axis
            can have the opposite letter (to constrain the aspect
            ratio) or the same letter (to match scales across
            subplots). Loops (`yaxis: {scaleanchor: *x*}, xaxis:
            {scaleanchor: *y*}` or longer) are redundant and the
            last constraint encountered will be ignored to avoid
            possible inconsistent constraints via `scaleratio`.
        scaleratio
            If this axis is linked to another by `scaleanchor`,
            this determines the pixel to unit scale ratio. For
            example, if this value is 10, then every unit on this
            axis spans 10 times the number of pixels as a unit on
            the linked axis. Use this for example to create an
            elevation profile where the vertical scale is
            exaggerated a fixed amount with respect to the
            horizontal.
        separatethousands
            If "true", even 4-digit integers are separated
        showexponent
            If *all*, all exponents are shown besides their
            significands. If *first*, only the exponent of the
            first tick is shown. If *last*, only the exponent of
            the last tick is shown. If *none*, no exponents appear.
        showgrid
            Determines whether or not grid lines are drawn. If
            *true*, the grid lines are drawn at every tick mark.
        showline
            Determines whether or not a line bounding this axis is
            drawn.
        showspikes
            Determines whether or not spikes (aka droplines) are
            drawn for this axis. Note: This only takes affect when
            hovermode = closest
        showticklabels
            Determines whether or not the tick labels are drawn.
        showtickprefix
            If *all*, all tick labels are displayed with a prefix.
            If *first*, only the first tick is displayed with a
            prefix. If *last*, only the last tick is displayed with
            a suffix. If *none*, tick prefixes are hidden.
        showticksuffix
            Same as `showtickprefix` but for tick suffixes.
        side
            Determines whether a x (y) axis is positioned at the
            *bottom* (*left*) or *top* (*right*) of the plotting
            area.
        spikecolor
            Sets the spike color. If undefined, will use the series
            color
        spikedash
            Sets the dash style of lines. Set to a dash type string
            (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or
            *longdashdot*) or a dash length list in px (eg
            *5px,10px,2px,2px*).
        spikemode
            Determines the drawing mode for the spike line If
            *toaxis*, the line is drawn from the data point to the
            axis the  series is plotted on. If *across*, the line
            is drawn across the entire plot area, and supercedes
            *toaxis*. If *marker*, then a marker dot is drawn on
            the axis the series is plotted on
        spikesnap
            Determines whether spikelines are stuck to the cursor
            or to the closest datapoints.
        spikethickness
            Sets the width (in px) of the zero line.
        tick0
            Sets the placement of the first tick on this axis. Use
            with `dtick`. If the axis `type` is *log*, then you
            must take the log of your starting tick (e.g. to set
            the starting tick to 100, set the `tick0` to 2) except
            when `dtick`=*L<f>* (see `dtick` for more info). If the
            axis `type` is *date*, it should be a date string, like
            date data. If the axis `type` is *category*, it should
            be a number, using the scale where each category is
            assigned a serial number from zero in the order it
            appears.
        tickangle
            Sets the angle of the tick labels with respect to the
            horizontal. For example, a `tickangle` of -90 draws the
            tick labels vertically.
        tickcolor
            Sets the tick color.
        tickfont
            Sets the tick font.
        tickformat
            Sets the tick label formatting rule using d3 formatting
            mini-languages which are very similar to those in
            Python. For numbers, see: https://github.com/d3/d3-form
            at/blob/master/README.md#locale_format And for dates
            see: https://github.com/d3/d3-time-
            format/blob/master/README.md#locale_format We add one
            item to d3's date formatter: *%{n}f* for fractional
            seconds with n digits. For example, *2016-10-13
            09:15:23.456* with tickformat *%H~%M~%S.%2f* would
            display *09~15~23.46*
        tickformatstops
            plotly.graph_objs.layout.yaxis.Tickformatstop instance
            or dict with compatible properties
        ticklen
            Sets the tick length (in px).
        tickmode
            Sets the tick mode for this axis. If *auto*, the number
            of ticks is set via `nticks`. If *linear*, the
            placement of the ticks is determined by a starting
            position `tick0` and a tick step `dtick` (*linear* is
            the default value if `tick0` and `dtick` are provided).
            If *array*, the placement of the ticks is set via
            `tickvals` and the tick text is `ticktext`. (*array* is
            the default value if `tickvals` is provided).
        tickprefix
            Sets a tick label prefix.
        ticks
            Determines whether ticks are drawn or not. If **, this
            axis' ticks are not drawn. If *outside* (*inside*),
            this axis' are drawn outside (inside) the axis lines.
        ticksuffix
            Sets a tick label suffix.
        ticktext
            Sets the text displayed at the ticks position via
            `tickvals`. Only has an effect if `tickmode` is set to
            *array*. Used with `tickvals`.
        ticktextsrc
            Sets the source reference on plot.ly for  ticktext .
        tickvals
            Sets the values at which ticks on this axis appear.
            Only has an effect if `tickmode` is set to *array*.
            Used with `ticktext`.
        tickvalssrc
            Sets the source reference on plot.ly for  tickvals .
        tickwidth
            Sets the tick width (in px).
        title
            Sets the title of this axis.
        titlefont
            Sets this axis' title font.
        type
            Sets the axis type. By default, plotly attempts to
            determined the axis type by looking into the data of
            the traces that referenced the axis in question.
        visible
            A single toggle to hide the axis while preserving
            interaction like dragging. Default is true when a
            cheater plot is present on the axis, otherwise false
        zeroline
            Determines whether or not a line is drawn at along the
            0 value of this axis. If *true*, the zero line is drawn
            on top of the grid lines.
        zerolinecolor
            Sets the line color of the zero line.
        zerolinewidth
            Sets the width (in px) of the zero line.
        """

    def __init__(
        self,
        arg=None,
        anchor=None,
        automargin=None,
        autorange=None,
        calendar=None,
        categoryarray=None,
        categoryarraysrc=None,
        categoryorder=None,
        color=None,
        constrain=None,
        constraintoward=None,
        domain=None,
        dtick=None,
        exponentformat=None,
        fixedrange=None,
        gridcolor=None,
        gridwidth=None,
        hoverformat=None,
        layer=None,
        linecolor=None,
        linewidth=None,
        mirror=None,
        nticks=None,
        overlaying=None,
        position=None,
        range=None,
        rangemode=None,
        scaleanchor=None,
        scaleratio=None,
        separatethousands=None,
        showexponent=None,
        showgrid=None,
        showline=None,
        showspikes=None,
        showticklabels=None,
        showtickprefix=None,
        showticksuffix=None,
        side=None,
        spikecolor=None,
        spikedash=None,
        spikemode=None,
        spikesnap=None,
        spikethickness=None,
        tick0=None,
        tickangle=None,
        tickcolor=None,
        tickfont=None,
        tickformat=None,
        tickformatstops=None,
        ticklen=None,
        tickmode=None,
        tickprefix=None,
        ticks=None,
        ticksuffix=None,
        ticktext=None,
        ticktextsrc=None,
        tickvals=None,
        tickvalssrc=None,
        tickwidth=None,
        title=None,
        titlefont=None,
        type=None,
        visible=None,
        zeroline=None,
        zerolinecolor=None,
        zerolinewidth=None,
        **kwargs
    ):
        """
        Construct a new YAxis object
        
        Parameters
        ----------
        arg
            dict of properties compatible with this constructor or
            an instance of plotly.graph_objs.layout.YAxis
        anchor
            If set to an opposite-letter axis id (e.g. `x2`, `y`),
            this axis is bound to the corresponding opposite-letter
            axis. If set to *free*, this axis' position is
            determined by `position`.
        automargin
            Determines whether long tick labels automatically grow
            the figure margins.
        autorange
            Determines whether or not the range of this axis is
            computed in relation to the input data. See `rangemode`
            for more info. If `range` is provided, then `autorange`
            is set to *false*.
        calendar
            Sets the calendar system to use for `range` and `tick0`
            if this is a date axis. This does not set the calendar
            for interpreting data on this axis, that's specified in
            the trace or via the global `layout.calendar`
        categoryarray
            Sets the order in which categories on this axis appear.
            Only has an effect if `categoryorder` is set to
            *array*. Used with `categoryorder`.
        categoryarraysrc
            Sets the source reference on plot.ly for  categoryarray
            .
        categoryorder
            Specifies the ordering logic for the case of
            categorical variables. By default, plotly uses *trace*,
            which specifies the order that is present in the data
            supplied. Set `categoryorder` to *category ascending*
            or *category descending* if order should be determined
            by the alphanumerical order of the category names. Set
            `categoryorder` to *array* to derive the ordering from
            the attribute `categoryarray`. If a category is not
            found in the `categoryarray` array, the sorting
            behavior for that attribute will be identical to the
            *trace* mode. The unspecified categories will follow
            the categories in `categoryarray`.
        color
            Sets default for all colors associated with this axis
            all at once: line, font, tick, and grid colors. Grid
            color is lightened by blending this with the plot
            background Individual pieces can override this.
        constrain
            If this axis needs to be compressed (either due to its
            own `scaleanchor` and `scaleratio` or those of the
            other axis), determines how that happens: by increasing
            the *range* (default), or by decreasing the *domain*.
        constraintoward
            If this axis needs to be compressed (either due to its
            own `scaleanchor` and `scaleratio` or those of the
            other axis), determines which direction we push the
            originally specified plot area. Options are *left*,
            *center* (default), and *right* for x axes, and *top*,
            *middle* (default), and *bottom* for y axes.
        domain
            Sets the domain of this axis (in plot fraction).
        dtick
            Sets the step in-between ticks on this axis. Use with
            `tick0`. Must be a positive number, or special strings
            available to *log* and *date* axes. If the axis `type`
            is *log*, then ticks are set every 10^(n*dtick) where n
            is the tick number. For example, to set a tick mark at
            1, 10, 100, 1000, ... set dtick to 1. To set tick marks
            at 1, 100, 10000, ... set dtick to 2. To set tick marks
            at 1, 5, 25, 125, 625, 3125, ... set dtick to
            log_10(5), or 0.69897000433. *log* has several special
            values; *L<f>*, where `f` is a positive number, gives
            ticks linearly spaced in value (but not position). For
            example `tick0` = 0.1, `dtick` = *L0.5* will put ticks
            at 0.1, 0.6, 1.1, 1.6 etc. To show powers of 10 plus
            small digits between, use *D1* (all digits) or *D2*
            (only 2 and 5). `tick0` is ignored for *D1* and *D2*.
            If the axis `type` is *date*, then you must convert the
            time to milliseconds. For example, to set the interval
            between ticks to one day, set `dtick` to 86400000.0.
            *date* also has special values *M<n>* gives ticks
            spaced by a number of months. `n` must be a positive
            integer. To set ticks on the 15th of every third month,
            set `tick0` to *2000-01-15* and `dtick` to *M3*. To set
            ticks every 4 years, set `dtick` to *M48*
        exponentformat
            Determines a formatting rule for the tick exponents.
            For example, consider the number 1,000,000,000. If
            *none*, it appears as 1,000,000,000. If *e*, 1e+9. If
            *E*, 1E+9. If *power*, 1x10^9 (with 9 in a super
            script). If *SI*, 1G. If *B*, 1B.
        fixedrange
            Determines whether or not this axis is zoom-able. If
            true, then zoom is disabled.
        gridcolor
            Sets the color of the grid lines.
        gridwidth
            Sets the width (in px) of the grid lines.
        hoverformat
            Sets the hover text formatting rule using d3 formatting
            mini-languages which are very similar to those in
            Python. For numbers, see: https://github.com/d3/d3-form
            at/blob/master/README.md#locale_format And for dates
            see: https://github.com/d3/d3-time-
            format/blob/master/README.md#locale_format We add one
            item to d3's date formatter: *%{n}f* for fractional
            seconds with n digits. For example, *2016-10-13
            09:15:23.456* with tickformat *%H~%M~%S.%2f* would
            display *09~15~23.46*
        layer
            Sets the layer on which this axis is displayed. If
            *above traces*, this axis is displayed above all the
            subplot's traces If *below traces*, this axis is
            displayed below all the subplot's traces, but above the
            grid lines. Useful when used together with scatter-like
            traces with `cliponaxis` set to *false* to show markers
            and/or text nodes above this axis.
        linecolor
            Sets the axis line color.
        linewidth
            Sets the width (in px) of the axis line.
        mirror
            Determines if the axis lines or/and ticks are mirrored
            to the opposite side of the plotting area. If *true*,
            the axis lines are mirrored. If *ticks*, the axis lines
            and ticks are mirrored. If *false*, mirroring is
            disable. If *all*, axis lines are mirrored on all
            shared-axes subplots. If *allticks*, axis lines and
            ticks are mirrored on all shared-axes subplots.
        nticks
            Specifies the maximum number of ticks for the
            particular axis. The actual number of ticks will be
            chosen automatically to be less than or equal to
            `nticks`. Has an effect only if `tickmode` is set to
            *auto*.
        overlaying
            If set a same-letter axis id, this axis is overlaid on
            top of the corresponding same-letter axis. If *false*,
            this axis does not overlay any same-letter axes.
        position
            Sets the position of this axis in the plotting space
            (in normalized coordinates). Only has an effect if
            `anchor` is set to *free*.
        range
            Sets the range of this axis. If the axis `type` is
            *log*, then you must take the log of your desired range
            (e.g. to set the range from 1 to 100, set the range
            from 0 to 2). If the axis `type` is *date*, it should
            be date strings, like date data, though Date objects
            and unix milliseconds will be accepted and converted to
            strings. If the axis `type` is *category*, it should be
            numbers, using the scale where each category is
            assigned a serial number from zero in the order it
            appears.
        rangemode
            If *normal*, the range is computed in relation to the
            extrema of the input data. If *tozero*`, the range
            extends to 0, regardless of the input data If
            *nonnegative*, the range is non-negative, regardless of
            the input data.
        scaleanchor
            If set to another axis id (e.g. `x2`, `y`), the range
            of this axis changes together with the range of the
            corresponding axis such that the scale of pixels per
            unit is in a constant ratio. Both axes are still
            zoomable, but when you zoom one, the other will zoom
            the same amount, keeping a fixed midpoint. `constrain`
            and `constraintoward` determine how we enforce the
            constraint. You can chain these, ie `yaxis:
            {scaleanchor: *x*}, xaxis2: {scaleanchor: *y*}` but you
            can only link axes of the same `type`. The linked axis
            can have the opposite letter (to constrain the aspect
            ratio) or the same letter (to match scales across
            subplots). Loops (`yaxis: {scaleanchor: *x*}, xaxis:
            {scaleanchor: *y*}` or longer) are redundant and the
            last constraint encountered will be ignored to avoid
            possible inconsistent constraints via `scaleratio`.
        scaleratio
            If this axis is linked to another by `scaleanchor`,
            this determines the pixel to unit scale ratio. For
            example, if this value is 10, then every unit on this
            axis spans 10 times the number of pixels as a unit on
            the linked axis. Use this for example to create an
            elevation profile where the vertical scale is
            exaggerated a fixed amount with respect to the
            horizontal.
        separatethousands
            If "true", even 4-digit integers are separated
        showexponent
            If *all*, all exponents are shown besides their
            significands. If *first*, only the exponent of the
            first tick is shown. If *last*, only the exponent of
            the last tick is shown. If *none*, no exponents appear.
        showgrid
            Determines whether or not grid lines are drawn. If
            *true*, the grid lines are drawn at every tick mark.
        showline
            Determines whether or not a line bounding this axis is
            drawn.
        showspikes
            Determines whether or not spikes (aka droplines) are
            drawn for this axis. Note: This only takes affect when
            hovermode = closest
        showticklabels
            Determines whether or not the tick labels are drawn.
        showtickprefix
            If *all*, all tick labels are displayed with a prefix.
            If *first*, only the first tick is displayed with a
            prefix. If *last*, only the last tick is displayed with
            a suffix. If *none*, tick prefixes are hidden.
        showticksuffix
            Same as `showtickprefix` but for tick suffixes.
        side
            Determines whether a x (y) axis is positioned at the
            *bottom* (*left*) or *top* (*right*) of the plotting
            area.
        spikecolor
            Sets the spike color. If undefined, will use the series
            color
        spikedash
            Sets the dash style of lines. Set to a dash type string
            (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or
            *longdashdot*) or a dash length list in px (eg
            *5px,10px,2px,2px*).
        spikemode
            Determines the drawing mode for the spike line If
            *toaxis*, the line is drawn from the data point to the
            axis the  series is plotted on. If *across*, the line
            is drawn across the entire plot area, and supercedes
            *toaxis*. If *marker*, then a marker dot is drawn on
            the axis the series is plotted on
        spikesnap
            Determines whether spikelines are stuck to the cursor
            or to the closest datapoints.
        spikethickness
            Sets the width (in px) of the zero line.
        tick0
            Sets the placement of the first tick on this axis. Use
            with `dtick`. If the axis `type` is *log*, then you
            must take the log of your starting tick (e.g. to set
            the starting tick to 100, set the `tick0` to 2) except
            when `dtick`=*L<f>* (see `dtick` for more info). If the
            axis `type` is *date*, it should be a date string, like
            date data. If the axis `type` is *category*, it should
            be a number, using the scale where each category is
            assigned a serial number from zero in the order it
            appears.
        tickangle
            Sets the angle of the tick labels with respect to the
            horizontal. For example, a `tickangle` of -90 draws the
            tick labels vertically.
        tickcolor
            Sets the tick color.
        tickfont
            Sets the tick font.
        tickformat
            Sets the tick label formatting rule using d3 formatting
            mini-languages which are very similar to those in
            Python. For numbers, see: https://github.com/d3/d3-form
            at/blob/master/README.md#locale_format And for dates
            see: https://github.com/d3/d3-time-
            format/blob/master/README.md#locale_format We add one
            item to d3's date formatter: *%{n}f* for fractional
            seconds with n digits. For example, *2016-10-13
            09:15:23.456* with tickformat *%H~%M~%S.%2f* would
            display *09~15~23.46*
        tickformatstops
            plotly.graph_objs.layout.yaxis.Tickformatstop instance
            or dict with compatible properties
        ticklen
            Sets the tick length (in px).
        tickmode
            Sets the tick mode for this axis. If *auto*, the number
            of ticks is set via `nticks`. If *linear*, the
            placement of the ticks is determined by a starting
            position `tick0` and a tick step `dtick` (*linear* is
            the default value if `tick0` and `dtick` are provided).
            If *array*, the placement of the ticks is set via
            `tickvals` and the tick text is `ticktext`. (*array* is
            the default value if `tickvals` is provided).
        tickprefix
            Sets a tick label prefix.
        ticks
            Determines whether ticks are drawn or not. If **, this
            axis' ticks are not drawn. If *outside* (*inside*),
            this axis' are drawn outside (inside) the axis lines.
        ticksuffix
            Sets a tick label suffix.
        ticktext
            Sets the text displayed at the ticks position via
            `tickvals`. Only has an effect if `tickmode` is set to
            *array*. Used with `tickvals`.
        ticktextsrc
            Sets the source reference on plot.ly for  ticktext .
        tickvals
            Sets the values at which ticks on this axis appear.
            Only has an effect if `tickmode` is set to *array*.
            Used with `ticktext`.
        tickvalssrc
            Sets the source reference on plot.ly for  tickvals .
        tickwidth
            Sets the tick width (in px).
        title
            Sets the title of this axis.
        titlefont
            Sets this axis' title font.
        type
            Sets the axis type. By default, plotly attempts to
            determined the axis type by looking into the data of
            the traces that referenced the axis in question.
        visible
            A single toggle to hide the axis while preserving
            interaction like dragging. Default is true when a
            cheater plot is present on the axis, otherwise false
        zeroline
            Determines whether or not a line is drawn at along the
            0 value of this axis. If *true*, the zero line is drawn
            on top of the grid lines.
        zerolinecolor
            Sets the line color of the zero line.
        zerolinewidth
            Sets the width (in px) of the zero line.

        Returns
        -------
        YAxis
        """
        super(YAxis, self).__init__('yaxis')

        # Validate arg
        # ------------
        if arg is None:
            arg = {}
        elif isinstance(arg, self.__class__):
            arg = arg.to_plotly_json()
        elif isinstance(arg, dict):
            arg = copy.copy(arg)
        else:
            raise ValueError(
                """\
The first argument to the plotly.graph_objs.layout.YAxis 
constructor must be a dict or 
an instance of plotly.graph_objs.layout.YAxis"""
            )

        # Import validators
        # -----------------
        from plotly.validators.layout import (yaxis as v_yaxis)

        # Initialize validators
        # ---------------------
        self._validators['anchor'] = v_yaxis.AnchorValidator()
        self._validators['automargin'] = v_yaxis.AutomarginValidator()
        self._validators['autorange'] = v_yaxis.AutorangeValidator()
        self._validators['calendar'] = v_yaxis.CalendarValidator()
        self._validators['categoryarray'] = v_yaxis.CategoryarrayValidator()
        self._validators['categoryarraysrc'
                        ] = v_yaxis.CategoryarraysrcValidator()
        self._validators['categoryorder'] = v_yaxis.CategoryorderValidator()
        self._validators['color'] = v_yaxis.ColorValidator()
        self._validators['constrain'] = v_yaxis.ConstrainValidator()
        self._validators['constraintoward'
                        ] = v_yaxis.ConstraintowardValidator()
        self._validators['domain'] = v_yaxis.DomainValidator()
        self._validators['dtick'] = v_yaxis.DtickValidator()
        self._validators['exponentformat'] = v_yaxis.ExponentformatValidator()
        self._validators['fixedrange'] = v_yaxis.FixedrangeValidator()
        self._validators['gridcolor'] = v_yaxis.GridcolorValidator()
        self._validators['gridwidth'] = v_yaxis.GridwidthValidator()
        self._validators['hoverformat'] = v_yaxis.HoverformatValidator()
        self._validators['layer'] = v_yaxis.LayerValidator()
        self._validators['linecolor'] = v_yaxis.LinecolorValidator()
        self._validators['linewidth'] = v_yaxis.LinewidthValidator()
        self._validators['mirror'] = v_yaxis.MirrorValidator()
        self._validators['nticks'] = v_yaxis.NticksValidator()
        self._validators['overlaying'] = v_yaxis.OverlayingValidator()
        self._validators['position'] = v_yaxis.PositionValidator()
        self._validators['range'] = v_yaxis.RangeValidator()
        self._validators['rangemode'] = v_yaxis.RangemodeValidator()
        self._validators['scaleanchor'] = v_yaxis.ScaleanchorValidator()
        self._validators['scaleratio'] = v_yaxis.ScaleratioValidator()
        self._validators['separatethousands'
                        ] = v_yaxis.SeparatethousandsValidator()
        self._validators['showexponent'] = v_yaxis.ShowexponentValidator()
        self._validators['showgrid'] = v_yaxis.ShowgridValidator()
        self._validators['showline'] = v_yaxis.ShowlineValidator()
        self._validators['showspikes'] = v_yaxis.ShowspikesValidator()
        self._validators['showticklabels'] = v_yaxis.ShowticklabelsValidator()
        self._validators['showtickprefix'] = v_yaxis.ShowtickprefixValidator()
        self._validators['showticksuffix'] = v_yaxis.ShowticksuffixValidator()
        self._validators['side'] = v_yaxis.SideValidator()
        self._validators['spikecolor'] = v_yaxis.SpikecolorValidator()
        self._validators['spikedash'] = v_yaxis.SpikedashValidator()
        self._validators['spikemode'] = v_yaxis.SpikemodeValidator()
        self._validators['spikesnap'] = v_yaxis.SpikesnapValidator()
        self._validators['spikethickness'] = v_yaxis.SpikethicknessValidator()
        self._validators['tick0'] = v_yaxis.Tick0Validator()
        self._validators['tickangle'] = v_yaxis.TickangleValidator()
        self._validators['tickcolor'] = v_yaxis.TickcolorValidator()
        self._validators['tickfont'] = v_yaxis.TickfontValidator()
        self._validators['tickformat'] = v_yaxis.TickformatValidator()
        self._validators['tickformatstops'
                        ] = v_yaxis.TickformatstopsValidator()
        self._validators['ticklen'] = v_yaxis.TicklenValidator()
        self._validators['tickmode'] = v_yaxis.TickmodeValidator()
        self._validators['tickprefix'] = v_yaxis.TickprefixValidator()
        self._validators['ticks'] = v_yaxis.TicksValidator()
        self._validators['ticksuffix'] = v_yaxis.TicksuffixValidator()
        self._validators['ticktext'] = v_yaxis.TicktextValidator()
        self._validators['ticktextsrc'] = v_yaxis.TicktextsrcValidator()
        self._validators['tickvals'] = v_yaxis.TickvalsValidator()
        self._validators['tickvalssrc'] = v_yaxis.TickvalssrcValidator()
        self._validators['tickwidth'] = v_yaxis.TickwidthValidator()
        self._validators['title'] = v_yaxis.TitleValidator()
        self._validators['titlefont'] = v_yaxis.TitlefontValidator()
        self._validators['type'] = v_yaxis.TypeValidator()
        self._validators['visible'] = v_yaxis.VisibleValidator()
        self._validators['zeroline'] = v_yaxis.ZerolineValidator()
        self._validators['zerolinecolor'] = v_yaxis.ZerolinecolorValidator()
        self._validators['zerolinewidth'] = v_yaxis.ZerolinewidthValidator()

        # Populate data dict with properties
        # ----------------------------------
        _v = arg.pop('anchor', None)
        self.anchor = anchor if anchor is not None else _v
        _v = arg.pop('automargin', None)
        self.automargin = automargin if automargin is not None else _v
        _v = arg.pop('autorange', None)
        self.autorange = autorange if autorange is not None else _v
        _v = arg.pop('calendar', None)
        self.calendar = calendar if calendar is not None else _v
        _v = arg.pop('categoryarray', None)
        self.categoryarray = categoryarray if categoryarray is not None else _v
        _v = arg.pop('categoryarraysrc', None)
        self.categoryarraysrc = categoryarraysrc if categoryarraysrc is not None else _v
        _v = arg.pop('categoryorder', None)
        self.categoryorder = categoryorder if categoryorder is not None else _v
        _v = arg.pop('color', None)
        self.color = color if color is not None else _v
        _v = arg.pop('constrain', None)
        self.constrain = constrain if constrain is not None else _v
        _v = arg.pop('constraintoward', None)
        self.constraintoward = constraintoward if constraintoward is not None else _v
        _v = arg.pop('domain', None)
        self.domain = domain if domain is not None else _v
        _v = arg.pop('dtick', None)
        self.dtick = dtick if dtick is not None else _v
        _v = arg.pop('exponentformat', None)
        self.exponentformat = exponentformat if exponentformat is not None else _v
        _v = arg.pop('fixedrange', None)
        self.fixedrange = fixedrange if fixedrange is not None else _v
        _v = arg.pop('gridcolor', None)
        self.gridcolor = gridcolor if gridcolor is not None else _v
        _v = arg.pop('gridwidth', None)
        self.gridwidth = gridwidth if gridwidth is not None else _v
        _v = arg.pop('hoverformat', None)
        self.hoverformat = hoverformat if hoverformat is not None else _v
        _v = arg.pop('layer', None)
        self.layer = layer if layer is not None else _v
        _v = arg.pop('linecolor', None)
        self.linecolor = linecolor if linecolor is not None else _v
        _v = arg.pop('linewidth', None)
        self.linewidth = linewidth if linewidth is not None else _v
        _v = arg.pop('mirror', None)
        self.mirror = mirror if mirror is not None else _v
        _v = arg.pop('nticks', None)
        self.nticks = nticks if nticks is not None else _v
        _v = arg.pop('overlaying', None)
        self.overlaying = overlaying if overlaying is not None else _v
        _v = arg.pop('position', None)
        self.position = position if position is not None else _v
        _v = arg.pop('range', None)
        self.range = range if range is not None else _v
        _v = arg.pop('rangemode', None)
        self.rangemode = rangemode if rangemode is not None else _v
        _v = arg.pop('scaleanchor', None)
        self.scaleanchor = scaleanchor if scaleanchor is not None else _v
        _v = arg.pop('scaleratio', None)
        self.scaleratio = scaleratio if scaleratio is not None else _v
        _v = arg.pop('separatethousands', None)
        self.separatethousands = separatethousands if separatethousands is not None else _v
        _v = arg.pop('showexponent', None)
        self.showexponent = showexponent if showexponent is not None else _v
        _v = arg.pop('showgrid', None)
        self.showgrid = showgrid if showgrid is not None else _v
        _v = arg.pop('showline', None)
        self.showline = showline if showline is not None else _v
        _v = arg.pop('showspikes', None)
        self.showspikes = showspikes if showspikes is not None else _v
        _v = arg.pop('showticklabels', None)
        self.showticklabels = showticklabels if showticklabels is not None else _v
        _v = arg.pop('showtickprefix', None)
        self.showtickprefix = showtickprefix if showtickprefix is not None else _v
        _v = arg.pop('showticksuffix', None)
        self.showticksuffix = showticksuffix if showticksuffix is not None else _v
        _v = arg.pop('side', None)
        self.side = side if side is not None else _v
        _v = arg.pop('spikecolor', None)
        self.spikecolor = spikecolor if spikecolor is not None else _v
        _v = arg.pop('spikedash', None)
        self.spikedash = spikedash if spikedash is not None else _v
        _v = arg.pop('spikemode', None)
        self.spikemode = spikemode if spikemode is not None else _v
        _v = arg.pop('spikesnap', None)
        self.spikesnap = spikesnap if spikesnap is not None else _v
        _v = arg.pop('spikethickness', None)
        self.spikethickness = spikethickness if spikethickness is not None else _v
        _v = arg.pop('tick0', None)
        self.tick0 = tick0 if tick0 is not None else _v
        _v = arg.pop('tickangle', None)
        self.tickangle = tickangle if tickangle is not None else _v
        _v = arg.pop('tickcolor', None)
        self.tickcolor = tickcolor if tickcolor is not None else _v
        _v = arg.pop('tickfont', None)
        self.tickfont = tickfont if tickfont is not None else _v
        _v = arg.pop('tickformat', None)
        self.tickformat = tickformat if tickformat is not None else _v
        _v = arg.pop('tickformatstops', None)
        self.tickformatstops = tickformatstops if tickformatstops is not None else _v
        _v = arg.pop('ticklen', None)
        self.ticklen = ticklen if ticklen is not None else _v
        _v = arg.pop('tickmode', None)
        self.tickmode = tickmode if tickmode is not None else _v
        _v = arg.pop('tickprefix', None)
        self.tickprefix = tickprefix if tickprefix is not None else _v
        _v = arg.pop('ticks', None)
        self.ticks = ticks if ticks is not None else _v
        _v = arg.pop('ticksuffix', None)
        self.ticksuffix = ticksuffix if ticksuffix is not None else _v
        _v = arg.pop('ticktext', None)
        self.ticktext = ticktext if ticktext is not None else _v
        _v = arg.pop('ticktextsrc', None)
        self.ticktextsrc = ticktextsrc if ticktextsrc is not None else _v
        _v = arg.pop('tickvals', None)
        self.tickvals = tickvals if tickvals is not None else _v
        _v = arg.pop('tickvalssrc', None)
        self.tickvalssrc = tickvalssrc if tickvalssrc is not None else _v
        _v = arg.pop('tickwidth', None)
        self.tickwidth = tickwidth if tickwidth is not None else _v
        _v = arg.pop('title', None)
        self.title = title if title is not None else _v
        _v = arg.pop('titlefont', None)
        self.titlefont = titlefont if titlefont is not None else _v
        _v = arg.pop('type', None)
        self.type = type if type is not None else _v
        _v = arg.pop('visible', None)
        self.visible = visible if visible is not None else _v
        _v = arg.pop('zeroline', None)
        self.zeroline = zeroline if zeroline is not None else _v
        _v = arg.pop('zerolinecolor', None)
        self.zerolinecolor = zerolinecolor if zerolinecolor is not None else _v
        _v = arg.pop('zerolinewidth', None)
        self.zerolinewidth = zerolinewidth if zerolinewidth is not None else _v

        # Process unknown kwargs
        # ----------------------
        self._process_kwargs(**dict(arg, **kwargs))
