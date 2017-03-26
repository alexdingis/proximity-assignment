import arcpy
## set the workspace environment
workSpace                 = "C:\my\workspace\and\geodatabase.gdb"
arcpy.env.workspace       = workSpace
arcpy.env.overwriteOutput = True
## set variables, points = HCVP locations, nearPoints = population centers, nearTable = near statistics table
## these variables you may need to change as the analysis changes
points                    = "state_plane_randomized_voucher_locations"
nearPoints                = "state_plane_population_centers"
nearTable                 = "Near_Table_02"
## the below is the summarized table of the near table and the accompanying statistics
## these variables always stay the same, no change required
## sumTable = 
sumTable                  = "%s_SUMMARY" %(nearTable)
myFields                  = [["NEAR_DIST","COUNT"],["NEAR_DIST","MIN"],["NEAR_DIST","MAX"],["NEAR_DIST","MEAN"],["NEAR_DIST","STD"]]
## generate near table
arcpy.GenerateNearTable_analysis(points,nearPoints,nearTable,"","LOCATION","","CLOSEST")
## summarize the near table
arcpy.Statistics_analysis(nearTable,sumTable,myFields,"NEAR_FID")
## add coefficient of vartion and name fields
arcpy.AddField_management(sumTable,"NEAR_DIST_CV","DOUBLE")
arcpy.AddField_management(sumTable,"NAME","TEXT")
## join in the population centers to get their names, it makes reading the table easier
arcpy.AddJoin_management(sumTable,"NEAR_FID",nearPoints,"OBJECTID")
## calculate coefficient of variation and bring in the name of the population center
arcpy.CalculateField_management(sumTable,"NEAR_DIST_CV", "!STD_NEAR_DIST! / !MEAN_NEAR_DIST!","PYTHON_9.3")
expression   = "!%s.NAME!" %(nearPoints)
sumTableName = "%s.NAME"   %(sumTable)
arcpy.CalculateField_management(sumTable,sumTableName,expression,"PYTHON_9.3")
## remove the join
arcpy.RemoveJoin_management(sumTable,nearPoints)
