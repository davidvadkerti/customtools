# -*- coding: UTF-8 -*-
from pyrevit.userconfig import user_config
from hooksScripts import versionLogger, releasedVersion, snapshot
from customOutput import ct_icon, mass_message_url
from customOutput import def_hookLogs, def_revitBuildLogs, def_revitBuilds, def_massMessagePath
from customOutput import def_syncLogPath, def_openingLogPath, def_dashboardsPath, def_language

# CustomTools update at revit startup
import os
import subprocess
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


# creating sections in pyRevit_config.ini if it does not exist
try:
    user_config.add_section('CustomToolsSettings')
except:
    pass
# if parameter does not exist create one in pyRevit_config.ini
# hookLogs
try:
    user_config.CustomToolsSettings.hookLogs
except AttributeError:
    user_config.CustomToolsSettings.hookLogs = def_hookLogs
# revitBuildLogs
try:
    user_config.CustomToolsSettings.revitBuildLogs
except AttributeError:
    user_config.CustomToolsSettings.revitBuildLogs = def_revitBuildLogs
# revitBuilds
try:
    user_config.CustomToolsSettings.revitBuilds
except AttributeError:
    user_config.CustomToolsSettings.revitBuilds = def_revitBuilds
# massMessagePath
try:
    user_config.CustomToolsSettings.massMessagePath
except AttributeError:
    user_config.CustomToolsSettings.massMessagePath = def_massMessagePath
# syncLogPath
try:
    user_config.CustomToolsSettings.syncLogPath
except AttributeError:
    user_config.CustomToolsSettings.syncLogPath = def_syncLogPath
# openingLogPath
try:
    user_config.CustomToolsSettings.openingLogPath
except AttributeError:
    user_config.CustomToolsSettings.openingLogPath = def_openingLogPath
# dashboardsPath
try:
    user_config.CustomToolsSettings.dashboardsPath
except AttributeError:
    user_config.CustomToolsSettings.dashboardsPath = def_dashboardsPath
# language
try:
    user_config.CustomToolsSettings.language
except AttributeError:
    # user_config.CustomToolsSettings.language = str(def_language)
    user_config.CustomToolsSettings.language = def_language

user_config.save_changes()

# write log with revit build, username, CTversion and timestamp
# check revit build and show warning window if it's wrong
versionLogger(releasedVersion,snapshot)

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