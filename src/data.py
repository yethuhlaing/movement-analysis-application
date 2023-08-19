def checkFirstTime():
    if USER_DATA["dataframe"]["reference_df"] == None :
        return True
    return False

USER_DATA = { 
    "headingData" : {
        "project_name": "Swimming",
        "project_creator": "Ye Thu"
    },
    "informationData": {
        "height": 34,
        "weight" : 23,
        "student_name": "James"
    } ,
    "visualizationData": {
        "categories": ["Joint Angles XZY"],
        "movements": ["L5S1 Lateral Bending", "L5S1 Axial Bending" ], 
        "scenario": "200Metres",
        "duration": 1000,
        "starting_time": 20,
        "Graph_type": "Single Graph" , 
        # Graph type options =>["Single Graph", "Double Graph"],
        "ref_name": "JohnSon",
        "ref_file": "C:/Users/yethu/Desktop/Movement Analysis Project/data/Reference downsampled data/Simulator riding/Reference Harjusimu-003 Extended walk.xlsx",
        "student_name": "Toni",
        "student_file": "C:/Users/yethu/Desktop/Movement Analysis Project/data/Student downsampled data/simulator riding/Sudent1-003Harju ext walk.xlsx"
    },
    "dataframe" : {
        "reference_df": None,
        "student_df": None,
        "status_df": None
    },
    "summary_data": {
        "category" : [],
        "movement" : [],
        "minimum_time" : [],
        "maximum_time": [] ,
        "minimum_duration": [] ,
        "optimal_duration": [],
        "maximum_duration":[] ,  
    }
}
