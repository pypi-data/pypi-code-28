import subprocess
import json
import atexit
import jsonschema
import psutil
import sys
import random
import time
import datetime
import os

class Execution:
    """
        This class represents a single execution of a model with a given set of hyper-parameters. It takes care of
        of managing the model process and standardizing the results.
    """

    def __init__(self, config, parameters):
        """
            Initialize this execution with the given configuration and the given parameters.

            :param config: The Execution configuration. See configurationSchema() or the README file for more information.
            :param parameters: The hyper parameters for this model.
        """
        jsonschema.validate(config, self.configurationSchema())

        # Perform one additional validation
        if ('auto_kill_max_time' in config or 'auto_kill_max_ram' in config or 'auto_kill_max_system_ram' in config) and ('auto_kill_loss' not in config):
            raise ValueError("Configuration for model execution has an auto_kill parameter, but is missing the auto_kill_loss. Please set an auto_kill_loss to use automatic kill.")

        self.config = config
        self.parameters= parameters

        self.process = None
        self.result = None
        self.startTime = None
        self.endTime = None
        self.killed = False

    @classmethod
    def configurationSchema(self):
        """ This method returns the configuration schema for the execution module. The schema
            is a standard JSON-schema object."""
        return {
            "type": "object",
            "oneOf": [{
                "properties": {
                    "type": {
                        "type": "string",
                        "constant": "python_function"
                    },
                    "module": {"type": "string"},
                    "name": {"type": "string"}
                },
                "required": ['type', 'module', 'name']
            }],
            "properties": {
                "auto_kill_max_time": {"type": "number"},
                "auto_kill_max_ram": {"type": "number"},
                "auto_kill_max_system_ram": {"type": "number"},
                "auto_kill_loss": {"type": "number"}
            }
        }

    def generateScriptToken(self):
        """
            The script token is used to easily differentiate when the log-output from the model is finished, and its results JSON object
            is now being printed.

            The token is just a random string that is extremely unlikely to come up in log output, used to define the cutoff line.

            Its saved to self.scriptToken

            :return: The generated script token
        """
        characters = 'abcdefghijklmnopqrstuvwxyz123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.scriptToken = ''.join([random.choice(characters) for c in range(64)])
        return self.scriptToken


    def createPythonFunctionScript(self):
        """
            This creates a Python script that will be executed to call the given Python function.

            :return: A string representing the Python script
        """
        self.generateScriptToken()
        script = "from " + self.config['module'] + " import " + self.config['name'] + "\n"
        script += "import json\n"
        script += "result = " + self.config['name'] + "(" + json.dumps(self.parameters) + ")\n"
        script += "print(\"" + self.scriptToken + "\")\n"
        script += "print(json.dumps(result))\n"
        return script

    def startSubprocess(self):
        """
            This function starts a subprocess to execute a model.

            :return: The subprocess.Popen object representing the subprocess. Also stored in self.process
        """
        if self.config['type'] == 'python_function':
            process = subprocess.Popen(['python3', '-c', self.createPythonFunctionScript()], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            atexit.register(lambda: process.kill())

            # Set process affinities - hypermax in one, the model in the rest. Prevents them from causing cache conflicts.
            if psutil.cpu_count() > 2:
                processUtil = psutil.Process(process.pid)
                processUtil.cpu_affinity([k for k in range(psutil.cpu_count()-1)])
                processUtil = psutil.Process(os.getpid())
                processUtil.cpu_affinity([psutil.cpu_count()-1])

            self.process = process
            self.startTime = datetime.datetime.now()
            return process
        else:
            pass


    def shouldKillProcess(self):
        """
            This method checks all of the conditions on the process, such as time usage and RAM usage, to decide whether
            it should be killed prematurely.

            :return: True/False on whether the process should be killed prematurely.
        """
        processStats = psutil.Process(self.process.pid)

        memUsageMB = float(processStats.memory_info().vms) / (1024*1024)
        if 'auto_kill_max_ram' in self.config and memUsageMB > self.config['auto_kill_max_ram']:
            return True

        systemStats = psutil.virtual_memory()
        memUsageMB = float(systemStats.total - systemStats.available) / (1024 * 1024)
        if 'auto_kill_max_system_ram' in self.config and memUsageMB > self.config['auto_kill_max_system_ram']:
            return True

        elapsedTime = (datetime.datetime.now() - self.startTime).total_seconds()
        if 'auto_kill_max_time' in self.config and elapsedTime > self.config['auto_kill_max_time']:
            return True

        return False


    def run(self):
        """
            Run the model, return the results.

            :return: A standard 'results' object.
        """
        # print("Running: ", parameters)
        if self.config['type'] == 'python_function':
            process = self.startSubprocess()
            while process.returncode is None:
                process.poll()
                try:
                    if self.shouldKillProcess():
                        self.killed = True
                        parent = psutil.Process(process.pid)
                        children = parent.children(recursive=True)
                        children.append(parent)
                        for p in children:
                            p.send_signal(9)
                except psutil.NoSuchProcess:
                    pass
                time.sleep(0.1)

            if self.killed:
                output = str(process.stdout.read(), 'utf8')
                self.result = {"status": "fail", "loss": self.config['auto_kill_loss'], "log": output, "error": "Model was automatically killed.",
                               "time": (datetime.datetime.now() - self.startTime).total_seconds()}
                self.process = None
                return self.result

            output = str(process.stdout.read(), 'utf8')
            cutoffIndex = output.find(self.scriptToken)
            if cutoffIndex == -1:
                self.result = {"status": "fail", "loss": None, "log": output, "error": "Did not find result object in the output from the model script."}
                self.process = None
                return self.result
            else:
                resultString = output[cutoffIndex + len(self.scriptToken)+1:]
                try:
                    rawResult = json.loads(resultString)
                    self.result = self.interpretResultObject(rawResult)
                    self.result['status'] = 'ok'
                    self.result['log'] = output[:cutoffIndex]
                    self.result['error'] = None
                    self.process = None
                    return self.result
                except json.JSONDecodeError as e:
                    self.result = {"status": "fail", "loss": None, "log": output, "error": "Unable to decode the JSON result object from the model."}
                    self.process = None
                    return self.result

    def interpretResultObject(self, rawResult):
        """
            This method has the job of interpreting and standardizing the result object from the model.

            :param rawResult: The raw result object from the model.
            :return: The standardized results object.
        """
        if isinstance(rawResult, int) or isinstance(rawResult, float) or isinstance(rawResult, bool):
            return {"loss": rawResult}
        elif isinstance(rawResult, dict):
            return rawResult
        else:
            raise ValueError("Unexpected value for result object from model: " + json.dumps(rawResult) + "\nReturn value must be either a Python dictionary/JSON object or a single floating point value.")