#!/usr/bin/env python3
import argparse
import json
import os

import toml

__title__ = "pipsync"
__version__ = "0.1.0"
__author__ = "Bryson Tyrrell"
__author_email__ = "bryson.tyrrell@gmail.com"
__license__ = "MIT"
__copyright__ = "Copyright 2020 Bryson Tyrrell"
__description__ = "Sync requirements.txt files with Pipfile.lock"


def arguments():
    parser = argparse.ArgumentParser(prog="pipsync", description=__description__)
    parser.add_argument("PATH", help="Pipfile.lock location")
    parser.add_argument(
        "-x",
        "--exclude",
        action="append",
        default=[],
        help="Exclude top level directories from requirements.txt file search",
    )
    parsed_args = parser.parse_args()

    if parsed_args.PATH.endswith("Pipfile.lock"):
        parsed_args.DIR = os.path.dirname(parsed_args.PATH)
    else:
        if not os.path.isfile(os.path.join(parsed_args.PATH, "Pipfile.lock")):
            print("Pipfile.lock not found at given path")
            raise SystemExit(1)
        else:
            parsed_args.DIR = parsed_args.PATH

    if parsed_args.exclude:
        parsed_args.exclude = [
            os.path.join(parsed_args.DIR, d) for d in parsed_args.exclude
        ]

    return parsed_args


def find_requirements_files(root_dir: str, exclude: list):
    file_list = list()

    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [
            d
            for d in dirs
            if os.path.join(root, d) not in exclude and not d.startswith(".")
        ]
        for file in files:
            if file.lower() == "requirements.txt":
                file_list.append(os.path.join(root, file))

    return file_list


def get_pipfile_packages(base_dir):
    pipfile = toml.load(os.path.join(base_dir, "Pipfile"))

    with open(os.path.join(base_dir, "Pipfile.lock"), "r") as f:
        pipfile_lock = json.load(f)

    values = dict()

    for r in pipfile_lock["default"].keys():
        if r in pipfile["packages"].keys():
            # Git installed packages will not have version values
            version = pipfile_lock["default"][r].get("version")

            if not version:
                git_url = pipfile_lock["default"][r].get("git")
                if git_url:
                    values[r] = {"pip": f"git+{git_url}#egg={r}"}
            else:
                values[r] = {"pip": f"{r}{version}"}

    return values


def parse_requirements(file_path):
    with open(file_path, "r") as rf:
        requirements_raw = rf.read().splitlines()
    requirements = {}
    for line in requirements_raw:
        try:
            name = line.split("==")[0]
        except IndexError:
            continue
        requirements[name] = {"pip": line}
    return requirements


def write_requirements(pipfile_packages, requirements_packages, file_path):
    # TODO: DO NOT REMOVE PACKAGES THAT ARE NOT IN PIPFILE?
    matched_requirements = set([i.lower() for i in pipfile_packages.keys()]) & set(
        [i.lower() for i in requirements_packages.keys()]
    )

    if matched_requirements:
        with open(file_path, "w") as f:
            for package in sorted(matched_requirements):
                f.write(pipfile_packages[package]["pip"] + "\n")

        return matched_requirements

    else:
        return None


def main():
    args = arguments()
    print(args)

    requirements_files = find_requirements_files(args.DIR, args.exclude)

    pipfile_packages = get_pipfile_packages(args.DIR)

    for file in requirements_files:
        print(file)
        write_requirements(pipfile_packages, parse_requirements(file), file)


if __name__ == "__main__":
    main()
