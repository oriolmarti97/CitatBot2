#!/bin/bash

find captures -type f ! -atime 4 -delete
find captures -type d -empty -delete
