---
title: 'AICSImageIO: Delayed Parallel Image Reading for Microscopy Images in Python'
tags:
  - Python
  - Microscopy
  - Image Reading
  - Image Metadata
  - Distributed Computing
authors:
  - name: Jackson Maxfield Brown
    orcid: 0000-0003-2564-0373
    affiliation: 1
  - name: Jamie Sherman
    orcid: {PLEASE LET ME KNOW}
    affiliation: 1
  - name: Madison Bowden
    orcid: {PLEASE LET ME KNOW}
    affiliation: 2
  - name: Daniel Toloudis
    orcid: {PLEAST LET ME KNOW}
    affiliation: 1

affiliations:
  - name: Allen Institute for Cell Science
    index: 1
  - name: Seattle Pacific University
    index: 2
date: 02 April 2020
bibliography: paper.bib
---

# Summary

AICSImageIO is a delayed parallel image reading Python library for reading common microscopy image file formats. Microscopy and computational biologists are increasingly facing challenges when reading images without the software that acquired the image and especially so in a programmatic interface. AICSImageIO acts as a single unified interface and API for the many various image reading frameworks in Python while additionally adding delayed and distributed functionality to each reader.

AICSImageIO is built upon many core image reading and manipulation libraries common to computation biologists who work in Python, namely: [imageio](https://github.com/imageio/imageio), [tifffile](https://github.com/cgohlke/tifffile), and [numpy](https://github.com/numpy/numpy) [@imageio;@tifffile;@numpy].

# Acknowledgments

We wish to thank the Allen Institute for Cell Science founder, Paul G. Allen, for his vision, encouragement, and support. This work could not have been completed without the additional support and input from all members of the Allen Institute for Cell Science.

# References
