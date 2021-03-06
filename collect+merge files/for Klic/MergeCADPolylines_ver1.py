import os
import arcpy

#Input parameter
in_path=arcpy.GetParameterAsText(0)
gdb_path=arcpy.GetParameterAsText(1)
#Output parameter
out_merge=arcpy.GetParameterAsText(2)

def pr(x):
    arcpy.AddMessage(x)

#Creating the feature layers for the specified CAD objects from specific CAD layers
list_layers=[]
s=0
for dirpath, dirnames, filenames in os.walk(in_path):
    for filename in filenames:
        if filename.endswith((".DWG",".dwg")):
            s+=1
            filename_path=os.path.join(dirpath,filename)
            object_path=os.path.join(filename_path,"Polyline")
            feature_layer="Layer"+str(s)
            #ex below: "D:\\ioana\\cadastru.DWG\\Polyline", "cadastru", "\"Layer\" = 'CORP_PROPR'"
            arcpy.MakeFeatureLayer_management(object_path, feature_layer)
            list_layers.append(feature_layer)
pr("feature layers created")           
to_merge=str(' " '+'; '.join(list_layers)+' " ')

arcpy.env.workspace = gdb_path
# Set Geoprocessing environments
arcpy.env.outputCoordinateSystem = "PROJCS['RD_New',GEOGCS['GCS_Amersfoort',DATUM['D_Amersfoort',SPHEROID['Bessel_1841',6377397.155,299.1528128]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Double_Stereographic'],PARAMETER['False_Easting',155000.0],PARAMETER['False_Northing',463000.0],PARAMETER['Central_Meridian',5.38763888888889],PARAMETER['Scale_Factor',0.9999079],PARAMETER['Latitude_Of_Origin',52.15616055555555],UNIT['Meter',1.0]]"
arcpy.Merge_management(to_merge, os.path.join(gdb_path,out_merge))


arcpy.DeleteField_management(out_merge, "Handle;LyrFrzn;LyrLock;LyrOn;LyrVPFrzn;LyrHandle;EntColor;LyrColor;BlkColor;EntLinetype;LyrLnType;BlkLinetype;Thickness;EntLineWt;LyrLineWt;BlkLineWt;LTScale;ExtX;ExtY;ExtZ;DocName;DocPath;DocType;DocVer")
pr("merged file created. Done.")

                                              
