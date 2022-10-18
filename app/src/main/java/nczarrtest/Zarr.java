
/**
 * 
 * ./gradlew run --args="/Users/will/Documents/GitHub/ncZarrTest/outputs/netcdf.zarr"
 * 
 * 
 */

package nczarrtest;

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

import com.bc.zarr.*;

import org.nd4j.linalg.api.buffer.DataBuffer;
import org.nd4j.linalg.factory.Nd4j;

import main.java.nczarrtest.OutputHelper;
import static main.java.nczarrtest.OutputHelper.createOutput;

import java.nio.Buffer;
import java.nio.file.Path;


public class Zarr {

    //private static Logger logger = LoggerFactory.getLogger(Zarr.class);

    public static void main(String[] args) throws Exception {

        System.out.println(args[0]);

        //jZarrRead(args[0]);

        netCdfRead(args[0]);
    
    }

    /**
     * Read zarrPath file using JZarr
     * @param zarrPath
     * @throws Exception
     */
    public static void jZarrRead(String zarrPath) throws Exception {
        ZarrArray array = ZarrArray.open(zarrPath);

        float[] entireData = (float[]) array.read();

        System.out.println(array);

        // Helper method from JZarr to print out all data
        OutputHelper.Writer writer = out -> {
            DataBuffer buffer = Nd4j.createBuffer(entireData);
            out.println(Nd4j.create(buffer).reshape('c', array.getShape()));
        };
    }
    
    /**
     * Read zarrPath file using NetCdf-Java
     * @param zarrPath
     * @throws Exception
     */

    public static void netCdfRead(String zarrPath) throws Exception {

        //System.out.println(zarrPath);

        //NetcdfFile ncfile = NetcdfFiles.open(zarrPath);

        try (NetcdfFile ncfile = NetcdfFiles.open(zarrPath);) {

            System.out.println("No exception happened");

            System.out.println(ncfile.getVariables());

        } catch (IOException ioe) {

            System.out.println("Exception happened");

            System.out.println(ioe);
            
            // Handle less-cool exceptions here
            //logger.log("asd", ioe);
        }

        //System.out.println(ncfile.getVariables());

        // // a local file path + '.zip'
        // NetcdfFile zipdirectoryStoreZarr = NetcdfFiles.open(pathToZipStore);
        // // an object store path, sarting with 'cdms3:' and ending with 'delimiter=' + the store delimiter
        // NetcdfFile objectStoreZarr = NetcdfFiles.open(pathToObjectStore);
    }


    // Helper method found online to perform JZarr read from S3 data source

    // static void readFromS3Bucket(Path bucketPath) throws IOException, InvalidRangeException {
    //     Path groupPath = bucketPath.resolve("GroupName.zarr");
    //     final ZarrGroup group = ZarrGroup.open(groupPath);
    //     ZarrArray array = group.openArray("AnArray");
    //     byte[] bytes = (byte[]) array.read();
    //     System.out.println(Arrays.toString(bytes));
    // } /// end

    /**
     * 
     * Generating cdls:
     * ncdump -b c foo.nc > foo.cdl
     * 
     * 
     * Generating NCZarr files:
     * 
     * /Users/will/Documents/GitHub/ncZarrTest/outputs/
     * ``` ncgen -4 -lb -o "file:///Users/will/Documents/GitHub/ncZarrTest/outputs/dataset.file#mode=nczarr,file" dataset.cdl ```
     * Display the content of an nczarr file using a local directory tree as storage. ``` ncdump "file:///home/user/dataset.zip#mode=nczarr,zip" ```
     * Create an nczarr file using S3 as storage. ``` ncgen -4 -lb -o "s3://s3.us-west-1.amazonaws.com/datasetbucket" dataset.cdl ```
     * Create an nczarr file using S3 as storage and keeping to the pure zarr format. ``` ncgen -4 -lb -o "s3://s3.uswest-1.amazonaws.com/datasetbucket#mode=zarr" dataset.cdl ```
     * 
     * 
     * 
     */



}

