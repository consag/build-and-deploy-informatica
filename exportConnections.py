#  MIT License
#
#  Copyright (c) 2019 Jac. Beekers
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.
#

import logging, datetime, supporting
from supporting import errorcodes
from informatica import infaSettings
from informatica import infaConstants
from supporting import generalSettings
from informatica import manageConnection
import sys

now = datetime.datetime.now()
result = errorcodes.OK

def main(argv):
    thisproc = "MAIN"
    mainProc='exportConnections'

    resultlogger = supporting.configurelogger(mainProc)
    logger = logging.getLogger(mainProc)

    generalSettings.getenvvars()

    supporting.log(logger, logging.DEBUG, thisproc, 'Started')
    supporting.log(logger, logging.DEBUG, thisproc, 'logDir is >' + generalSettings.logDir + "<.")

#    if len(argv) < 1:
#        supporting.log(logger, logging.ERROR, thisproc, 'No group name provided.')
#        result = errorcodes.INFACMD_NOGROUPNAME
#        supporting.exitscript(resultlogger, result)

#    # mandatory
#    group_name = argv[0]
    # optional
    output_file = argv[0] if len(argv) > 0 else infaConstants.DEFAULT_EXPORT_CONNECTIONSFILE
    export_control_file = argv[1] if len(argv) > 1 else ""

    infaSettings.getinfaenvvars()
    infaSettings.outinfaenvvars()

    if export_control_file != "":
        connection = manageConnection.ManageConnection(Tool="ExportConnections",
            Domain=infaSettings.sourceDomain,
            ExportControlfile=export_control_file,
            ExportFile=output_file,
            RetainPassword='true',
            Force='true',
            OnError=errorcodes.INFACMD_EXPORT_CONN_FAILED
        )
    else:
        connection = manageConnection.ManageConnection(Tool="ExportConnections",
            Domain=infaSettings.sourceDomain,
            ExportFile=output_file,
            RetainPassword='true',
            Force='true',
            OnError=errorcodes.INFACMD_EXPORT_CONN_FAILED
        )

    result = connection.manage()

    supporting.log(logger, logging.DEBUG, thisproc, 'Completed with return code >' + str(result.rc)
                   + '< and result code >' + result.code + "<.")
    supporting.exitscript(resultlogger, result)


main(sys.argv[1:])
