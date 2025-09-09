import re
import sys
from pathlib import Path

def remove_spaces(s: str) -> str:
    """Collapse one-or-more spaces and remove them entirely."""
    return re.sub(r"\s{1,}", "", s)

def to_hex(n: int) -> str:
    """Uppercase hex without 0x prefix."""
    return format(n, "X")

def left_pad(s: str, length: int = 2, char: str = "0") -> str:
    """Pad on the left with `char` until `length`."""
    if len(char) != 1:
        raise ValueError("pad char must be a single character")
    return s if len(s) >= length else char * (length - len(s)) + s

def extract_main_data(inp: str) -> str:
    """
    Remove spaces, uppercase, then extract the substring between
    prefix AAB1 and suffix 55. Returns '' if not found.
    """
    main_data = ""
    try:
        output = remove_spaces(inp).upper()
        # (^AAB1)([0-9A-F]*)(55$)
        m = re.match(r"^(AAB1)([0-9A-F]*)(55)$", output)
        if m and len(m.groups()) == 3:
            main_data = m.group(2)
    finally:
        return main_data

def convert_b1_to_b0(inp: str, repeat_val: int = 8) -> str:
    """
    Convert a B1-frame payload to a B0-frame payload.

    Output layout:
      AA B0 <len> <numBuckets> <repeats> <buckets...> <data> 55
    """
    input_str = extract_main_data(inp)
    if input_str == "":
        raise ValueError("invalid input")

    bucket_length = 4  # hex chars per bucket
    hex_nbr_buckets = input_str[0:2]
    int_nbr_buckets = int(hex_nbr_buckets, 16)

    buckets = []
    for i in range(int_nbr_buckets):
        start = 2 + i * bucket_length
        buckets.append(input_str[start:start + bucket_length])

    data = input_str[2 + int_nbr_buckets * bucket_length : ]

    # Compute byte length: header(2 bytes: AA B0) + len + count + repeats (2 bytes)
    # + buckets + data + trailer(1 byte 55). The original JS formula counts hex chars,
    # then divides by 2 to get bytes for the variable portion starting after AA B0.
    # It specifically uses: (2 + 2 + (int_nbr_buckets*bucket_length) + len(data)) / 2
    # which corresponds to: <numBuckets><repeats><buckets><data> measured in bytes.
    variable_hex_chars = 2 + 2 + (int_nbr_buckets * bucket_length) + len(data)
    length_bytes = variable_hex_chars // 2  # should be even; integer division mirrors intent

    hex_length = left_pad(to_hex(length_bytes))
    hex_rep_val = left_pad(to_hex(repeat_val))

    parts = [
        "AA",
        "B0",
        hex_length,
        hex_nbr_buckets,
        hex_rep_val,
        *buckets,
        data,
        "55",
    ]
    # Join with spaces exactly like the JS template string.
    return " ".join(parts)

# Optional: simple manual test
if __name__ == "__main__":
    if len(sys.argv) < 2:
      print(f"Usage: {sys.argv[0]} <B1 Code | file_containing_codes.txt>")
      print("")
      print(f"{sys.argv[0]} 'AA B1 06 12DE 0654 0118 033E 01E0 21E8 581A3A3A3A3B4A3A3B4A3A3B4B4A3A3B4A3A3A3A3A3B4A3B4B4B4B2B2A3A3A3A3A3A3B2A3B2A3B2A3B 55'")
      sys.exit(1)
    try:
        _list_codes = Path(sys.argv[1])
        if _list_codes.is_file():
          with open(sys.argv[1], "r") as c:
            codes = c.readlines()
            for i in codes:
              print(convert_b1_to_b0(i, repeat_val=8))
        else:
           print(convert_b1_to_b0(sys.argv[1], repeat_val=8))
    except ValueError as e:
        print("Error:", e)

