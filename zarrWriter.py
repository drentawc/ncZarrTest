
#/Users/will/opt/miniconda3/envs/zarr/bin/python zarrWriter.py --path inputs/SM_D2022270_Map_SATSSS_data_1day.nc


import xarray as xa
import zarr
import netCDF4
import fsspec
import h5py
from hdf5zarr import HDF5Zarr

from sys import stdout
import argparse

#from zarr.storage import FileChunkStore

def main():

    parser = setupArgparser().parse_args()

    #createNcZarr(parser.path)

    createZarr(parser.path)

    #printZarr()


def createNcZarr(path):

# >>> source = h5py.File('data/example.h5', mode='r')
# >>> dest = zarr.open_group('data/example2.zarr', mode='w')
# >>> zarr.copy_all(source, dest, log=stdout)
# copy /foo
# copy /foo/bar
# copy /foo/bar/baz (100,) int64
# copy /spam (100,) int64
# all done: 4 copied, 0 skipped, 1,600 bytes copied
# (4, 0, 1600)
# >>> dest.tree()
# /
#  ├── foo
#  │   └── bar
#  │       └── baz (100,) int64
#  └── spam (100,) int64

    hdf = h5py.File(path, mode='r')

    print(hdf.keys())

    dest = zarr.open_group('outputs/netcdfjava.zarr', mode='w')

    zarr.copy_all(hdf, dest, log=stdout)


    # for key in hdf:
    #     print(hdf[key])
    #     zarr.copy(hdf['chlor_a'], dest, log=stdout)

    #dest.tree()

    # file_name = 'inputs/V2022001_a1_WW00_chlora.nc'
    # hdf5_zarr = HDF5Zarr(filename = file_name, store_mode='w', max_chunksize=2*2**20)
    # zgroup = hdf5_zarr.consolidate_metadata(metadata_key = '.zmetadata')

    # zgroup.tree()



    #ncfile = netCDF4.Dataset('inputs/V2022002_a1_WW00_chlora.nc')
    # ncfile.close()


def createZarr(path):
    data = xa.open_dataset(path)

    #data = zarr.open('outputs/dataset.file')

    #data = xa.open_dataset('outputs/dataset.zarr')

    #data = netCDF4.Dataset('inputs/ncolci.nc', "w", format="NETCDF4")

    #data = zarr.open('inputs/V2022002_a1_WW00_chlora.nc')


    #Test zarr to see if netcdf-Java can read base zarr
    #data = zarr.zeros((10000, 10000), chunks=(1000, 1000), dtype='i4')

    # print("data loaded")

    # print(data)

    # zarr.save('outputs/netcdfjava.zarr', data)

    #print(data.tree())

    data.to_zarr('outputs/netcdf.zarr')

    # for variable in data.data_vars:

    #     print(variable)

        #zarr.convenience.save('outputs/chlora.zarr', data.data_vars['chlor_a'].to_numpy())

    print("data saved")

def printZarr():

    ""

    # ncfile = fsspec.open('inputs/OLCVCW_I2019157_I2019157_F1_WW00_closest_chlora.nc', 
    #                  anon=False, requester_pays=True)

    # store = fsspec.get_mapper('outputs/test3.zarr', 
    #                       anon=False, requester_pays=True)

    # chunk_store = FileChunkStore(store, chunk_source=ncfile.open())

    #data = xa.open_zarr('inputs/OLCVCW_I2019157_I2019157_F1_WW00_closest_chlora.nc')#, consolidated=True, chunk_store=chunk_store)
    #data = xa.open_zarr('outputs/ncolci.zarr')

    #print(data)

    # print(data.attrs)
    # print("\n\n\n")
    # print(data.data_vars)
    # print("\n\n\n")
    # print(data.variables)

    #print(data['chlor_a'].values)


def dataAccessTest(path):
    data = xa.open_zarr(path)

def setupArgparser():
    parser = argparse.ArgumentParser(description='Zarr test script.')

    parser.add_argument('--path')

    parser.add_argument('--test')
    parser.add_argument('--write')

    return parser

if __name__ == '__main__':
    main()