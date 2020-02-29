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

import supporting.deploylist
from cicd import informatica
from cicd.informatica import infaSettings
from cicd.informatica import infaConstants
from supporting import generalSettings
from supporting import errorcodes

logger = logging.getLogger(__name__)
entrynr = 0

def processList(what, deployFile):
    this_function = "processList"
    latest_result = errorcodes.OK
    overall_result = errorcodes.OK

    supporting.log(logger, logging.DEBUG, this_function, "deployfile is >" + deployFile + "<.")
    result, deploy_items = supporting.deploylist.getWorkitemList(deployFile)
    if result.rc == 0:
        if what == infaConstants.DEPLOY_APP:
            for deployEntry in deploy_items:
                latest_result = process_deploy_app_entry(what, deployEntry)
                if latest_result.rc != errorcodes.OK.rc:
                    overall_result = latest_result
        elif what == infaConstants.CREATE_APP:
            for deployEntry in deploy_items:
                latest_result = process_create_app_entry(what, deployEntry)
                if latest_result.rc != errorcodes.OK.rc:
                    overall_result = latest_result
        else:
            supporting.log(logger, logging.ERROR, this_function, 'Invalid "what" value >' + what + '.')
            overall_result = errorcodes.INVALID_DEPLOY_TYPE

        return overall_result
    else:
        supporting.log(logger, logging.ERROR, this_function, "Could not get deploylist")
        return errorcodes.FILE_NF


def create_iar_file(app_path):
    result = informatica.create_iar_file(
        Domain=infaSettings.sourceDomain,
        Repository=infaSettings.sourceModelRepository,
        ApplicationPath=app_path,
        OutputDirectory=generalSettings.artifactDir + "/",
    )

    return result


def deploy_iar_file(app_name, dis_name):
    informatica_app_dir = infaSettings.target_informatica_app_dir

    result = informatica.deploy_iar_file(
        Domain=infaSettings.targetDomain,
        Application=app_name,
        ServiceName=dis_name,
        FileName=informatica_app_dir + "/" + app_name + '.iar'
    )

    return result


def redeploy_iar_file(app_name, dis_name):
    informatica_app_dir = infaSettings.target_informatica_app_dir

    result = informatica.redeploy_iar_file(
        Domain=infaSettings.targetDomain,
        Application=app_name,
        ServiceName=dis_name,
        FileName=informatica_app_dir + "/" + app_name + '.iar'
    )

    return result


def process_create_app_entry(what, deployEntry):
    global entrynr
    thisproc = "process_create_app_entry"
    result = errorcodes.OK

    entrynr += 1
    supporting.log(logger, logging.DEBUG, thisproc,
                   "Started to work on deploy entry# >" + str(entrynr) + "< being >" + deployEntry + "<.")
    parts = deployEntry.split(':')
    if not len(parts) == 2:
        supporting.log(logger, logging.DEBUG, thisproc,
                       "Expected 2 arguments, got >" + str(len(parts)) + "<.")
        return errorcodes.IGNORE

    app_path = parts[0]
    supporting.log(logger, logging.DEBUG, thisproc, 'app_path is >' + app_path + '<')
    result = create_iar_file(app_path)

    return result


def process_deploy_app_entry(what, deployEntry):
    global entrynr
    thisproc = "process_deploy_app_entry"
    result = errorcodes.OK

    entrynr += 1
    supporting.log(logger, logging.DEBUG, thisproc,
                   "Started to work on deploy entry# >" + str(entrynr) + "< being >" + deployEntry + "<.")
    parts = deployEntry.split(':')
    if not len(parts) == 2:
        supporting.log(logger, logging.DEBUG, thisproc,
                       "Insufficient entries found. Expected 2, got >" + str(len(parts)) + "<.")
        return errorcodes.IGNORE

    app_path = parts[0]
    app_name = app_path.rsplit('/', 1)[1]
    logical_dis_name = parts[1]

    # find the actual DIS name
    actual_dis_name = infaSettings.get_dis_name(logical_dis_name)

    supporting.log(logger, logging.DEBUG, thisproc, 'app_name is >' + app_name + '<, logical_dis_name is >'
                   + logical_dis_name + '<, actual_dis_name is >' + actual_dis_name + '<.')

    #TODO: Check if app exists, if so, run redeploy_iar_file, if not, run deploy_iar_file
    result = deploy_iar_file(app_name, actual_dis_name)
    if result.rc != errorcodes.OK.rc:
        # Check the message if the failure is due to the fact the app already exists
        if infaConstants.informatica_app_already_exists in result.message:
            supporting.log(logger, logging.DEBUG, thisproc, 'Application >' + app_name
                           + '< already exists, will update it. (Code contains TODO to optimize the process)')
            result = redeploy_iar_file(app_name, actual_dis_name)


    return result
