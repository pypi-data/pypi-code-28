# -*- coding: utf-8 -*-
"""
Zurich Instruments LabOne Python API Example.

Demonstrate how to connect to a Zurich Instruments Device and obtain streaming
scope data from one or two scope channels.
"""

# Copyright 2018 Zurich Instruments AG

from __future__ import print_function
import time
import warnings
import numpy as np
import zhinst.utils


def run_example(device_id, do_plot=False, scope_stream_rate=12, scope_inputselects=[16, 32]):
    """
    Run the example: Connect to a Zurich Instruments Device via the Data Server,
    generate a constant signal on the auxillary outputs and demodulate it in
    order to observe a sine wave in the demodulator X and Y output. Acquire the
    demodulator X and Y output on the scope's streaming channels using subscribe
    and poll (the Scope Module does not support the scopes's streaming
    nodes). Obtains a fixed number of scope samples (defined below as
    num_scope_samples).

    Requirements:

      MF or UHF Instrument with DIG Option (HF2 does not support scope
        streaming).

    Arguments:

      device_id (str): The ID of the device to run the example with. For
        example, `dev2006` or `uhf-dev2006`.

      do_plot (bool, optional): Specify whether to plot the acquired
        data. Default is no plot output. Plotting requires the matplotlib
        module.

      scope_stream_rate: The rate of the scope streaming data, the data will be
      set at a rate of clockbase/2**rate. For example:
        8  - sets the sampling rate to 7.03 MHz
        9  - "                         3.50 MHz
        ...
        16 - "                         27.5 kHz

      scope_inputselect (list of int, optional): A list containing one or two
        input signals to measure with the scope
        (/dev..../scopes/0/channels/{0,1}/inputselect). For example, [16,
        32]. Example values (see the User Manual for more info):
          0  - signal input 0,
          1  - signal input 1,
          2  - signal output 0,
          3  - signal output 1,
          16 - demod 0 X,
          32 - demod 0 Y.

    Returns:

      data (dict of numpy arrays): The last dictionary as returned by poll.

      scope_samples(list of dict): A list of dictionaries. Each entry in the is
        a dictionary with the keys timestamp and value holding the data obtained
        for one scope channel.

    Raises:

      Exception: If the specified device is not an MF or UHF with the DIG
        Option.

      RuntimeError: If the device is not "discoverable" from the API.

    See the "LabOne Programing Manual" for further help, available:
      - On Windows via the Start-Menu:
        Programs -> Zurich Instruments -> Documentation
      - On Linux in the LabOne .tar.gz archive in the "Documentation"
        sub-folder.
    """

    apilevel_example = 6  # The API level supported by this example.
    # Call a zhinst utility function that returns:
    # - an API session `daq` in order to communicate with devices via the data server.
    # - the device ID string that specifies the device branch in the server's node hierarchy.
    # - the device's discovery properties.
    # This example can't run with HF2 Instruments or instruments without the DIG option.
    required_devtype = r'UHFLI|MF'  # Regular expression of supported instruments.
    required_options = ['DIG']
    required_err_msg = "This example requires the DIG Option on either UHFLI or MF instruments (HF2 is unsupported)."
    (daq, device, _) = zhinst.utils.create_api_session(device_id, apilevel_example,
                                                       required_devtype=required_devtype,
                                                       required_options=required_options,
                                                       required_err_msg=required_err_msg)
    zhinst.utils.api_server_version_check(daq)

    # Enable the API's log.
    daq.setDebugLevel(0)

    # Create a base configuration: Disable all available outputs, awgs, demods, scopes,...
    zhinst.utils.disable_everything(daq, device)

    # The value of the instrument's ADC sampling rate.
    clockbase = daq.getInt('/{}/clockbase'.format(device))
    rate = clockbase/2**scope_stream_rate

    # Now configure the instrument for this experiment.
    auxout_channel = 0
    demod_channel = 0
    osc_index = 0
    num_samples_period = 16
    frequency = rate/num_samples_period
    exp_setting = [
        ['/%s/auxouts/%d/outputselect'   % (device, auxout_channel), -1],  # Auxout manual mode.
        ['/%s/auxouts/%d/offset'         % (device, auxout_channel), 1],
        ['/%s/auxouts/%d/limitlower'     % (device, auxout_channel), -10],
        ['/%s/auxouts/%d/limitupper'     % (device, auxout_channel), 10],
        ['/%s/oscs/%d/freq'              % (device, osc_index), frequency]]
    node_branches = daq.listNodes('/{}/'.format(device), 0)
    if 'DEMODS' in node_branches:
        # NOTE we don't need to obtain any demodulator data directly from the
        # DEMODS branch for this example (it is obtained directly by the scope
        # within the device using a feedback channel in the firmware), but we
        # need to configure the demodulator input and the frequency of the
        # output signal on out_mixer_c.
        exp_setting.append(['/%s/demods/%d/timeconstant' % (device, demod_channel), 0.])
        exp_setting.append(['/%s/demods/%d/oscselect' % (device, demod_channel), osc_index])
        # ADCSELECT: Specify which source signal the demodulator should use as its input.
        exp_setting.append(['/%s/demods/%d/adcselect' % (device, demod_channel), auxout_channel + 4])
    daq.set(exp_setting)

    # Perform a global synchronisation between the device and the data server:
    # Ensure that the signal input and output configuration has taken effect
    # before calculating the signal input autorange.
    daq.sync()

    ####################################################################################################################
    # Configure the scope's channels and streaming nodes.
    # Note: Nodes not listed below not effect the scope streaming data, e.g. (scopes/0/{time,length,trig*,...}).
    ####################################################################################################################
    #
    # 'channels/0/bwlimit' : bandwidth limit the scope data. Enabling bandwidth
    # limiting avoids antialiasing effects due to subsampling when the scope
    # sample rate is less than the input channel's sample rate.
    #  Bool:
    #   0 - do not bandwidth limit
    #   1 - bandwidth limit
    daq.setInt('/%s/scopes/0/channels/*/bwlimit' % device, 1)
    # 'channel/0/channels/*/inputselect' : the input channel for the scope:
    #   0 - signal input 1
    #   1 - signal input 2
    #   2, 3 - trigger 1, 2 (front)
    #   8-9 - auxiliary inputs 1-2
    #   The following inputs are additionally available with the DIG option:
    #   10-11 - oscillator phase from demodulator 3-7
    #   16-23 - demodulator 0-7 x value
    #   32-39 - demodulator 0-7 y value
    #   48-55 - demodulator 0-7 R value
    #   64-71 - demodulator 0-7 Phi value
    #   80-83 - pid 0-3 out value
    #   96-97 - boxcar 0-1
    #   112-113 - cartesian arithmetic unit 0-1
    #   128-129 - polar arithmetic unit 0-1
    #   144-147 - pid 0-3 shift value
    # Here, we specify the demod 0 X and y values for channels 1 and 2, respectively.
    daq.setInt('/%s/scopes/0/channels/0/inputselect' % device, scope_inputselects[0])
    if len(scope_inputselects) > 1:
        daq.setInt('/%s/scopes/0/channels/1/inputselect' % device, scope_inputselects[1])
    # 'channels/0/channels/*/limit{lower,upper}
    # Set the scope limits for the data to values far outside legal values
    # allowed by the firmware; the firmware will clamp to the smallest/largest
    # value of the legal lower/upper limits.
    #
    # NOTE: In order to obtain the best possible bit resolution in the scope,
    # these values should be set according to the magnitude of the signals being
    # measured in the scope.
    daq.setDouble('/%s/scopes/0/channels/*/limitlower' % device, -10e9)
    daq.setDouble('/%s/scopes/0/channels/*/limitupper' % device, 10e9)
    # 'stream/rate' : specifies the rate of the streaming data, the data will be set at a rate of clockbase/2**rate.
    #   7  - sets the samplint rate to 14.06 MHz (maximum rate supported by 1GbE)
    #   8  -                            7.03 MHz (maximum rate supported by USB)
    #   9  - "                          3.50 MHz
    #   ...
    #   16 - "                          27.5 kHz
    daq.setDouble('/%s/scopes/0/stream/rate' % device, scope_stream_rate)

    # Perform a global synchronisation between the device and the data server: Ensure that the settings have taken
    # effect on the device before enabling streaming and acquiring data.
    daq.sync()

    # Enable the scope streaming nodes:
    daq.setInt('/%s/scopes/0/stream/enables/0' % device, 1)
    if len(scope_inputselects) > 1:
        daq.setInt('/%s/scopes/0/stream/enables/1' % device, 1)

    # Ensure buffers are flushed before subscribing.
    daq.sync()

    # Subscribe to the scope's streaming samples in the ziDAQServer session.
    stream_nodepath = '/{}/scopes/0/stream/sample'.format(device)
    daq.subscribe(stream_nodepath)

    # We will construct arrays of the scope streaming samples and their timestamps.
    num_scope_samples = int(1e5)  # Critical parameter for memory consumption.
    # Preallocate arrays.
    scope_samples = [{'value': np.nan*np.ones(num_scope_samples), 'timestamp': np.zeros(num_scope_samples, dtype=int)},
                     {'value': np.nan*np.ones(num_scope_samples), 'timestamp': np.zeros(num_scope_samples, dtype=int)}]

    n = 0  # The number of scope samples acquired on each channel.
    num_blocks = 0  # Just for statistics.
    poll_count = 0
    timeout = 60
    t_start = time.time()
    while n < num_scope_samples:
        if time.time() - t_start > timeout:
            raise Exception("Failed to acquired %d scope samples after %f s. Num samples acquired")
        data = daq.poll(0.02, 200, 0, True)
        poll_count += 1
        if stream_nodepath not in data:
            # Could be the case for very slow streaming rates and fast poll frequencies.
            print("Poll did not return any subscribed data.")
            continue
        num_blocks_poll = len(data[stream_nodepath])
        num_blocks += num_blocks_poll
        print("Poll #", poll_count, " returned ", num_blocks_poll, " blocks of streamed scope data",
              "blocks processed ", num_blocks, ", samples acquired ", n, ".", sep="", end='\r')
        for b, block in enumerate(data[stream_nodepath]):
            if block['flags'] & 1:
                message = "Block {} from poll indicates dataloss (flags: {})".format(b, block['flags'])
                warnings.warn(message)
                continue
            if block['flags'] & 2:
                # This should not happen.
                message = "Block {} from poll indicates missed trigger (flags: {})".format(b, block['flags'])
                warnings.warn(message)
                continue
            if block['flags'] & 3:
                message = "Block {} from poll indicates transfer failure  (flags: {})".format(b, block['flags'])
                warnings.warn(message)
            assert block['datatransfermode'] == 3, \
                "The block's datatransfermode states the block does not contain scope streaming data."
            num_samples_block = len(block['wave'][:, 0])  # The same for all channels.
            if num_samples_block + n > num_scope_samples:
                num_samples_block = num_scope_samples - n
            ts_delta = int(clockbase*block['dt'])  # The delta inbetween timestamps.
            for (i,), channelenable in np.ndenumerate(block['channelenable']):
                if not channelenable:
                    continue
                # 'timestamp' is the last sample's timestamp in the block.
                ts_end = block['timestamp'] - (len(block['wave'][:, i]) - num_samples_block)*ts_delta
                ts_start = ts_end - num_samples_block*ts_delta
                scope_samples[i]['timestamp'][n:n + num_samples_block] = np.arange(ts_start, ts_end, ts_delta)
                scope_samples[i]['value'][n:n + num_samples_block] = \
                    block['channeloffset'][i] + block['channelscaling'][i]*block['wave'][:num_samples_block, i]
            n += num_samples_block
    daq.sync()
    daq.setInt('/%s/scopes/*/stream/enable' % device, 0)
    daq.unsubscribe('*')

    print()
    print("Total blocks processed ", num_blocks, ", samples acquired ", n, ".", sep="")

    expected_ts_delta = 2**scope_stream_rate
    for c, channel_samples in enumerate(scope_samples):
        # Check for sampleloss
        nan_count = np.sum(np.isnan(scope_samples[c]['value']))
        zero_count = np.sum(scope_samples[c]['timestamp'] == 0)
        diff_timestamps = np.diff(scope_samples[c]['timestamp'])
        min_ts_delta = np.min(diff_timestamps)
        max_ts_delta = np.max(diff_timestamps)
        if nan_count:
            nan_index = np.where(np.isnan(scope_samples[c]['value']))[0]
            warnings.warn("Scope channel %d values contain %d/%d nan entries (starting at index %d)."
                          % (c, nan_count, len(scope_samples[c]['value']), nan_index[0]))
        if zero_count:
            warnings.warn("Scope channel %d timestamps contain %d entries equal to 0." % (c, zero_count))
        ts_delta_mismatch = False
        if min_ts_delta != expected_ts_delta:
            index = np.where(diff_timestamps == min_ts_delta)[0]
            warnings.warn("Scope channel %d timestamps have a min_diff %d (first discrepancy at pos: %d). "
                          "Expected %d." % (c, min_ts_delta, index[0], expected_ts_delta))
            ts_delta_mismatch = True
        if max_ts_delta != expected_ts_delta:
            index = np.where(diff_timestamps == max_ts_delta)[0]
            warnings.warn("Scope channel %d timestamps have a max_diff %d (first discrepenacy at pos: %d). "
                          "Expected %d." % (c, max_ts_delta, index[0], expected_ts_delta))
            ts_delta_mismatch = True
        dt = (channel_samples['timestamp'][-1] - channel_samples['timestamp'][0])/float(clockbase)
        print("Samples in channel", c, "span", dt, "s at a rate of", rate/1e3, "kHz.")
        assert not nan_count, "Detected NAN in the array of scope samples."
        assert not ts_delta_mismatch, "Detected an unexpected timestamp delta in the scope data."

    if do_plot:
        import matplotlib.pyplot as plt

        # Get the instrument's ADC sampling rate.
        clockbase = daq.getInt('/{}/clockbase'.format(device))

        n = num_samples_period*5
        plt.figure(1)
        plt.clf()
        for c, channel_samples in enumerate(scope_samples):
            t = (channel_samples['timestamp'][0:n] - channel_samples['timestamp'][0])/clockbase
            plt.plot(t*1e6, channel_samples['value'][0:n])
        plt.draw()
        plt.grid(True)
        plt.xlabel(r'Time [$\mu$s]')
        plt.ylabel(r'Amplitude [V]')
        plt.autoscale(enable=True, axis='x', tight=True)
        dt = (scope_samples[0]['timestamp'][-1] - scope_samples[0]['timestamp'][0])/clockbase
        plt.title(r'Scope streaming data portion (total duration acquired %.1f s)' % dt)

    return data, scope_samples
