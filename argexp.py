# from __future__ import print_function
# from argparse import ArgumentParser
# parser = ArgumentParser()
# parser.add_argument("pos1", help="positional argument 1")
# parser.add_argument("-o", "--optional-arg", help="optional argument", dest="opt", default="default")
# args = parser.parse_args()
# print("positional arg:", args.pos1)
# print("optional arg:", args.opt)

# import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument('-m', '--mode', help="mode [default|fast|super-fast]", dest="mode")
# parser.add_argument('sources', nargs='*', help="input_files")
# args = parser.parse_args()
# for f in args.sources:
#     bpm = get_file_bpm(f, params = args)
#     print("{:6s} {:s}".format("{:2f}".format(bpm), f))

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbose:
    print "the square of {} equals {}".format(args.square, answer)
else:
    print answer
