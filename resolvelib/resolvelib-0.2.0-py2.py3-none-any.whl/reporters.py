class BaseReporter(object):
    """Delegate class to provider progress reporting for the resolver.
    """
    def starting(self):
        """Called before the resolution actually starts.
        """

    def starting_round(self, index):
        """Called before each round of resolution starts.
        """

    def ending_round(self, index, state):
        """Called before each round of resolution ends.

        This is NOT called if the resolution ends at this round.
        """

    def ending(self, state):
        """Called before the resolution ends successfully.
        """
