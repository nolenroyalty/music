#!/usr/bin/env python3
import argparse
import src.commands

def main():
    parser = src.commands.get_parser()
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__": main()
