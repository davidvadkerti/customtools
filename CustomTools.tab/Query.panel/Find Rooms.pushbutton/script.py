# -*- coding: utf-8 -*-
from pyrevit import DB, forms, script
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory, BuiltInParameter

from pyrevit.coreutils import Timer
from customOutput import hmsTimer
from customOutput import ct_icon

# change context for proper category - check in revit for category
__context__ = 'Selection'

doc = __revit__.ActiveUIDocument.Document
room_collector = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms) \
                .WhereElementIsNotElementType().ToElements()

# /////// UI WINDOW /////////
class findRoomWindow(forms.WPFWindow):
    def __init__(self, xaml_file_name):
        forms.WPFWindow.__init__(self, xaml_file_name)

    def process_text(self, sender, args):
        self.Close()
        name_RB = self.SearchByName.IsChecked
        number_RB = self.SearchByNumber.IsChecked
        # setting the searching parameter
        if number_RB:
            search_param = 0
        else:
            search_param = 1

        timer = Timer()
        output = script.get_output()
        output.set_width(400)
        # changing icon
        ct_icon(output)

        find_string =  self.sheets_tb.Text.lower()
        # getting the room data
        schedule_data = []
        for room in room_collector:
            room_id = room.Id
            room_name = room.get_Parameter(DB.BuiltInParameter.ROOM_NAME).AsString()
            room_number = room.get_Parameter(DB.BuiltInParameter.ROOM_NUMBER).AsString()
            room_level = room.Level.Name

            paramList = [
                room_number,
                room_name,
                output.linkify(room_id),
                room_level]

            # finding string in lowercase version of room name
            if find_string in paramList[search_param].lower():
                schedule_data.append(paramList)

        sorted_schedule_data = sorted(schedule_data, key=lambda x: x[search_param].lower())
        # printing the schedule if there are data
        if sorted_schedule_data:
            output.print_table(table_data=sorted_schedule_data,
                               title = "Rooms",
                               columns=["Number", "Name", "ID", "Level"],
                               formats=['', '', '', ''])
        # if there are no data print status claim
        else:
            print("There is no such a Room.")
        # for timing------
        endtime = timer.get_time()
        print(hmsTimer(endtime))        




findRoomWindow('findRoomWindow.xaml').ShowDialog()