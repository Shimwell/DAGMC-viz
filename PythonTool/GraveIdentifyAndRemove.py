import argparse
import numpy as np
from pymoab import core, types, tag
from pymoab.types import MBENTITYSET


def parse_arguments():
    """
    Parse the argument list and return
    an input file location and optional output file name.

    Input:
    ______
       none

    Returns:
    ________
       args: Namespace
           User supplied input file location and optional output file name.
    """

    parser = argparse.ArgumentParser(description="Remove graveyard from an h5m data file.")

    parser.add_argument("h5mfile",
                        type=str,
                        help='provide a path to the h5m data file'
                        )
    parser.add_argument("-o", "--outputfile",
                        type=str,
                        help='provide a name and extension for the output file'
                        )

    args = parser.parse_args()

    return args


def remove_graveyard(input_file, output_file = None):
    """
    Remove the graveyard volume EntitySet from the data file and write the
    result out to disk with a default input name or specified output name.

    If the user has specified an output file name and extension, use this to
    write the file. If they haven't, append "_no_grave" onto the name of the
    input file and add the .h5m extension.

    Input:
    ______
       input_file: str
           User supplied data file location.
       output_file: str
           Optional user supplied output file name and extension.

    Returns:
    ________
       none
    """

    mb = core.Core()

    # Read the data file with the graveyard to be removed.
    mb.load_file(input_file)

    tag_name = mb.tag_get_handle("NAME")
    tag_category = mb.tag_get_handle("CATEGORY")
    root = mb.get_root_set()

    # An array of tag values to be matched for entities returned by the following call.
    group_tag_values = np.array(["Group"])

    # Retrieve all EntitySets with a Category tag with the value of "Group".
    group_categories = list(mb.get_entities_by_type_and_tag(root, MBENTITYSET,
                                                            tag_category, group_tag_values))

    # Retrieve all EntitySets with a Name tag.
    group_names = mb.tag_get_data(tag_name, group_categories, flat=True)

    # Find the EntitySet whose Name tag value contains "graveyard".
    substring = "graveyard"
    graveyard_sets = [group_set for group_set, name in zip(group_categories, group_names)
                      if substring in str(name.lower())]

    # Warn the user if there was more than one EntitySet with the "graveyard" Name tag value.
    if len(graveyard_sets) > 1:
        print("WARNING: More than one graveyard set found.")

    # Warn the user if the file they provided did not contain a graveyard.
    if len(graveyard_sets) < 1:
        print("WARNING: This file did not contain a graveyard.")
        exit()

    # Print the EntityHandle of the EntitySet(s) with the "graveyard" Name tag value.
    print(graveyard_sets)

    # Remove the graveyard EntitySet from the data.
    groups_to_write = [group_set for group_set in group_categories
                       if group_set not in graveyard_sets]

    """
    Check if the user specified an output file name.
    If so, write the file with that name. If not, append onto
    the original input file name to indicate the graveyard has been removed.
    """

    if output_file is not None:
        mb.write_file(output_file, output_sets=groups_to_write)
    else:
        input_array = input_file.split("/")
        input_file = input_array[-1]
        base_file_name = input_file[:-4]
        mb.write_file(base_file_name + "_no_grave.h5m", output_sets=groups_to_write)


def main():

    # Parse arguments.
    args = parse_arguments()

    # Remove the graveyard from the data file.
    remove_graveyard(args.h5mfile, args.outputfile)

if __name__ == "__main__":
    main()
