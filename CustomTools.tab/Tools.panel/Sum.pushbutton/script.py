# -*- coding: utf-8 -*-
from collections import namedtuple
# from customcollections import DefaultOrderedDict

from pyrevit import revit, DB, HOST_APP
from pyrevit import forms
from pyrevit import script
from pyrevit.coreutils import pyutils
from customOutput import file_name_getter, ct_icon


__context__ = 'selection'
__doc__ = '''Sums up the values of selected numerical parameter on selected elements.
Sum is calculated for every Type and overall.

NEW:
Count of elements per type is also available.'''
__title__ = 'Sum\nParameters'
__helpurl__ = 'https://youtu.be/aWg-rj8k0Ts'
__highlight__ = 'updated'


selection = revit.get_selection()

logger = script.get_logger()
output = script.get_output()
# changing icon
ct_icon(output)

ParamDef = namedtuple('ParamDef', ['name', 'type', 'readableTypeName'])


def is_calculable_param(param):
    if param.StorageType == DB.StorageType.Double:
        return True

    if param.StorageType == DB.StorageType.Integer:
        val_str = param.AsValueString()
        if val_str and unicode(val_str).lower().isdigit():
            return True

    return False

def get_definition_type(definition):
    if HOST_APP.is_newer_than(2022):
        return definition.GetDataType()
    else:
        return definition.ParameterType

def get_definition_readableTypeName(definition):
    if HOST_APP.is_newer_than(2022):
        return DB.LabelUtils.GetLabelForSpec(definition.GetDataType())
    else:
        return definition.ParameterType


def calc_param_total(element_list, param_name):
    sum_total = 0.0

    def _add_total(total, param):
        if param.StorageType == DB.StorageType.Double:
            total += param.AsDouble()
        elif param.StorageType == DB.StorageType.Integer:
            total += param.AsInteger()

        return total

    for el in element_list:
        param = el.LookupParameter(param_name)
        if not param:
            el_type = revit.doc.GetElement(el.GetTypeId())
            type_param = el_type.LookupParameter(param_name)
            if not type_param:
                logger.error('Elemend with ID: {} '
                             'does not have parameter: {}.'.format(el.Id,
                                                                   param_name))
            else:
                sum_total = _add_total(sum_total, type_param)
        else:
            sum_total = _add_total(sum_total, param)

    return sum_total


def format_length(total):
    # return ('{} m'.format(total/3.28084))
    # always 3 decimal places coverted to meters
    return ("{:.3f} m".format(total/3.28084))


def format_area(total):
    # return ('{} m2'.format(total/10.7639))
    # always 3 decimal places coverted to square meters
    return ("{:.3f} m2".format(total/10.7639))


def format_volume(total):
    # return ('{} m3'.format(total/35.3147))
    # always 3 decimal places coverted to cubic meters
    return ("{:.3f} m3".format(total/35.3147))

if HOST_APP.is_newer_than(2022):
    formatter_funcs = {DB.SpecTypeId.Length: format_length,
                   DB.SpecTypeId.Area: format_area,
                   DB.SpecTypeId.Volume: format_volume}
else:
    formatter_funcs = {DB.ParameterType.Length: format_length,
                   DB.ParameterType.Area: format_area,
                   DB.ParameterType.Volume: format_volume}


def process_options(element_list):
    # find all relevant parameters
    param_sets = []

    for el in element_list:
        shared_params = set()
        # find element parameters
        for param in el.ParametersMap:
            if is_calculable_param(param):
                pdef = param.Definition
                shared_params.add(ParamDef(pdef.Name,
                                           get_definition_type(pdef),
                                           get_definition_readableTypeName(pdef)))

        # find element type parameters
        el_type = revit.doc.GetElement(el.GetTypeId())
        if el_type and el_type.Id != DB.ElementId.InvalidElementId:
            for type_param in el_type.ParametersMap:
                if is_calculable_param(type_param):
                    pdef = type_param.Definition
                    shared_params.add(ParamDef(pdef.Name,
                                               get_definition_type(pdef),
                                               get_definition_readableTypeName(pdef)))

        param_sets.append(shared_params)

    # make a list of options from discovered parameters
    if param_sets:
        all_shared_params = param_sets[0]
        for param_set in param_sets[1:]:
            all_shared_params = all_shared_params.intersection(param_set)

        return {'{} <{}>'.format(x.name, x.readableTypeName): x
                for x in all_shared_params}


def process_sets(element_list):
    # el_sets = DefaultOrderedDict(list)
    el_sets = pyutils.DefaultOrderedDict(list)

    # separate elements into sets based on their type
    for el in element_list:
        if hasattr(el, 'LineStyle'):
            el_sets[el.LineStyle.Name].append(el)
        else:
            eltype = revit.doc.GetElement(el.GetTypeId())
            if eltype:
                el_sets[revit.query.get_name(eltype)].append(el)
            # deprecated
            # wrapped_eltype = revit.ElementWrapper(eltype)
            # el_sets[wrapped_eltype.name].append(el)
    # add all elements as last set, for totals of all elements
    el_sets['SPOLU'].extend(element_list)

    return el_sets


# main -----------------------------------------------------------------------
# ask user to select an option
options = process_options(selection.elements)
# adding option "Count" which is not proper parameter - count of elements
options["Count"] = "count"

if options:
    selected_switch = \
        forms.CommandSwitchWindow.show(sorted(options),
                                       message='Select parameter:')

    # Calculating totals for each set and printing results

    if selected_switch:
        selected_option = options[selected_switch]
        if selected_option:
            # just if selected "Count" option which is not proper parameter
            if selected_option == "count":
                output.print_md("##{}".format("Count"))
                output.print_md("### " + file_name_getter(revit.doc))
                md_schedule = "| Family Type | Parameter Value |\n| ----------- | ----------- |"
                for type_name, element_set in process_sets(selection.elements).items():
                    type_name = type_name.replace('<', '&lt;').replace('>', '&gt;')
                    total_value = len(element_set)
                    if type_name == "SPOLU":
                        strongTag1 = "<span style='color:darkorange'>**"
                        strongTag2 = "**</span>"  
                    else:
                        strongTag1 = strongTag2 = ""
                    newScheduleLine = " \n| "+ strongTag1 + type_name + strongTag2 +" | "+ strongTag1 +str(total_value) + strongTag2 +" |"
                    md_schedule += newScheduleLine
            # if selected option is proper parameter
            else:
                output.print_md("##{}".format(selected_option.name))
                output.print_md("### " + file_name_getter(revit.doc))
                md_schedule = "| Family Type | Parameter Value |\n| ----------- | ----------- |"
                for type_name, element_set in process_sets(selection.elements).items():
                    type_name = type_name.replace('<', '&lt;').replace('>', '&gt;')
                    total_value = calc_param_total(element_set, selected_option.name)
                    if type_name == "SPOLU":
                        strongTag1 = "<span style='color:darkorange'>**"
                        strongTag2 = "**</span>"  
                    else:
                        strongTag1 = strongTag2 = ""
                    if selected_option.type in formatter_funcs.keys():
                        newScheduleLine = " \n| "+ strongTag1 + type_name + strongTag2 +" | "+ strongTag1 +formatter_funcs[selected_option.type](total_value) + strongTag2 +" |"
                    else:
                        newScheduleLine = " \n| "+ strongTag1 + type_name + strongTag2 +" | "+ strongTag1 +str(total_value) + strongTag2 +" |"
                    md_schedule += newScheduleLine
            # print md_schedule
            output.print_md(md_schedule)

# change to proper schedule
# data = [['结构', '结构', '结构结构', 80],
#         ['结构', '结构', '结构', 45],
#         ['row3', 'data', 'data', 45],
#         ['结构结构', 'data', '结构', 45]]

# # formats contains formatting strings for each column
# # last_line_style contains css styling code for the last line
# output.print_table(table_data=data,
#                    title="Example Table",
#                    columns=["Row Name", "Column 1", "Column 2", "Percentage"],
#                    formats=['', '', '', '{}%'],
#                    last_line_style='color:red;')