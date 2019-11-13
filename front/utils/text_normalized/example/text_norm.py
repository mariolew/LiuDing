# -*- coding: utf-8 -*-

import sys
import text_normalized.ch_convert as num_to_ch

if __name__ == '__main__':
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage: {0} <in_text> <out_text> [<split_sym>,default=' ']".format(sys.argv[0]))
        exit(1)
    if len(sys.argv) == 3:
        split_sym = ' '
    else:
        split_sym = sys.argv[3]
    in_text = open(sys.argv[1]).readlines()
    with open(sys.argv[2], 'w') as f:
        for line in in_text:
            items = line.strip().split(split_sym)
            if len(items) > 1:
                uttid = items[0]
                text = ''.join(items[1:])
                try:
                    convert_text = num_to_ch.convert_one_sent(text)
                    f.write('{0}{2}{1}\n'.format(uttid, convert_text, split_sym))
                except Exception as e:
                    print('{0}:{1}'.format(uttid, str(e)))
                finally:
                    pass
        f.close()
