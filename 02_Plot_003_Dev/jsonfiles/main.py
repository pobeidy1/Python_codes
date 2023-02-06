# -*- coding: utf-8 -*-
"""
Created on Sun Dec 19 21:24:26 2021

@author: pobe4699
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 14:11:44 2021

@author: pobe4699

"""
import jsons


from libs.load_json_func import *

data = loadDataFile("input/workspaces-SMG.json")

#Loop along dictionary keys
for key in data:
    print(key, ":", data[key])


measurment1 = []
for instance in data:
    selectInstance = False if "tag_strings" not in instance or \
                              not instance["tag_strings"] else True
    for tag in tags:
        try:
            if tag not in instance["tag_strings"].keys():
                selectInstance = False
                break
        except KeyError as keyerr:
            print(f"WARNING: {instance} does not have tag_strings")
            break
    if selectInstance:
        studyIdsOfInterest.append(instance["study_id"])

return studyIdsOfInterest




# It's a list of records. Process them one by one.
    for workspace in data:

        # Try and find a matching annotator first. This ID appears to be the first
        # part of the "current_compute_id"...
        # oid = workspace["studyIds"]
        oid = workspace["current_compute_id"].split("-")[0]
        if oid not in oidStudyDataMap.keys():
            continue

        flow_measurements = workspace.get("flow-measurements", None)

        # Not all records have "flow-measurements", skip the ones that don't.
        if flow_measurements is None:
            continue

        # The datapoint we will populate with flow data, matched to a study_id
        # and an annotator (which we get from the previously constructed dictionary).
        point = {}

        # The flow measurements are a dictionary, the keys are number or maybe
        # they are an ID? Just using the values for now...
        for flow_measurement in flow_measurements.values():

            # What this set of measurement represents.
            display_name = flow_measurement["display_name"].lower()

            # Some records are empty or incomplete in some way. It looks like
            # measurements that are empty/default are called Measurements #XX
            if display_name.startswith("measurement"):
                continue

            # Skip if we can't find the flow/beat data.
            if flow_measurement.get("average_positive_flow_beat", None) is None:
                continue

            # Add the positive/negative forward/reverse flow/beat data to the datapoint.
            point[f"{display_name}_forward_flow"] = flow_measurement["average_positive_flow_beat"]
            point[f"{display_name}_reverse_flow"] = flow_measurement["average_negative_flow_beat"]

            # To get the max/min flow velocity it looks like we need to read them
            # from the chart data. This is in the "flow_measurements" part of
            # the data, not "flow-measurements".
            flow_measurement = flow_measurement.get("flow_measurements", None)

            if flow_measurement is None:
                continue

            # Loop through the values in the chart area, and update with the max/min
            # points for "peak_speed".
            maximum = flow_measurement["measurements"][0]
            minimum = flow_measurement["measurements"][0]

            for measurement in flow_measurement["measurements"][1:]:

                # Here we are finding the max/min peak_speed, but there are other
                # values in this area too:
                #
                #   'area', 'center', 'center_of_negative_flow',
                #   'center_of_positive_flow', 'circumference', 'complex_polygon',
                #   'diameter', 'flow', 'flow_center', 'flow_eccentricity',
                #   'flow_jet_angle', 'forward_flow', 'mean_flow_direction',
                #   'normal', 'peak_speed', 'peak_speed_95_percentile',
                #   'regurgitant_fraction', 'reverse_flow', 'wss_mean', 'wss_peak',
                #   'wss_values'

                if measurement["peak_speed"] > maximum["peak_speed"]:
                    maximum = measurement

                if measurement["reverse_flow"] < minimum["peak_speed"]:
                    minimum = measurement


            # Add the velocity data to the datapoint
            point[f"{display_name}_maximum_speed"] = maximum["peak_speed"]
            point[f"{display_name}_minimum_speed"] = minimum["peak_speed"]
            # Add the annotator info and the study_id to the datapoint.
            # point["annotator"] = annotator
            point["study_id"] = oid
            point["study_instance_uid"] = oidStudyDataMap[oid]["study_instance_uid"]
            point["stilid"] = oidStudyDataMap[oid]["stilid"]

        # If we couldn't find any data to add to the datapoint, skip.
        if len(point) > 5:
            data.append(point)