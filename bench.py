#!/usr/bin/env python3

import logging
import os
import argparse

def load_output_path(prefix):
    return f"{prefix}.load_results"

def run_output_path(prefix):
    return f"{prefix}.run_results"

def bench(workload, records, operations, directory, prefix):
    load_config = {
        "rocksdb.dir": directory,
        "recordcount": records,
        "operations":  operations,
        "measurementtype": "hdrhistogram",
        "exportfile": load_output_path(prefix)
    }

    load_flags = " ".join(map(lambda item: f"-p {item[0]}={item[1]}", load_config.items()))
    load_cmd = f"bin/ycsb load rocksdb -s -P {workload} {load_flags}"

    run_config = {
        "rocksdb.dir": directory,
        "recordcount": records,
        "operations":  operations,
        "measurementtype": "hdrhistogram",
        "exportfile": run_output_path(prefix)
    }

    run_flags = " ".join(map(lambda item: f"-p {item[0]}={item[1]}", run_config.items()))
    run_cmd = f"bin/ycsb run rocksdb -s -P {workload} {run_flags}"

    logging.info(f"{workload}: loading {records} records, {operations} operations")
    if os.system(load_cmd) != 0:
        logging.error(f"{workload}: loading failed")
        return
    else:
        logging.info(f"{workload}: successfully loaded")

    logging.info(f"{workload}: running")
    if os.system(run_cmd) != 0:
        logging.error(f"{workload}: running failed")
    else:
        logging.info(f"{workload}: successfully ran")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-r", "--records",
        default=1_000_000,
        help="number of records to insert [default: 1_000_000]"
    )
    parser.add_argument(
        "-n", "--operations",
        default=1_000_000,
        help="number of operations to perform [default: 1_000_000]"
    )
    parser.add_argument(
        "-o", "--output",
        default="",
        help="prefix of files to output results to [default: basename of workload]"
    )
    parser.add_argument(
        "workload",
        help="the workload to run"
    )
    parser.add_argument(
        "directory",
        help="the directory to store to"
    )
    args = parser.parse_args()

    if not args.output:
        args.output = os.path.basename(args.workload)

    bench(
        args.workload,
        args.records,
        args.operations,
        args.directory,
        args.output
    )

if __name__ == "__main__":
    main()
