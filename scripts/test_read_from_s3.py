from datetime import datetime
from typing import NamedTuple

from dask_cloudprovider import FargateCluster
from distributed import Client
from s3fs import S3File, S3FileSystem

from aicsimageio import AICSImage


class TimeReport(NamedTuple):
    dask_data_time: int
    first_plane_time: int
    middle_c_time: int
    full_read_time: int

def read_record_times(path: str) -> TimeReport:
    fs = S3FileSystem(anon=True)
    f = S3File(fs, path)

    img = AICSImage(f)

    start = datetime.now()
    dask_data = img.dask_data
    dask_data_time = (datetime.now() - start).total_seconds()

    start = datetime.now()
    first_plane = img.get_image_data("YX", S=0, T=0, C=0, Z=0)
    first_plane_time = (datetime.now() - start).total_seconds()

    start = datetime.now()
    middle_c = img.get_image_data("ZYX", S=0, T=0, C=img.size_c() / 2)
    middle_c_time = (datetime.now() - start).total_seconds()

    start = datetime.now()
    full_read = img.data
    full_read_time = (datetime.now() - start).total_seconds()

    return TimeReport(dask_data_time, first_plane_time, middle_c_time, full_read_time)

if __name__ == "__main__":
    # Create cluster
    cluster = FargateCluster(
        image="jacksonmaxfield/aicsimageio",
    )

    print("dashboard at", cluster.dashboard_link)

    # Set adaptive worker settings
    cluster.scale_up(32)
    client = Client(cluster)

    sample_image_future = client.submit(read_record_times, "allencell/aics/pipeline_integrated_cell/fovs/0005b3bf_3500001845_100X_20180323_2-Scene-07-P37-E07.ome.tiff")
    sample_image_result = client.gather([sample_image_future])[0]

    print(sample_image_result)
    print("-" * 80)

    all_times_futures = client.map(
        read_record_times,
        [
            "allencell/aics/pipeline_integrated_cell/fovs/000801ac_3500002379_100X_20181005_3-Scene-26-aligned_cropped-P85-G07.ome.tiff",
            "allencell/aics/pipeline_integrated_cell/fovs/000f148b_3500001092_100X_20170718_1-Scene-1-P2-F04.ome.tiff",
            "allencell/aics/pipeline_integrated_cell/fovs/001f99c4_3500000980_100X_20170616_5-Scene-05-P25-E06.ome.tiff",
            "allencell/aics/pipeline_integrated_cell/fovs/00209533_3500000757_100X_20170327_3-Scene-02-P5-D04.ome.tiff",
            "allencell/aics/pipeline_integrated_cell/fovs/00253b64_3500001548_100X_20171117_1-Scene-03-P9-E04.ome.tiff",
            "allencell/aics/pipeline_integrated_cell/fovs/0029681e_3500002410_100X_20181012_1r-Scene-17-aligned_cropped-P47-G03.ome.tiff",
        ]
    )

    print("-" * 80)
    for result in client.gather(all_times_futures):
        print(result)
