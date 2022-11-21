from fabrictestbed_extensions.fablib.fablib import FablibManager as fablib_manager
import os
import datetime

fablib = fablib_manager()
print("Initializing slice_builder_utils -", "FABLib Configuration")
fablib.show_config()

def get_slice_by_name_or_id(slice_name=None, slice_id=None):
    try:
        if slice_name is None and slice_id is None:
            slice = None
        elif slice_name is not None:
            slice = fablib.get_slice(name=slice_name)
        else:
            slice = fablib.get_slice(slice_id=slice_id)
        return slice
    except Exception as e:
        return None

# Slice Creation, Submission, Topology Save & Deletion
def create_slice(slice_name):
    slice = get_slice_by_name_or_id(slice_name)
    try:
        if not slice:
            slice = fablib.new_slice(slice_name)
            return slice
        print("Slice already submitted with the same name")
    except Exception as e:
        print("slice_builder_utils -", "Exception in Creating Slice:", slice_name, e)
        return None
    return slice

def submit_slice(slice, progress=True):
    try:
        print("slice_builder_utils -", "Submitting Slice:", slice.get_name())
        slice.submit(progress=progress)
    except Exception as e:
        print("slice_builder_utils -", "Exception in Submitting Slice:", slice.get_name(), e)

def save_slice_topology(slice, file_path):
    try:
        slice.save(file_path)
        print("slice_builder_utils -", "Slice Topology Saved Successfully:", slice.get_name(), "Path:", file_path)
    except Exception as e:
        print("slice_builder_utils -", "Exception in Saving Slice Topology:", slice.get_name(), e)
    
def delete_slice(slice):
    try:
        slice.delete()
        print("slice_builder_utils -", "Deleted Slice Successfully:", slice.get_name())
    except Exception as e:
        print("slice_builder_utils -", "Exception in Deleting Slice:", slice.get_name(), e)

def extend_slice_lease(slice_name, days):
    try:
        end_date = (datetime.datetime.now().astimezone() + datetime.timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S %z")
        lease_slice = get_slice_by_name_or_id(slice_name=slice_name)
        lease_slice.renew(end_date)
        print("slice_builder_utils -", "New Lease End Date for Slice:", slice_name, "is", end_date)
    except Exception as e:
        print("slice_builder_utils -", "Error in Renewing Slice Lease for Slice:", slice_name, "error:", e)

        
def get_slice_interfaces(slice):
    nodes = slice.get_nodes()
    interfaces = []
    for node in nodes:
        interfaces += node.get_interfaces()
    return interfaces
