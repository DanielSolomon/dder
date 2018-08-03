import argparse
import progressbar
import sys
import time
import typing

class DD:

    def __init__(self,
        block_size      : int,
        input_file      : str   = None,
        output_file     : str   = None,
        count           : int   = None,
        total_bytes     : int   = None,
        progress_bar    : bool  = None,
    ):
        self.block_size     = block_size
        self.input_file     = input_file
        self.output_file    = output_file
        self.progress_bar   = progress_bar

        if count is not None:
            count_max_value = block_size * count
            self._max_value = count_max_value
        
        if total_bytes is not None and count is not None:
            self._max_value = min(total_bytes, count_max_value)
        elif total_bytes is not None:
            self._max_value = total_bytes

        if total_bytes is None and count is None:
            self._max_value = progressbar.UnknownLength

        if input_file is None:
            self._fr = sys.stdin
        else:
            self._fr = open(input_file, 'rb')

        if output_file is None:
            self._fw = sys.stdout
        else:
            self._fw = open(output_file, 'wb')

        if self.progress_bar is None or self.progress_bar:
            if self._max_value == progressbar.UnknownLength:
                self._progressbar = progressbar.ProgressBar()
            else:
                self._progressbar = progressbar.ProgressBar(maxval=self._max_value)
        else:
            self._progressbar = None

        self.start          = False
        self.written_bytes  = 0


    def __del__(self):
        if self.input_file is not None:
            self._fr.close()
        if self.output_file is not None:
            self._fw.close()

    @property
    def written_bytes(self) -> int:
        return self._written_bytes

    @property
    def _unknown_size(self) -> bool:
        return self._max_value == progressbar.UnknownLength

    @written_bytes.setter
    def written_bytes(self, value : int) -> None:
        self._written_bytes = value
        if self._progressbar and self._unknown_size and self.start:
            self._progressbar.maxval = value + self.block_size * 100
            self._progressbar.update(value)

    def _copy_block(self) -> None:
        written_bytes = 0
        if not self._unknown_size:
            block_size = min(self.block_size, self._max_value - self.written_bytes)
        else:
            block_size = self.block_size
        while written_bytes < block_size:
            data = self._fr.read(block_size - written_bytes)
            if not data:
                return written_bytes, True
            written_bytes += len(data)
            self._fw.write(data)
        return written_bytes, False

    def do_dis(self) -> None:
        self.start = True
        if self._progressbar:
            self._progressbar = self._progressbar.start()
        while self._max_value == progressbar.UnknownLength or self.written_bytes < self._max_value:
            written_bytes, eof = self._copy_block()
            self.written_bytes += written_bytes
            if eof or self.written_bytes == self._max_value:
                break
        if self._progressbar:
            self._progressbar.finish()
        self.start = False

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

def main():
    args = parse_arguments()
    dd = DD(1, args.if_, args.of)
    dd.do_dis()

if __name__ == '__main__':
    main()
    