from plotly.basedatatypes import BaseLayoutHierarchyType
import copy


class Rangeslider(BaseLayoutHierarchyType):

    # autorange
    # ---------
    @property
    def autorange(self):
        """
        Determines whether or not the range slider range is computed in
        relation to the input data. If `range` is provided, then
        `autorange` is set to *false*.
    
        The 'autorange' property must be specified as a bool
        (either True, or False)

        Returns
        -------
        bool
        """
        return self['autorange']

    @autorange.setter
    def autorange(self, val):
        self['autorange'] = val

    # bgcolor
    # -------
    @property
    def bgcolor(self):
        """
        Sets the background color of the range slider.
    
        The 'bgcolor' property is a color and may be specified as:
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
        return self['bgcolor']

    @bgcolor.setter
    def bgcolor(self, val):
        self['bgcolor'] = val

    # bordercolor
    # -----------
    @property
    def bordercolor(self):
        """
        Sets the border color of the range slider.
    
        The 'bordercolor' property is a color and may be specified as:
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
        return self['bordercolor']

    @bordercolor.setter
    def bordercolor(self, val):
        self['bordercolor'] = val

    # borderwidth
    # -----------
    @property
    def borderwidth(self):
        """
        Sets the border color of the range slider.
    
        The 'borderwidth' property is a integer and may be specified as:
          - An int (or float that will be cast to an int)
            in the interval [0, 9223372036854775807]

        Returns
        -------
        int
        """
        return self['borderwidth']

    @borderwidth.setter
    def borderwidth(self, val):
        self['borderwidth'] = val

    # range
    # -----
    @property
    def range(self):
        """
        Sets the range of the range slider. If not set, defaults to the
        full xaxis range. If the axis `type` is *log*, then you must
        take the log of your desired range. If the axis `type` is
        *date*, it should be date strings, like date data, though Date
        objects and unix milliseconds will be accepted and converted to
        strings. If the axis `type` is *category*, it should be
        numbers, using the scale where each category is assigned a
        serial number from zero in the order it appears.
    
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

    # thickness
    # ---------
    @property
    def thickness(self):
        """
        The height of the range slider as a fraction of the total plot
        area height.
    
        The 'thickness' property is a number and may be specified as:
          - An int or float in the interval [0, 1]

        Returns
        -------
        int|float
        """
        return self['thickness']

    @thickness.setter
    def thickness(self, val):
        self['thickness'] = val

    # visible
    # -------
    @property
    def visible(self):
        """
        Determines whether or not the range slider will be visible. If
        visible, perpendicular axes will be set to `fixedrange`
    
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

    # yaxis
    # -----
    @property
    def yaxis(self):
        """
        The 'yaxis' property is an instance of YAxis
        that may be specified as:
          - An instance of plotly.graph_objs.layout.xaxis.rangeslider.YAxis
          - A dict of string/value properties that will be passed
            to the YAxis constructor
    
            Supported dict properties:
                
                range
                    Sets the range of this axis for the
                    rangeslider.
                rangemode
                    Determines whether or not the range of this
                    axis in the rangeslider use the same value than
                    in the main plot when zooming in/out. If
                    *auto*, the autorange will be used. If *fixed*,
                    the `range` is used. If *match*, the current
                    range of the corresponding y-axis on the main
                    subplot is used.

        Returns
        -------
        plotly.graph_objs.layout.xaxis.rangeslider.YAxis
        """
        return self['yaxis']

    @yaxis.setter
    def yaxis(self, val):
        self['yaxis'] = val

    # property parent name
    # --------------------
    @property
    def _parent_path_str(self):
        return 'layout.xaxis'

    # Self properties description
    # ---------------------------
    @property
    def _prop_descriptions(self):
        return """\
        autorange
            Determines whether or not the range slider range is
            computed in relation to the input data. If `range` is
            provided, then `autorange` is set to *false*.
        bgcolor
            Sets the background color of the range slider.
        bordercolor
            Sets the border color of the range slider.
        borderwidth
            Sets the border color of the range slider.
        range
            Sets the range of the range slider. If not set,
            defaults to the full xaxis range. If the axis `type` is
            *log*, then you must take the log of your desired
            range. If the axis `type` is *date*, it should be date
            strings, like date data, though Date objects and unix
            milliseconds will be accepted and converted to strings.
            If the axis `type` is *category*, it should be numbers,
            using the scale where each category is assigned a
            serial number from zero in the order it appears.
        thickness
            The height of the range slider as a fraction of the
            total plot area height.
        visible
            Determines whether or not the range slider will be
            visible. If visible, perpendicular axes will be set to
            `fixedrange`
        yaxis
            plotly.graph_objs.layout.xaxis.rangeslider.YAxis
            instance or dict with compatible properties
        """

    def __init__(
        self,
        arg=None,
        autorange=None,
        bgcolor=None,
        bordercolor=None,
        borderwidth=None,
        range=None,
        thickness=None,
        visible=None,
        yaxis=None,
        **kwargs
    ):
        """
        Construct a new Rangeslider object
        
        Parameters
        ----------
        arg
            dict of properties compatible with this constructor or
            an instance of
            plotly.graph_objs.layout.xaxis.Rangeslider
        autorange
            Determines whether or not the range slider range is
            computed in relation to the input data. If `range` is
            provided, then `autorange` is set to *false*.
        bgcolor
            Sets the background color of the range slider.
        bordercolor
            Sets the border color of the range slider.
        borderwidth
            Sets the border color of the range slider.
        range
            Sets the range of the range slider. If not set,
            defaults to the full xaxis range. If the axis `type` is
            *log*, then you must take the log of your desired
            range. If the axis `type` is *date*, it should be date
            strings, like date data, though Date objects and unix
            milliseconds will be accepted and converted to strings.
            If the axis `type` is *category*, it should be numbers,
            using the scale where each category is assigned a
            serial number from zero in the order it appears.
        thickness
            The height of the range slider as a fraction of the
            total plot area height.
        visible
            Determines whether or not the range slider will be
            visible. If visible, perpendicular axes will be set to
            `fixedrange`
        yaxis
            plotly.graph_objs.layout.xaxis.rangeslider.YAxis
            instance or dict with compatible properties

        Returns
        -------
        Rangeslider
        """
        super(Rangeslider, self).__init__('rangeslider')

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
The first argument to the plotly.graph_objs.layout.xaxis.Rangeslider 
constructor must be a dict or 
an instance of plotly.graph_objs.layout.xaxis.Rangeslider"""
            )

        # Import validators
        # -----------------
        from plotly.validators.layout.xaxis import (
            rangeslider as v_rangeslider
        )

        # Initialize validators
        # ---------------------
        self._validators['autorange'] = v_rangeslider.AutorangeValidator()
        self._validators['bgcolor'] = v_rangeslider.BgcolorValidator()
        self._validators['bordercolor'] = v_rangeslider.BordercolorValidator()
        self._validators['borderwidth'] = v_rangeslider.BorderwidthValidator()
        self._validators['range'] = v_rangeslider.RangeValidator()
        self._validators['thickness'] = v_rangeslider.ThicknessValidator()
        self._validators['visible'] = v_rangeslider.VisibleValidator()
        self._validators['yaxis'] = v_rangeslider.YAxisValidator()

        # Populate data dict with properties
        # ----------------------------------
        _v = arg.pop('autorange', None)
        self.autorange = autorange if autorange is not None else _v
        _v = arg.pop('bgcolor', None)
        self.bgcolor = bgcolor if bgcolor is not None else _v
        _v = arg.pop('bordercolor', None)
        self.bordercolor = bordercolor if bordercolor is not None else _v
        _v = arg.pop('borderwidth', None)
        self.borderwidth = borderwidth if borderwidth is not None else _v
        _v = arg.pop('range', None)
        self.range = range if range is not None else _v
        _v = arg.pop('thickness', None)
        self.thickness = thickness if thickness is not None else _v
        _v = arg.pop('visible', None)
        self.visible = visible if visible is not None else _v
        _v = arg.pop('yaxis', None)
        self.yaxis = yaxis if yaxis is not None else _v

        # Process unknown kwargs
        # ----------------------
        self._process_kwargs(**dict(arg, **kwargs))
