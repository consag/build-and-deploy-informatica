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
import logging
from informatica import executeCommand
import os
from informatica import infaSettings
from supporting import errorcodes

logger = logging.getLogger(__name__)
entrynr = 0


def execute(command):
    """Execute an Informatica command line
    Sets INFA_DEFAULT_DOMAIN_PASSWORD, INFA_DEFAULTS_DOMAIN_USER and INFA_DEFAULT_SECURITY_DOMAIN based on provided Informatica settings.
    """
    infa_env = {**os.environ, 'INFA_DEFAULT_DOMAIN_PASSWORD': infaSettings.sourcePassword,
                'INFA_DEFAULT_DOMAIN_USER': infaSettings.sourceUsername,
                'INFA_DEFAULT_SECURITY_DOMAIN': infaSettings.sourceSecurityDomain}

    result = executeCommand.execute(command, infa_env)

    if result.code == errorcodes.COMMAND_FAILED:
        old_result = result.message
        result = errorcodes.INFACMD_FAILED
        result.message = old_result

    return result
