from exceptions import ZeroDivisionError

def execute(self, inputs, outputs, gvm):
    self.logger.debug("Executing decider state")
    self.logger.debug("state-inputs: %s" % str(inputs))
    if isinstance(self.get_errors_for_state_name("Second"), ZeroDivisionError):
        return 1
    else:
        return 0
