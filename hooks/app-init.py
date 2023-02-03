# -*- coding: UTF-8 -*-
import os
import subprocess
from pyrevit.userconfig import user_config
from hooksScripts import versionLogger, releasedVersion, snapshot
from customOutput import ct_icon, mass_message_url
from customOutput import def_hookLogs, def_revitBuildLogs, def_revitBuilds, def_massMessagePath
from customOutput import def_syncLogPath, def_openingLogPath, def_dashboardsPath, def_language
from customOutput import company_conf


# reading custom tools company config file if it does exist
# config_values are stored as dictionary
config_values = company_conf()

# creating sections in pyRevit_config.ini if it does not exist
try:
    user_config.add_section('CustomToolsSettings')
except:
    pass
# if parameter does not exist create one in pyRevit_config.ini

# hookLogs
try:
    try:
        # if there is ct_config.ini present reset the values from company config
        user_config.CustomToolsSettings.hookLogs = config_values['hookLogs']
    except: 
        user_config.CustomToolsSettings.hookLogs
except:
    user_config.CustomToolsSettings.hookLogs = def_hookLogs

# revitBuildLogs
try:
    try:
        user_config.CustomToolsSettings.revitBuildLogs = config_values['revitBuildLogs']
    except:
        user_config.CustomToolsSettings.revitBuildLogs
except:
    user_config.CustomToolsSettings.revitBuildLogs = def_revitBuildLogs

# revitBuilds
try:
    try:
        user_config.CustomToolsSettings.revitBuilds = config_values['revitBuilds']
    except:
        user_config.CustomToolsSettings.revitBuilds
except:
    user_config.CustomToolsSettings.revitBuilds = def_revitBuilds

# massMessagePath
try:
    try:
        user_config.CustomToolsSettings.massMessagePath = config_values['massMessagePath']
    except:
        user_config.CustomToolsSettings.massMessagePath
except:
    user_config.CustomToolsSettings.massMessagePath = def_massMessagePath

# syncLogPath
try:
    try:
        user_config.CustomToolsSettings.syncLogPath = config_values['syncLogPath']
    except:
        user_config.CustomToolsSettings.syncLogPath
except:
    user_config.CustomToolsSettings.syncLogPath = def_syncLogPath

# openingLogPath
try:
    try:
        user_config.CustomToolsSettings.openingLogPath = config_values['openingLogPath']
    except:
        user_config.CustomToolsSettings.openingLogPath
except:
    user_config.CustomToolsSettings.openingLogPath = def_openingLogPath

# dashboardsPath
try:
    try:
        user_config.CustomToolsSettings.dashboardsPath = config_values['dashboardsPath']
    except:
        user_config.CustomToolsSettings.dashboardsPath
except:
    user_config.CustomToolsSettings.dashboardsPath = def_dashboardsPath

# language
try:
    try:
        # language is a number stored as string - it must be converted to integer
        user_config.CustomToolsSettings.language = int(config_values['language'])
    except:
        user_config.CustomToolsSettings.language
except:
    # user_config.CustomToolsSettings.language = str(def_language)
    user_config.CustomToolsSettings.language = def_language

# pyrevit telemetry path
try:
    # try to read telemetry path from the customtools config file
    # cmd_command = 'cmd /c PowerShell pyrevit configs telemetry file "' + company_conf()['pyrevitTelemetry'] + '"'
    user_config.telemetry.telemetry_file_dir = config_values['pyrevitTelemetry']
except:
    # if there is no telemetry path present in the config file
    # cmd_command = 'cmd /c PowerShell pyrevit configs telemetry file "L:\\customToolslogs\\toolsLogs"'
    user_config.telemetry.telemetry_file_dir = "L:\\customToolslogs\\toolsLogs"
# os.system(cmd_command)

user_config.save_changes()

# write log with revit build, username, CTversion and timestamp
# check revit build and show warning window if it's wrong
versionLogger(releasedVersion,snapshot)

# CustomTools update at revit startup
try:
    appdataPath = os.getenv('APPDATA')
    # replacing CustomToolsUpdater.cmd file each time when revit starts
    # uncomment only when it is needed
    # running InitUpdate.cmd script at:
    # %AppData%\\Roaming\\pyRevit\\Extensions\\CustomTools.extension\\hooks\\InitUpdate.cmd
    #newCTupdatePath = appdataPath + '\\pyRevit\\Extensions\\CustomTools.extension\\hooks\\InitUpdate.cmd'
    #u = subprocess.Popen([newCTupdatePath])

    # updating CustomTools from the git repository
    # running CustomToolsUpdater.cmd script at:
    # %AppData%\\Roaming\\pyRevit\\Extensions\\CustomTools.extension\\updater\\CustomToolsUpdater.cmd
    updaterPath = appdataPath + '\\pyRevit\\Extensions\\CustomTools.extension\\updater\\CustomToolsUpdater.cmd'
    p = subprocess.Popen([updaterPath])
except:
    pass

"""TEASER."""
#prints heading and links offline version of mass message
from pyrevit import script
output = script.get_output()
output.set_height(700)
output.set_title("Mass Message")
# changing icon
ct_icon(output)

# server version of massmessage
output.open_page(mass_message_url(output))