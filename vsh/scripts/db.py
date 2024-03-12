#!/usr/bin/env python3

from pymatgen.io.vasp.outputs import Vasprun
import json
import hashlib
import time
import gzip

def parse_vasprun_file(file_path: str, **parse_kwargs) -> dict:
    """
    Parse the Vasprun file and return the results as a dictionary.

    Parameters:
        file_path (str): Path to the Vasprun file.
        parse_kwargs (dict): Additional keyword arguments for Vasprun parsing.

    Returns:
        dict: Parsed results as a dictionary.
    """
    try:
        return Vasprun(file_path, **parse_kwargs).as_dict()
    except Exception as e:
        print(f"Error parsing Vasprun file: {e}")
        return {}

def calculate_hashes(data: dict) -> dict:
    """
    Calculate MD5 hashes for INCAR, KPOINTS, and POSCAR.

    Parameters:
        data (dict): Dictionary containing INCAR, KPOINTS, and POSCAR data.

    Returns:
        dict: Dictionary containing MD5 hashes for INCAR, KPOINTS, and POSCAR.
    """
    hashes = {}
    for key, value in data['input'].items():
        hashes[f"{key}_hash"] = hashlib.md5(json.dumps(value).encode()).hexdigest()
    return hashes

def update_dict_with_hashes(data: dict, hashes: dict) -> dict:
    """
    Update the dictionary with MD5 hashes.

    Parameters:
        data (dict): Original dictionary.
        hashes (dict): Dictionary containing MD5 hashes.

    Returns:
        dict: Updated dictionary.
    """
    input_data = data.get('input', {})

    for key, value in hashes.items():
        target_key = key.replace('_hash', '')
        if target_key in input_data and isinstance(input_data[target_key], dict):
            input_data[target_key]['hash'] = value

    return data

def update_dict_with_time(data: dict) -> dict:
    """
    Update the dictionary with the current time.

    Parameters:
        data (dict): Original dictionary.

    Returns:
        dict: Updated dictionary.
    """
    data['time'] = time.time()
    return data

def write_to_file(data: dict, file_path: str):
    """
    Serialize and compress dictionary data, then write to a file.

    Parameters:
        data (dict): Dictionary to be written.
        file_path (str): Output file path.
    """
    serialized_data = json.dumps(data, indent=4)
    compressed_data = gzip.compress(serialized_data.encode('utf-8'))
    
    with open(file_path, 'wb') as f:
        f.write(compressed_data)

def save_vasprun_to_file(args):

    results_dict = parse_vasprun_file(args.input, parse_dos=args.dos, parse_eigen=args.eigen, parse_projected_eigen=args.projected_eigen, parse_potcar_file=args.potcar)
    
    if results_dict:
        hashes = calculate_hashes(results_dict)
        results_dict = update_dict_with_hashes(results_dict, hashes)
        results_dict = update_dict_with_time(results_dict)
        write_to_file(results_dict, args.output)

def summarize_vasprun(args):
    """Summarizes either vasprun.xml or vasprun.tgz file."""

    #try tgz first
    try:
        with gzip.open(args.input, 'rb') as f:
            results_dict = json.loads(f.read().decode('utf-8'))
    except OSError:
        results_dict = parse_vasprun_file(args.input, parse_dos=args.dos, parse_eigen=args.eigen, parse_projected_eigen=args.projected_eigen, parse_potcar_file=args.potcar)
    except Exception as e:
        print(f"Error summarizing Vasprun file: {e}")
    
    #print time, convergence, and formula
    print(f"Time: {results_dict['time']}")
    print(f"Formula: {results_dict['output']['final_structure']['composition']['reduced_formula']}")
    print(f"Converged: {results_dict['converged']}")


def run(args):

    functions = {
        'save': save_vasprun_to_file,
        'summarize': summarize_vasprun
    }

    for arg, func in functions.items():
        if getattr(args, arg):
            func(args)




