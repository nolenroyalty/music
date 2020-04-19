#!/usr/bin/env python3
import argparse
import src.commands

def main():
    parser = src.commands.get_parser()
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__": main()
