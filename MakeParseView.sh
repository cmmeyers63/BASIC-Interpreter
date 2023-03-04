#!/bin/bash

# Make a pdf from the .dot file created by the application
dot -Tpdf parse.dot > parse.pdf
# view in firefox for convinence
firefox parse.pdf