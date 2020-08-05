#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import logging
from collections.abc import Iterable

from tifffile import TiffFile

from .. import types
from ..buffer_reader import BufferReader
from .ome_tiff_reader import OmeTiffReader

###############################################################################

log = logging.getLogger(__name__)

###############################################################################


class MicromanagerReader(OmeTiffReader):
    """
    Opening and processing the contents of a Micromanager OME Tiff file
    """

    def __init__(self, data: types.FileLike, **kwargs):
        super().__init__(data, **kwargs)

        # Lazy load is mm
        self._is_mm = None
        self._IFD_mapping = None

    @staticmethod
    def _is_this_type(buffer: io.BytesIO) -> bool:
        is_ome = OmeTiffReader._is_this_type(buffer)
        if is_ome:
            with BufferReader(buffer) as buffer_reader:
                # Per the TIFF-6 spec
                # (https://www.itu.int/itudoc/itu-t/com16/tiff-fx/docs/tiff6.pdf),
                # 'II' is little-endian (Intel format)
                # 'MM' is big-endian (Motorola format)
                if buffer_reader.endianness not in [
                    buffer_reader.INTEL_ENDIAN,
                    buffer_reader.MOTOROLA_ENDIAN,
                ]:
                    return False
                magic = buffer_reader.read_uint16()

                # Per TIFF-6, magic is 42.
                if magic == 42:
                    found = False
                    while not found:
                        ifd_offset = buffer_reader.read_uint32()
                        if ifd_offset == 0:
                            return False
                        buffer_reader.buffer.seek(ifd_offset, 0)
                        entries = buffer_reader.read_uint16()
                        for n in range(0, entries):
                            tag = buffer_reader.read_uint16()
                            type = buffer_reader.read_uint16()
                            count = buffer_reader.read_uint32()
                            offset = buffer_reader.read_uint32()
                            if tag == 51123:
                                if offset == 0:
                                    return False
                                found = True
                                break

                # Per BigTIFF
                # (https://www.awaresystems.be/imaging/tiff/bigtiff.html), magic is 43.
                if magic == 43:
                    # Alex magic here...
                    if buffer_reader.read_uint16() != 8:
                        return False
                    if buffer_reader.read_uint16() != 0:
                        return False
                    found = False
                    while not found:
                        ifd_offset = buffer_reader.read_uint64()
                        if ifd_offset == 0:
                            return False
                        buffer_reader.buffer.seek(ifd_offset, 0)
                        entries = buffer_reader.read_uint64()
                        for n in range(0, entries):
                            tag = buffer_reader.read_uint16()
                            type = buffer_reader.read_uint16()  # noqa: F841
                            count = buffer_reader.read_uint64()
                            offset = buffer_reader.read_uint64()
                            if tag == 51123:
                                if offset == 0:
                                    return False
                                found = True
                                break
            return True

    def _lazy_init_mm_metadata(self) -> dict:
        with TiffFile(self._file) as tiff:
            if tiff.is_micromanager:
                mm_metadata = tiff.micromanager_metadata
        return mm_metadata

    def is_mm(self):
        return self.is_this_type(self._file)

    @property
    def metadata(self) -> dict:
        if self._metadata is None:
            ome_metadata = self._lazy_init_metadata()
            mm_metadata = self._lazy_init_mm_metadata()
            self._metadata = {'ome_metadata': ome_metadata,
                              'mm_metadata': mm_metadata}
        return self._metadata

    def get_page_metadata(self, z=0, c=0, t=0, s=0) -> dict:
        ## TODO: Check that inputs are of the correct dimensions

        if self._IFD_mapping is None:
            ome_metadata = self.metadata['ome_metadata']
            pixels = ome_metadata.image(0).Pixels
            self._IFD_mapping = {}
            for i in range(pixels.plane_count):
                tiff_data = pixels.TiffData(i)
                self._IFD_mapping[(tiff_data.FirstZ,
                                   tiff_data.FirstC,
                                   tiff_data.FirstT)] = tiff_data.IFD

        with TiffFile(self._file) as tiff:
            IFD = self._IFD_mapping[(z, c, t)]
            page = tiff.series[s].pages[IFD].aspage()
            page_metadata = page.tags[51123].value

        return page_metadata
