
#/Users/will/opt/miniconda3/envs/zarr/bin/python zarrWriter.py


import xarray as xa

def main():
    
    createZarr()

    printZarr()


def createZarr():
    data = xa.open_dataset('OLCVCW_I2019157_I2019157_F1_WW00_closest_chlora.nc')

    print("data loaded")

    data.to_zarr('OLCVCW_I2019157_I2019157_F1_WW00_closest_chlora.zarr')

    print("data saved")

def printZarr():
    data = xa.open_zarr('OLCVCW_I2019157_I2019157_F1_WW00_closest_chlora.zarr')

    print(data.attrs)
    print("\n\n\n")
    print(data.data_vars)
    print("\n\n\n")
    print(data.variables)

if __name__ == '__main__':
    main()