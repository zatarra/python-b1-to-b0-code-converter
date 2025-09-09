# python-b1-to-b0-code-converter
Python implementation of the popular BitBucket converter script that converts b1 codes into b0 as required by the tasmota sonoff rf bridge. Implementation based on [this javascript version](https://github.com/francoismassart/0xB1-to-0xB0) 


# instructions

You can pass a single B1 code to the script:

```python converter.py AA B1 06 12DE 0654 0118 033E 01E0 21E8 581A3A3A3A3B4A3A3B4A3A3B4B4A3A3B4A3A3A3A3A3B4A3B4B4B4B2B2A3A3A3A3A3A3B2A3B2A3B2A3B 55```


Or you can pass a file containing a list of B1 codes.

```python converter.py list_of_codes.txt```

