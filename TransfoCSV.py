FILENAME = "motion2lenght.csv"
OUTPUT_FILENAME = "motion2.csv"

middle_part_headers = []

def get_header_from_part(part):
    global middle_part_headers

    tmp = part.split('  >  ')
    split = tmp[1].split(' ')
    split = split[1:]

    flag = False
    for s in split:
        if not flag:
            if s.startswith('['):
                flag = True
            else:
                param = s.split('=')
                if param[0] not in middle_part_headers:
                    middle_part_headers.append(param[0])
        else:
            if s.endswith(']'):
                flag = False

# Extract parameters from fields like "Seq=0 Ack=1 Win=65160 Len=0 MSS=1460 SACK_PERM=1 TSval=398896409 TSecr=3714222335 WS=128"
first = True
with open(FILENAME, 'r') as f:
    for line in f:
        # skip the first line
        if first:
            first = False
            continue

        # First major split
        split_1 = line.split(';')
        for minor_split in split_1:
            if "  >  " in minor_split:
                part = minor_split.split('\"\",\"\"')[-1].replace('\"', '')
                get_header_from_part(part)

print('Found the following parameters:')
print(middle_part_headers)
print()

# Extract column headers
headers = []
premade_headers = []

first = True
with open(FILENAME, 'r') as f:
    for line in f:
        line = line.replace('\n', '')

        # First major split
        split_1 = line.split(';')

        # skip the first line
        if first:
            first = False
            premade_headers = line.split(';')
            continue

        for i1 in range(len(split_1)):
            # Get if there is a premade header
            if len(premade_headers[i1]) > 0:
                headers.append(premade_headers[i1])
                continue

            s1 = split_1[i1].replace(',\"', ';').replace('\"', '')

            # second split
            split_2 = s1.split(';')
            for s2 in split_2:
                if "  >  " in s2:
                    # this is a middle part
                    headers.append('X > Y')
                    headers.append('Flags')
                    for mh in middle_part_headers:
                        headers.append(mh)
                else:
                    # No header for this section
                    headers.append('')

        # We are only interested in the second line
        break

print('Found the following headers:')
print(headers)
print()

# Get the actual values for each header
values = []
first = True
with open(FILENAME, 'r') as f:
    for line in f:
        line = line.replace('\n', '')

        # skip the first line
        if first:
            first = False
            continue

        line = line.replace(',\"', ';')
        line = line.replace('\"', '')
        split = line.split(';')

        line_val = []

        for i in range(len(split)):
            s = split[i]

            if '  >  ' in s:
                # this is a middle part

                # get the X  >  Y part
                tmp = s.split('  >  ')
                line_val.append(tmp[0])
                tmp = tmp[1].split(' ')
                line_val[-1] += '  >  ' + tmp[0]
                tmp = tmp[1:]

                # get the flags
                line_val.append('')
                flags = False
                if tmp[0].startswith('['):
                    # there are flags
                    tmp[0] = tmp[0].replace('[', '')
                    flags= True

                while flags:
                    if tmp[0].endswith(']'):
                        # this is the last flag
                        flags = False
                        tmp[0] = tmp[0].replace(']', '')

                    tmp[0] = tmp[0].replace(',', '')
                    if len(line_val[-1]) > 0:
                        line_val[-1] += ', '
                    line_val[-1] += tmp[0]

                    tmp = tmp[1:]

                # get the parameters
                param_index_0 = len(line_val)

                for _ in middle_part_headers:
                    line_val.append('')

                for param in tmp:
                    param_val = param.split('=')
                    if len(param_val) > 1:
                        for pi in range(len(middle_part_headers)):
                            if param_val[0] == middle_part_headers[pi]:
                                line_val[param_index_0 + pi] = param_val[1]
            else:
                line_val.append(s)

        values.append(line_val)

# Write the actual csv
with open(OUTPUT_FILENAME, 'w') as f:
    for i in range(len(headers)):
        if i > 0:
            f.write(';')
        f.write(headers[i])

    f.write('\n')

    for line in values:
        for i in range(len(line)):
            if i > 0:
                f.write(';')
            f.write(line[i])
        f.write('\n')
