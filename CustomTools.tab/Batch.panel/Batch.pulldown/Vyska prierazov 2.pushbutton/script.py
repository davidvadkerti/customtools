#!/usr/bin/env python
# -*- coding: utf-8 -*-

__title__ = 'Výška a označenie\nprierazov V2'
__doc__ = """Sets distance of Sill Height of Windows from Project zero to parameter "SH prierazu".
Sets Level number to parameter "Poschodie" to Windows and Generic Models
Sets Level elevation to parameter "ref od 0" to Windows.
Sets Mark to Windows and Generic Models in xxx format f.e. 001

Only Windows and Generic Models with Type Comments == "stavebne upravy" are processed.
You need to add theese Shared Parameters: Poschodie, SH prierazu, Offset Shared, Priemer, ref od 0."""

__helpurl__ = "https://youtu.be/2LBi9p3gPiY"

# for timing------
from pyrevit.coreutils import Timer
from pyrevit import coreutils, forms
from customOutput import hmsTimer, ct_icon
timer = Timer()
# ----------------

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, \
                Transaction, Document, BuiltInParameter
from pyrevit import revit, DB
from pyrevit import script

doc = __revit__.ActiveUIDocument.Document


# dialog
dialog = forms.alert("Pozor toto je WIP skript.\nChceš naozaj prepísať všetky prierazy? ",
                  ok=False, yes=True, no=True)
if dialog:
    # /////// COLLECTORS /////////
    # collecting windows
    windows_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Windows) \
        .WhereElementIsNotElementType() \
        .ToElements()

    # collecting generic models
    genericModel_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_GenericModel) \
        .WhereElementIsNotElementType() \
        .ToElements()

    output = script.get_output()
    # changing icon
    ct_icon(output)

    # /////// GLOBAL VARIABLES /////////
    unique_types = [] # unique specifications of openings (e.g. ['-2', 'ZT', ['wc', 350, '30']])
    list_starts = [] # list of specialist + level (e.g. VZ01), numbering sequence starts here over and over
    sqc_number_list = [] # list of just last used numbers for each specialist + level
    unique_types_nums = [] # list of all numbers for each opening type

    # /////// FUNCTIONS /////////
    #converts feets to milimeters and makes rounded integer from the result
    def feet2mm(a):
        b = a/0.00328084
        return int(round(b))

    # highlights text using html string with css
    def text_highligter(a):
            content = str(a)
            html_code = "<p class='elementlink'>"+content+"</p>"
            return coreutils.prepare_html_str(html_code)

    # error handling
    def skipped(element,parameterName):
        # notprocessed.append(element.Id.IntegerValue)
        # notprocessed.append(element.Id)
        elemID = element.Id
        elemName = element.Name
        paramList = [output.linkify(elemID), elemName]
        # paramList = [elemID, elemName]
        notprocessed.append(paramList)

        parameter = element.LookupParameter(parameterName)
        if parameter:
            parameter.Set("no data")

    # adding leading zeros to one digit numbers
    def zerosNum(a):
        if a < 10 and a > 0:
            a = "0"+str(a)
        # elif a < 100:
        #     a = "0"+str(a)
        return str(a)

    def poschodieSetter(element,levelElement):
        elementTypeId = element.GetTypeId()
        elementType = Document.GetElement(doc,elementTypeId)
        # filtering elements
        # filterp = elementType.LookupParameter('Type Comments')
        filterp = elementType.get_Parameter(DB.BuiltInParameter.ALL_MODEL_TYPE_COMMENTS)
        if filterp and filterp.AsString() == "stavebne upravy":
            try:
                # setting parameters
                # getting the levelCode string from Levels
                levelCode = levelElement.LookupParameter("Poschodie").AsString()
                # setting parameter "Poschodie" for openings
                levelNameP = element.LookupParameter("Poschodie")
                if levelNameP:
                        levelNameP.Set(levelCode)
                else:
                    skipped(element,"Poschodie")
            except:
                skipped(element,"Poschodie")

    # numbers openings by type, every new type will have new number
    # atributes names:
    # circular: diameter name, circular mark f.e. "wc"
    # rectangular: width, height or depth, rectangular mark f.e. "wr"
    def markSetter(element,DiameterName,CircularMark,WidthName,HeightDepthName,RectMark):
    # # filter by Type Comments == stavebne upravy
        elementTypeId = element.GetTypeId()
        elementType = Document.GetElement(doc,elementTypeId)
        # filterp = elementType.LookupParameter('Type Comments')
        filterp = elementType.get_Parameter(DB.BuiltInParameter.ALL_MODEL_TYPE_COMMENTS)

        if filterp and filterp.AsString() == "stavebne upravy":
            # setting Mark values
            try:
                try:
                    # circular windows
                    diameter_param = element.LookupParameter(DiameterName).AsDouble()
                    # print("diameter = " +str(diameter_param))
                    diameterValue = feet2mm(diameter_param)
                    fire_rating = element.LookupParameter("Fire_Rating").AsString()
                    spclst = element.LookupParameter("Profesia").AsString()
                    level = element.LookupParameter("Poschodie").AsString()
                    # wc = wall circular
                    # opening specs
                    opng = [level, spclst, [CircularMark, diameterValue, fire_rating]]
                    # seting dimension parameter "Rozmer", e.g. "Ø400"
                    dim_param = element.LookupParameter("Rozmer")
                    dim_param_value = "Ø" + str(diameterValue)
                    dim_param.Set(dim_param_value)
                except:
                    # rectangular windows
                    width_param = element.LookupParameter(WidthName).AsDouble()
                    heightDepth_param = element.LookupParameter(HeightDepthName).AsDouble()

                    widthValue = feet2mm(width_param)
                    heightDepthValue = feet2mm(heightDepth_param)
                    fire_rating = element.LookupParameter("Fire_Rating").AsString()
                    spclst = element.LookupParameter("Profesia").AsString()
                    level = element.LookupParameter("Poschodie").AsString()

                    # windows with Depth not equal with Wall width - niky
                    # not through the wall
                    try:
                        DepthName = "Hlbka"
                        depth_param = element.LookupParameter(DepthName).AsDouble()
                        depthValue = feet2mm(depth_param)

                        # RectMark >>> wr = wall rectengular
                        # opening specs
                        opng = [level, spclst, [RectMark, widthValue, heightDepthValue, fire_rating, depthValue]]
                        # seting dimension parameter "Rozmer", e.g. 400x700
                        dim_param = element.LookupParameter("Rozmer")
                        dim_param_value = str(widthValue) + "x" + str(heightDepthValue) + "x" + str(depthValue)
                        dim_param.Set(dim_param_value)

                    # standard rectangular windows - through the wall
                    except:    
                        # RectMark >>> wr = wall rectengular
                        # opening specs
                        opng = [level, spclst, [RectMark, widthValue, heightDepthValue, fire_rating]]
                        # seting dimension parameter "Rozmer", e.g. 400x700
                        dim_param = element.LookupParameter("Rozmer")
                        dim_param_value = str(widthValue) + "x" + str(heightDepthValue) 
                        dim_param.Set(dim_param_value)

                # sorting and numbering openings
                # prefix specialist + level, e.g. VZ01
                prefix = opng[1] + opng[0]
                # if specialist + level (e.g. VZ01) is not in the list
                if prefix not in list_starts:
                    unique_types.append(opng)
                    list_starts.append(prefix) # storing the prefix value in a list
                    sqc_number_list.append(1) # storing the last value in a list
                    # if is not value in list_starts it must start a new sequence
                    opng_num = 1 # hence opening number is 1
                    unique_types_nums.append(opng_num)
                # if specialist + level (e.g. VZ01) is already in the list
                else:
                    # search for index of the prefix in the list
                    prefix_index = list_starts.index(prefix)
                    # if this type of the opening is not in the list
                    if opng not in unique_types:
                        unique_types.append(opng) # storing the new opening specs in the list
                        sqc_number_list[prefix_index] += 1  # refreshing the last sequence number in the list
                        unique_types_nums.append(sqc_number_list[prefix_index])
                        opng_num = sqc_number_list[prefix_index]
                        # print("new")
                        # print(opng_num_index)
                    else:
                        opng_num_index = unique_types.index(opng)
                        opng_num = unique_types_nums[opng_num_index]
                        # print("used")
                        # print(opng_num_index)
                opng_id = zerosNum(opng_num)
                opng_mark = spclst + "." + level + "." + opng_id

                # setting the parameter values - just numbers
                opng_num_param = element.LookupParameter("Cislo Prierazu")
                # setting the parameter values - all opening id string
                opng_num_param.Set(opng_id)
                opng_mark_param = element.LookupParameter("Cislo Prvku")
                opng_mark_param.Set(opng_mark)
            except:
                pass

    # getting levels from generic models and other elements
    def GetLevel(item):
        #if hasattr(item, "LevelId"): return item.Document.GetElement(item.LevelId)
        if hasattr(item, "Level"): return item.Level
        elif hasattr(item, "GenLevel"): return item.GenLevel
        else:
            try: return item.Document.GetElement(item.get_Parameter(BuiltInParameter.INSTANCE_REFERENCE_LEVEL_PARAM).AsElementId())
            except: 
                try:
                    return item.Document.GetElement(item.get_Parameter(BuiltInParameter.INSTANCE_SCHEDULE_ONLY_LEVEL_PARAM).AsElementId())
                except:
                    pass

    t = Transaction(doc, "Vyska a oznacenie prierazov")
    t.Start()

    notprocessed = []
    # creating lists - just for debugging
    # sill_height_values_list=[]
    # sill_height_values_list=[]
    # level_ids_list=[]
    # level_elevation_list=[]
    # sill_height_zeroMM_list=[]
    # offset_shared_values_list=[]

    # creating lists - just for debugging
    # level_ids_list=[]
    # level_name_list=[]
    # indexlist=[]

    # /////// WINDOW SILL HEIGHT /////////
    # getting window parameters
    for window in windows_collector:
        # filter by Type Comments == stavebne upravy
        elementTypeId = window.GetTypeId()
        elementType = Document.GetElement(doc,elementTypeId)
        # filterp = elementType.LookupParameter('Type Comments')
        filterp = elementType.get_Parameter(DB.BuiltInParameter.ALL_MODEL_TYPE_COMMENTS)

        if filterp and filterp.AsString() == "stavebne upravy":
            try:
                try:
                    # hosted elements with Sill Height
                    # geting Sill Height from windows
                    # sillHeightFt = window.LookupParameter('Sill Height')
                    sillHeightFt = window.get_Parameter(DB.BuiltInParameter.INSTANCE_SILL_HEIGHT_PARAM)
                    sill_height_value = sillHeightFt.AsDouble()
                    # sill_height_values_list.append(feet2mm(sill_height_value))

                except:
                    # nonhosted elements with Offset Shared
                    # geting Offset Shared from windows
                    OffsetSharedFt = window.LookupParameter('Offset Shared')
                    offset_shared_value = OffsetSharedFt.AsDouble()
                    # offset_shared_values_list.append(feet2mm(offset_shared_value))

                # geting levels from windows
                level = window.LevelId
                # level_ids_list.append(level)

                # getting elevation of levels from project zero +0.000
                level_element = Document.GetElement(doc,level)
                level_elevation = level_element.Elevation
                # level_elevation_list.append(feet2mm(level_elevation))

                # write Level Height Values to "ref od 0" parameter of windows
                level_height_param = window.LookupParameter('ref od 0')
                if level_height_param:
                        level_height_param.Set(level_elevation)

                # add Level Height Values to Sill Height Values of windows
                try:
                    sill_height_zero = level_elevation + sill_height_value
                    # sill_height_zeroMM = round(feet2mm(sill_height_zero))
                    # sill_height_zeroMM_list.append(sill_height_zeroMM)
                except:
                    sill_height_zero = level_elevation + offset_shared_value

                # writing "SH prierazu" parameters
                custom_param = window.LookupParameter('SH prierazu')
                if custom_param:
                    custom_param.Set(sill_height_zero)

            except:
                # notprocessed.append(window.Id.IntegerValue)
                # custom_param = window.LookupParameter('SH prierazu')
                skipped(window,'SH prierazu')

    # /////// POSCHODIE PARAMETER ASIGNMENT /////////
    for window in windows_collector:
        try:
            level = window.LevelId
            levelElement = Document.GetElement(doc,level)
            # setting parameters
            poschodieSetter(window,levelElement)
        except:
            skipped(window,"Poschodie")

    for element in genericModel_collector:
        try:
            # Workplane based elements
            try:
                levelElement = GetLevel(element)
            # facebased elements
            except:
                level = element.LevelId
                levelElement = Document.GetElement(doc,level)
        #   setting parameters
            poschodieSetter(element,levelElement)
        except:
            skipped(element,"Poschodie")


    # /////// UNIQUE MARK PARAMETER ASIGNMENT /////////
    # Types of openings used in markSetter function, a is used as Mark sequence
    elementTypes = []
    a = 0
    for element in windows_collector:
        # setting Mark values - atributes are parameters names, wc = window circular
        markSetter(element,"Priemer","wc","Width","Height","wr")

    for element in genericModel_collector:
        # setting Mark values - atributes are parameters names, gmc = generic model circular
        markSetter(element,"Diameter","gmc","Width","Length","gmr")

    t.Commit()

    # just for debuging window sill height
    # print("control lists for debugging")
    # print(sill_height_values_list)
    # print(level_ids_list)
    # print(level_elevation_list)
    # print(sill_height_zeroMM_list)
    # print(offset_shared_values_list)

    # debuging poschodie
    # print(level_name_list)
    # print(indexlist)

    # Final Claims

    countOfSkippedElms = len(notprocessed)
    print(text_highligter(str(countOfSkippedElms) +" elements were skipped"))
    # print(notprocessed)
    if countOfSkippedElms>0:
        output.print_table(table_data = notprocessed,
                           title = "Skipped elements",
                           columns=["Element Id", "Name"],
                           formats=['', ''])

    # for timing------
    endtime = timer.get_time()
    print(hmsTimer(endtime))
    # endtimeRound = round(endtime*1000)/1000
    # print("\nTime "+str(endtimeRound)+" seconds.")
    # --------------