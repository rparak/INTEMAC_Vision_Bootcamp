# OS module for file handling and accessing directories
import os

# PyYAML library for reading and writing YAML files
import yaml

# Numpy for numerical operations and handling arrays
import numpy as np

# Pickle (Python object serialization)
import pickle as pkl

def Get_Full_Path(camera_stand_name, dataset_name):
    """
    Description:
        Construct the full absolute path to the dataset.

    Args:
        (1) camera_stand_name [string]: The name of the camera stand.
        (2) dataset_name [string]: The name of the dataset.

    Returns:
        (1) parameter [string]: The full path to the dataset.
    """

    # Define dataset path (relative)
    file_path = os.path.join('..', 'Data', camera_stand_name, dataset_name)
    
    # Get absolute full path (cross-platform)
    return os.path.abspath(file_path)

def Update_Yaml(config_file, full_path):
    """
    Description:
        Update the path in the YAML configuration file.

    Args:
        (1) config_file [string]: Path to the configuration YAML file.
        (2) full_path [string]: The full dataset path to update in the YAML file.
    """

    # Load the YAML file
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    
    # Modify the YAML content
    config['path'] = full_path
    
    # Write back to YAML file
    with open(config_file, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
    
    print(f'YAML file <{config_file}> successfully updated and saved.')

def Load_Data(file_path, format, separator):
    """
    Description:
        A simple function to read data from the file.

        Note:
            Deserialization of the data into a binary / text file.

    Args:
        (1) file_path [string]: The specified path of the file without extension (format).
        (2) format [string]: The format of the loaded file.
                             Note:
                                'pkl' : Pickle file; 'txt' : Text file
        (3) separator [string]: Separator between data.

    Returns:
        (1) parameter [Dictionary of different types of data <float, bool, etc.>]: Loaded data from a binary file.
    """

    if format == 'pkl':
        # Open the file in 'rb' mode (read binary). 
        with open(file_path + f'.{format}', 'rb') as f:
            # Load the data from the file using the file object (f).
            data = pkl.load(f)

    elif format == 'txt':
        data_tmp = []
        with open(file_path + f'.{format}', 'r') as f:
            # Read the line of the file in the current step.
            for line in f:
                # Splits a string into a list with the specified delimiter (,) 
                # and converts to a float.
                data_tmp.append(np.float64(line.split(separator)))

        # Convert a list to an array.
        data = np.array(data_tmp, dtype=np.float64)
    
    # Close the file after loading the data.
    f.close()

    return data

def Save_Data(file_path: str, data, format, separator):
    """
    Description:
        A simple function to write data to the file.

        Note:
            Serialization of the data into a binary / text file.

    Args:
        (1) file_path [string]: The specified path of the file without extension (format).
        (2) data [Dictionary of different types of data <float, bool, etc.>]: Individual data.
        (3) format [string]: The format of the saved file.
                             Note:
                                'pkl' : Pickle file; 'txt' : Text file.
        (3) separator [string]: Separator between data.
    """
    
    if format == 'pkl':
        # Open the file in 'wb' mode (write binary). 
        with open(file_path + f'.{format}', 'wb') as f:
            # Write the input data to a file using the file object (f).
            pkl.dump(data, f)
    elif format == 'txt':
        with open(file_path + f'.{format}', 'a+') as f:
            # Write the data to the file.
            for data_i in data[:-1]:
                f.writelines([str(data_i), separator])
            f.writelines([str(data[-1]), '\n'])

    # Close the file after writing the data.
    f.close()