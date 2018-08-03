import argparse
import progressbar
import sys
import time
import typing


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument('--if',
        dest    = 'if_',
        help    = 'Read from file `IF` instead of stdin.'
    )
    parser.add_argument('--of',
        help    = 'Write to file `OF` instead of stdout.'
    )

    return parser.parse_args()

def _copy(fr, fw, size) -> typing.Tuple[int, bool]:
    written_bytes = 0
    while written_bytes < size:
        data = fr.read(size - written_bytes)
        if not data:
            return written_bytes, True
        written_bytes += len(data)
        fw.write(data)
    return written_bytes, False
    

def dd(
    block_size  : int,
    input_file  : str = None,
    output_file : str = None,
):
    if input_file is None:
        inputf = sys.stdin
    else:
        inputf = open(input_file, 'rb')
    
    if output_file is None:
        outputf = sys.stdout
    else:
        outputf = open(output_file, 'wb')

    bar = progressbar.ProgressBar().start()
    total_written_bytes = 0

    while True:
        written_bytes, eof = _copy(inputf, outputf, block_size)
        total_written_bytes += written_bytes
        bar.maxval += written_bytes
        bar.update(total_written_bytes)
        if eof:
            bar.finish()
            break
        time.sleep(0.01)

    # CLEANUP:
    if input_file is not None:
        inputf.close()
    if output_file is not None:
        outputf.close()

def main():
    args = parse_arguments()
    dd(1, args.if_, args.of)


if __name__ == '__main__':
    main()
    