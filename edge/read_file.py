import os


def last_n_lines(f_name, n):
    buf_size = 8192
    f_size = os.stat(f_name).st_size
    i = 0
    data = []
    with open(f_name) as f:
        if buf_size > f_size:
            buf_size = f_size - 1
            fetched_lines = []
            while True:
                i += 1
                f.seek(f_size - buf_size * i)
                fetched_lines.extend(f.readlines())
                if len(fetched_lines) >= n or f.tell() == 0:
                    data.append(''.join(fetched_lines[-n:]))
                    break
