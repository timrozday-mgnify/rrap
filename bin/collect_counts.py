#!/usr/bin/env python3

import argparse
import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get numbers from fastp report")
    parser.add_argument(
        "--qc-json", dest="input_qc", help="Json from fastp QC", required=False
    )
    parser.add_argument(
        "--overlap-json",
        dest="fastp_overlap",
        help="Json from fastp overlap reads",
        required=False,
    )
    parser.add_argument(
        "--decontamination-counts",
        dest="decontamination_overlap",
        help="Counts from decontamination output files",
        required=False,
    )
    parser.add_argument(
        "--overlap-counts",
        dest="seqprep_overlap",
        help="Counts from SeqPrep output files",
        required=False,
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        help="output with stats",
        required=False,
        default="output.txt",
    )

    args = parser.parse_args()
    if not (args.input_qc or args.input_overlap):
        print("No json provided")
        exit(1)

    with open(args.output, "w") as f_out:
        if args.input_qc:
            with open(args.input_qc, "r") as f_in:
                input = json.load(f_in)
                total_reads = input["summary"]["before_filtering"]["total_reads"]
                count = total_reads
                f_out.write(f"Initial reads: {total_reads}\n")
                filtered_reads = input["summary"]["after_filtering"]["total_reads"]
                f_out.write(f"Reads passed filters: {filtered_reads}\n")

                if "low_quality_reads" in input["filtering_result"]:
                    lq = input["filtering_result"]["low_quality_reads"]

                f_out.write(f"Low quality reads: {lq}\n")
                """
                if 'too_short_reads' in input['filtering_result']:
                    count -= input['filtering_result']['too_short_reads']
                if 'too_long_reads' in input['filtering_result']:
                    count -=  input['filtering_result']['too_long_reads']
                f_out.write(f"Length filter: {count}\n")
                if 'too_many_N_reads' in input['filtering_result']:
                    count -= input['filtering_result']['too_many_N_reads']
                f_out.write(f"Qualified reads filter: {count}\n")
                """
        if args.decontamination_overlap:
            counts = []
            with open(args.decontamination_overlap, "r") as f_in:
                for line in f_in:
                    counts.append(line.strip())
                if len(counts) == 1:
                    f_out.write(f"Cleaned reads: {counts[0]}\n")
                elif len(counts) == 2:
                    f_out.write(f"Cleaned forward reads: {counts[0]}\n")
                    f_out.write(f"Cleaned reverse reads: {counts[1]}\n")
                
        if args.fastp_overlap:
            with open(args.fastp_overlap, "r") as f_in:
                input = json.load(f_in)
                # corrected reads?
                merged_reads = input["merged_and_filtered"]["total_reads"]
                f_out.write(f"Merged reads: {merged_reads}\n")
                
        if args.seqprep_overlap:
            counts = []
            with open(args.seqprep_overlap, "r") as f_in:
                for line in f_in:
                    counts.append(line.strip())
                f_out.write(f"Unmapped_forward: {counts[0]}\n")
                f_out.write(f"Unmapped_reverse: {counts[1]}\n")
                f_out.write(f"Overlapped: {counts[2]}\n")
                
