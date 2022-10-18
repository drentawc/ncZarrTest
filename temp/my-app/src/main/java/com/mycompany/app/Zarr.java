
// java -cp target/my-app-1.0-SNAPSHOT.jar com.mycompany.app.Zarr

package com.mycompany.app;

import ucar.ma2.Array;
import ucar.ma2.ArrayDouble;
import ucar.ma2.ArrayFloat;
import ucar.ma2.DataType;
import ucar.ma2.InvalidRangeException;
import ucar.nc2.Attribute;
import ucar.nc2.Dimension;
import ucar.nc2.NetcdfFile;
import ucar.nc2.Variable;
import ucar.nc2.dataset.NetcdfDataset;
import ucar.nc2.units.DateUnit;
import ucar.nc2.NetcdfFiles;
import ucar.nc2.write.Ncdump;

import java.io.File;
import java.io.IOException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


import java.nio.file.Path;


public class Zarr {

    //private static Logger logger = LoggerFactory.getLogger(Zarr.class);

    public static void main(String[] args) throws Exception {
    
        System.out.println("World");

        //Logger logger = LoggerFactory.getLogger(Zarr.class);

        // a local file path
        // File file = new File("test.zarr");
        // Path filePath = file.getParentFile().toPath();

        NetcdfFile ncfile = NetcdfFiles.open("test.zarr");
    
        Variable v = ncfile.findVariable("chlor_a");
        if (v == null)
        return;

        // sectionSpec is string specifying a range of data, eg ":,1:2,0:3"
        Array data = v.read();
        String arrayStr = Ncdump.printArray(data, "chlor_a", null);

        System.out.println(arrayStr);



    //    try (NetcdfFile ncfile = NetcdfDataset.openFile(NetcdfDataset."test.zarr")) {

            // varName is a string with the name of a variable, e.g. "T"
            // Variable v = ncfile.findVariable("chlor_a");
            // if (v == null)
            // return;

            // // sectionSpec is string specifying a range of data, eg ":,1:2,0:3"
            // Array data = v.read();
            // String arrayStr = Ncdump.printArray(data, "chlor_a", null);

            // System.out.println(arrayStr);

            // Do cool stuff here
        // } catch (IOException ioe) {
        //     System.out.println("error");
        //     // Handle less-cool exceptions here
        //     //logger.info("Error text...", ioe);
        // }

        // // a local file path + '.zip'
        // NetcdfFile zipdirectoryStoreZarr = NetcdfFiles.open(pathToZipStore);
        // // an object store path, sarting with 'cdms3:' and ending with 'delimiter=' + the store delimiter
        // NetcdfFile objectStoreZarr = NetcdfFiles.open(pathToObjectStore);
    
    }
}

