#! /usr/bin/env python
import sys
from aubio import source, tempo
from numpy import median, diff

def get_file_bpm(path, params=None):
    """ Calculate the beats per minute (bpm) of a given file.
        path: path to the file
        param: dictionary of parameters
         {
           'key1': 'somevalue',
           'mode': 'fast',
         }
    """
    if params is None:
        params = {}
    # default:
    samplerate, win_s, hop_s = 44100, 1024, 512
    if 'mode' in params:
        if params.mode in ['super-fast']:
            # super fast
            samplerate, win_s, hop_s = 4000, 128, 64
        elif params.mode in ['fast']:
            # fast
            samplerate, win_s, hop_s = 8000, 512, 128
        elif params.mode in ['default']:
            pass
        else:
            print("unknown mode {:s}".format(params.mode))
    # manual settings
    if 'samplerate' in params:
        samplerate = params.samplerate
    if 'win_s' in params:
        win_s = params.win_s
    if 'hop_s' in params:
        hop_s = params.hop_s

    s = source(path, samplerate, hop_s)
    samplerate = s.samplerate
    o = tempo("specdiff", win_s, hop_s, samplerate)
    # List of beats, in samples
    beats = []
    # Total number of frames read
    total_frames = 0

    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = o.get_last_s()
            beats.append(this_beat)
            #if o.get_confidence() > .2 and len(beats) > 2.:
            #    break
        total_frames += read
        if read < hop_s:
            break

    def beats_to_bpm(beats, path):
        # if enough beats are found, convert to periods then to bpm
        if len(beats) > 1:
            if len(beats) < 4:
                print("few beats found in {:s}".format(path))
            bpms = 60./diff(beats)
            return median(bpms)
        else:
            print("not enough beats found in {:s}".format(path))
            return 0

    return beats_to_bpm(beats, path)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', help="mode [default|fast|super-fast]", dest="mode")
    """
    when you type : python demo_bpm_extract.py -m fast
    add_arguent will put the word "fast" under the "mode" keyu in your dictionary
    """
    parser.add_argument('sources', nargs='*', help="input_files")
    args = parser.parse_args()
    for f in args.sources:
        bpm = get_file_bpm(f, params = args)
        # print("{:6s} {:s}".format("{:2f}".format(bpm),f))
        print "source file: ",f
        print ("The bpm is: %7.3f.") %bpm



#! tempo
#! /usr/bin/env python
win_s = 512                 # fft size
hop_s = win_s // 2          # hop size

if len(sys.argv) < 2:
    print("Usage: %s <filename> [samplerate]" % sys.argv[0])
    sys.exit(1)

filename = sys.argv[1]

samplerate = 0
if len( sys.argv ) > 2: samplerate = int(sys.argv[2])

print "samplerate: ", samplerate
print ""

s = source(filename, samplerate, hop_s)
samplerate = s.samplerate
o = tempo("default", win_s, hop_s, samplerate)

# tempo detection delay, in samples
# default to 4 blocks delay to catch up with
delay = 4. * hop_s

# list of beats, in samples
beats = []

# total number of frames read
total_frames = 0

fh1=open("BeatsMusic.txt", "w")
fh1.write('{ "The Music of": ')
fh1.write(f)
fh1.write(",")
fh1.write("\n")
fh1.write(("'bpm': %i") %bpm)
fh1.write(",")
fh1.write("\n")

fh1.write("'beat_list': [")

while True:
    samples, read = s()
    is_beat = o(samples)
    if is_beat:
        this_beat = int(total_frames - delay + is_beat[0] * hop_s)
        print("%6.1f" % (this_beat / float(samplerate)))
        beats.append(this_beat)
        fh1.write("%6.1f" % (this_beat / float(samplerate)))
    total_frames += read
    if read < hop_s: break

fh1.write("]}")

fh1.close()
#print len(beats)
