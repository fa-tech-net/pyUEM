import time
import os
import sys


class Logger(object):
    """
    Class for logging
    """

    def __init__(self, path=None, logname=None, log_error_filename=None):
        super(Logger, self).__init__()
        if logname is None:
            self.__logname = "Logger.py." \
                             + str(os.getpid()) + "." + time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()) + ".log"
        else:
            self.__logname = str(logname)
        if log_error_filename is None:
            self.__logErrorName = self.__logname + ".error"
        else:
            self.__logErrorName = str(log_error_filename)
        if path is None:
            path = "./"
        self.__printOutput = False
        self.__path = path
        self.__VERBOSE = False
        self.__writeLogfile = True
        self.__logFile = None
        self.__errorLogFile = None

    def toggle_verbose(self):
        self.__VERBOSE = not self.__VERBOSE

    def set_verbose(self, b):
        self.__VERBOSE = not (not b)  # force casting into boolean

    def toggle_print(self):
        self.__printOutput = not self.__printOutput

    def set_print(self, value):
        self.__printOutput = value

    def toggle_logfile(self):
        self.__writeLogfile = not self.__writeLogfile

    def disable_logfile_write(self):
        self.__writeLogfile = False

    @staticmethod
    def static_log(loglevel, message):
        curr_time = str(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()))  # getting current time
        sys.stdout.write(str(curr_time) + " - " + "[" + str(loglevel) + "]\t- " + str(message) + os.linesep)

    def log(self, loglevel, message):
        """
        Write log into carrier
        :param loglevel:
        :param message:
        :return:
        """
        curr_time = str(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()))  # getting current time
        if self.__writeLogfile:
            if self.__logFile is None:
                self.__logFile = open(self.__path + "/" + self.__logname, 'a+')  # Append or create file
            self.__logFile.write(str(curr_time) + " - " + "[" + str(loglevel) + "]\t- " + str(message) + os.linesep)
        if self.__printOutput:
            sys.stdout.write(str(curr_time) + " - " + "[" + str(loglevel) + "]\t- " + str(message) + os.linesep)

    def log_error(self, loglevel, message):
        """
        Write on stderr, and, if set, logfile error
        :param loglevel:
        :param message:
        :return:
        """
        curr_time = str(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime()))  # getting current time
        sys.stderr.write(str(curr_time) + " - " + "[" + str(loglevel) + "]\t- " + str(message) + os.linesep)
        if self.__writeLogfile:
            if self.__errorLogFile is None:
                self.__errorLogFile = open(self.__path + "/" + self.__logErrorName, 'a+')  # Append or create file
            self.__errorLogFile.write(
                str(curr_time) + " - " + "[" + str(loglevel) + "]\t- " + str(message) + os.linesep)


class LogBuffer(object):
    """
    Little component for buffering logs
    """

    def __init__(self):
        super(LogBuffer, self).__init__()
        self._log = []

    def get_log(self):
        return self._log

    def set_log(self, log):
        self._log = log

    def log(self, loglevel, data, is_error=False):
        message = [loglevel, data, is_error]
        self._log.append(message)

    def flush_log(self, logger):
        for loglevel, data, is_error in self._log:
            if is_error:
                logger.logError(loglevel, data)
            else:
                logger.log(loglevel, data)
        self._log = []

    @staticmethod
    def flush_all(obj_list, logger):
        for obj in obj_list:
            if isinstance(obj, LogBuffer) is LogBuffer:
                obj.flush_log(logger)
