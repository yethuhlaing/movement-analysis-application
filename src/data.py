def checkFirstTimeDF():
    dataframe = getDataframe()
    if len(dataframe["reference_df"]) == 0 :
        return True
    return False

def checkFirstTimeHD():
    if USER_DATA["informationData"]["student_name"] == "" :
        print("TUre")
        return True
    return False

def setHeadingData(project_name, project_creator,):
    global USER_DATA
    USER_DATA["headingData"]["project_name"] = project_name
    USER_DATA["headingData"]["project_creator"] = project_creator

def setInformationData( height, weight, student_name):
    global USER_DATA
    USER_DATA["headingData"]["height"] = height
    USER_DATA["headingData"]["weight"] = weight
    USER_DATA["headingData"]["student_name"] = student_name

def setUserData(userData):
    global USER_DATA
    USER_DATA = userData

def setDataframe(dataframe):
    global DATAFRAME
    DATAFRAME = dataframe

def setEachUserData(primaryType, secondaryType, isArray, value):
    global USER_DATA
    if isArray:
        USER_DATA[primaryType][secondaryType].append(value)
    else:
        USER_DATA[primaryType][secondaryType] = value

def setEachDataframe(primaryType, value):
    DATAFRAME[primaryType] = value


def getDataframe():
    return DATAFRAME

def getUserData():
    return USER_DATA


def getHeadingData():
    global USER_DATA
    return USER_DATA["headingData"]

def getInformationData():
    global USER_DATA
    return USER_DATA["informationData"]

def getVisualizationData():
    global USER_DATA
    return USER_DATA["visualizationData"]

def getSummaryData():
    global USER_DATA
    return USER_DATA["summaryData"]


def setLoadingContents(content):
    global LOADING_CONTENTS
    LOADING_CONTENTS.append(content)

def getLoadingContents():
    global LOADING_CONTENTS
    return LOADING_CONTENTS


def setSummaryData(category, value):
    global USER_DATA
    USER_DATA["summaryData"][category].append(value)

def getSummaryData(category):
    global USER_DATA
    return USER_DATA["summaryData"][category]

def getReference_df(): 
    global DATAFRAME
    return DATAFRAME["reference_df"]

def getStudent_df():
    global DATAFRAME
    return DATAFRAME["student_df"]

def getStatus_df():
    global DATAFRAME
    return DATAFRAME["status_df"]

def setReference_df(value):
    global DATAFRAME
    DATAFRAME["reference_df"] = value

def setStudent_df(value):
    global DATAFRAME
    DATAFRAME["student_df"] = value

def setStatus_df(value):
    global DATAFRAME
    DATAFRAME["status_df"] = value


    
def setOneReference_df(value):
    global DATAFRAME
    DATAFRAME["reference_df"].append(value)  

def setOneStudent_df(value):
    global DATAFRAME
    DATAFRAME["student_df"].append(value)

def setOneStatus_df(value):
    global DATAFRAME
    DATAFRAME["status_df"].append(value)




def resetReference_df():
    global DATAFRAME
    DATAFRAME["reference_df"] = []

def resetStudent_df():
    global DATAFRAME
    DATAFRAME["student_df"] = []

def resetStatus_df():
    global DATAFRAME
    DATAFRAME["status_df"] = []

USER_DATA = {}
    # "headingData" : {
    #     "project_name": "",
    #     "project_creator": ""
    #     # "project_name": "Running",
    #     # "project_creator": "Ye Thu"
    # },
    # "informationData": {
    #     "height": 0,
    #     "weight" : 0,
    #     "student_name": ""
    #     # "height": 14,
    #     # "weight" : 23,
    #     # "student_name": "Meteo"
    # } ,
    # "visualizationData": {
    #     "categories": {} ,         
    #     "scenario": "",
    #     "duration": 0,
    #     "starting_time": 0,
    #     "Graph_type": "" , 

    #     "ref_name": "",
    #     "ref_file": "",
    #     "student_name": "",
    #     "student_file": ""

    #     # "categories": {
    #     #     # 'Segment Velocity': ['Pelvis x', 'Pelvis y', 'L5 y', 'L3 x', 'L3 y', 'L3 z', 'T12 x'], 
    #     #     # 'Joint Angles XZY': ['L5S1 Axial Bending', 'L4L3 Lateral Bending', 'L4L3 Axial Rotation',  'L4L3 Flexion/Extension', 'L1T12 Lateral Bending', 'L1T12 Axial Rotation', 'L1T12 Flexion/Extension', 'T9T8 Lateral Bending'], 
    #     #     'Sensor Orientation - Quat': ['Pelvis q1', 'Pelvis q3', 'L5 q0', 'L5 q1', 'L5 q2', 'L5 q3', 'L3 q0']
    #     # } ,         
    #     # "scenario": "200Metres",
    #     # "duration": 50,
    #     # "starting_time": 20,
    #     # "Graph_type": "Single Graph" , 
    #     # # Graph type options =>["Single Graph", "Double Graph"],
    #     # "ref_name": "JohnSon",
    #     # "ref_file": "C:/Users/yethu/Desktop/Movement Analysis Project/data/Reference downsampled data/Simulator riding/Reference Harjusimu-003 Extended walk.xlsx",
    #     # "student_name": "Toni",
    #     # "student_file": "C:/Users/y
    # },
    # "summaryData": {
    #     "category" : [],
    #     "movement" : [],
    #     "minimum_time" : [],
    #     "maximum_time": [] ,
    #     "minimum_duration": [] ,
    #     "optimal_duration": [],
    #     "maximum_duration":[],
    # }


DATAFRAME = {
    ## Dictionary in array
    "reference_df": [],
    "student_df": [],
    "status_df": []
}

LOADING_CONTENTS = []

# "categories": ["Joint Angles XZY"],
# "movements": ["L5S1 Lateral Bending", "L5S1 Axial Bending" ],
 
SpreadsheetData = {
    "Segment Orientation - Quat": [
        "Pelvis q0", "Pelvis q1", "Pelvis q2", "Pelvis q3", "L5 q0", "L5 q1", "L5 q2", "L5 q3", "L3 q0", "L3 q1",
        "L3 q2", "L3 q3", "T12 q0", "T12 q1", "T12 q2", "T12 q3", "T8 q0", "T8 q1", "T8 q2", "T8 q3", "Neck q0",
        "Neck q1", "Neck q2", "Neck q3", "Head q0", "Head q1", "Head q2", "Head q3", "Right Shoulder q0",
        "Right Shoulder q1", "Right Shoulder q2", "Right Shoulder q3", "Right Upper Arm q0", "Right Upper Arm q1",
        "Right Upper Arm q2", "Right Upper Arm q3", "Right Forearm q0", "Right Forearm q1", "Right Forearm q2",
        "Right Forearm q3", "Right Hand q0", "Right Hand q1", "Right Hand q2", "Right Hand q3", "Left Shoulder q0",
        "Left Shoulder q1", "Left Shoulder q2", "Left Shoulder q3", "Left Upper Arm q0", "Left Upper Arm q1",
        "Left Upper Arm q2", "Left Upper Arm q3", "Left Forearm q0", "Left Forearm q1", "Left Forearm q2",
        "Left Forearm q3", "Left Hand q0", "Left Hand q1", "Left Hand q2", "Left Hand q3", "Right Upper Leg q0",
        "Right Upper Leg q1", "Right Upper Leg q2", "Right Upper Leg q3", "Right Lower Leg q0", "Right Lower Leg q1",
        "Right Lower Leg q2", "Right Lower Leg q3", "Right Foot q0", "Right Foot q1", "Right Foot q2", "Right Foot q3",
        "Right Toe q0", "Right Toe q1", "Right Toe q2", "Right Toe q3", "Left Upper Leg q0", "Left Upper Leg q1",
        "Left Upper Leg q2", "Left Upper Leg q3", "Left Lower Leg q0", "Left Lower Leg q1", "Left Lower Leg q2",
        "Left Lower Leg q3", "Left Foot q0", "Left Foot q1", "Left Foot q2", "Left Foot q3", "Left Toe q0", "Left Toe q1",
        "Left Toe q2", "Left Toe q3"],
    "Segment Orientation - Euler": [
        "Pelvis x", "Pelvis y", "Pelvis z", "L5 x", "L5 y", "L5 z", "L3 x", "L3 y", "L3 z", "T12 x", "T12 y", "T12 z", 
        "T8 x", "T8 y", "T8 z", "Neck x", "Neck y", "Neck z", "Head x", "Head y", "Head z", "Right Shoulder x", 
        "Right Shoulder y", "Right Shoulder z", "Right Upper Arm x", "Right Upper Arm y", "Right Upper Arm z", 
        "Right Forearm x", "Right Forearm y", "Right Forearm z", "Right Hand x", "Right Hand y", "Right Hand z", 
        "Left Shoulder x", "Left Shoulder y", "Left Shoulder z", "Left Upper Arm x", "Left Upper Arm y", "Left Upper Arm z", 
        "Left Forearm x", "Left Forearm y", "Left Forearm z", "Left Hand x", "Left Hand y", "Left Hand z", 
        "Right Upper Leg x", "Right Upper Leg y", "Right Upper Leg z", "Right Lower Leg x", "Right Lower Leg y", 
        "Right Lower Leg z", "Right Foot x", "Right Foot y", "Right Foot z", "Right Toe x", "Right Toe y", "Right Toe z", 
        "Left Upper Leg x", "Left Upper Leg y", "Left Upper Leg z", "Left Lower Leg x", "Left Lower Leg y", 
        "Left Lower Leg z", "Left Foot x", "Left Foot y", "Left Foot z", "Left Toe x", "Left Toe y", "Left Toe z"
    ],
    "Segment Position" : [
        "Pelvis x", "Pelvis y", "Pelvis z", "L5 x", "L5 y", "L5 z", "L3 x", "L3 y", "L3 z",
        "T12 x", "T12 y", "T12 z", "T8 x", "T8 y", "T8 z", "Neck x", "Neck y", "Neck z",
        "Head x", "Head y", "Head z", "Right Shoulder x", "Right Shoulder y", "Right Shoulder z",
        "Right Upper Arm x", "Right Upper Arm y", "Right Upper Arm z", "Right Forearm x", "Right Forearm y", "Right Forearm z",
        "Right Hand x", "Right Hand y", "Right Hand z", "Left Shoulder x", "Left Shoulder y", "Left Shoulder z",
        "Left Upper Arm x", "Left Upper Arm y", "Left Upper Arm z", "Left Forearm x", "Left Forearm y", "Left Forearm z",
        "Left Hand x", "Left Hand y", "Left Hand z", "Right Upper Leg x", "Right Upper Leg y", "Right Upper Leg z",
        "Right Lower Leg x", "Right Lower Leg y", "Right Lower Leg z", "Right Foot x", "Right Foot y", "Right Foot z",
        "Right Toe x", "Right Toe y", "Right Toe z", "Left Upper Leg x", "Left Upper Leg y", "Left Upper Leg z",
        "Left Lower Leg x", "Left Lower Leg y", "Left Lower Leg z", "Left Foot x", "Left Foot y", "Left Foot z",
        "Left Toe x", "Left Toe y", "Left Toe z"
    ],
    "Segment Velocity": [
        "Pelvis x", "Pelvis y", "Pelvis z", "L5 x", "L5 y", "L5 z", "L3 x", "L3 y", "L3 z",
        "T12 x", "T12 y", "T12 z", "T8 x", "T8 y", "T8 z", "Neck x", "Neck y", "Neck z",
        "Head x", "Head y", "Head z", "Right Shoulder x", "Right Shoulder y", "Right Shoulder z",
        "Right Upper Arm x", "Right Upper Arm y", "Right Upper Arm z", "Right Forearm x", "Right Forearm y", "Right Forearm z",
        "Right Hand x", "Right Hand y", "Right Hand z", "Left Shoulder x", "Left Shoulder y", "Left Shoulder z",
        "Left Upper Arm x", "Left Upper Arm y", "Left Upper Arm z", "Left Forearm x", "Left Forearm y", "Left Forearm z",
        "Left Hand x", "Left Hand y", "Left Hand z", "Right Upper Leg x", "Right Upper Leg y", "Right Upper Leg z",
        "Right Lower Leg x", "Right Lower Leg y", "Right Lower Leg z", "Right Foot x", "Right Foot y", "Right Foot z",
        "Right Toe x", "Right Toe y", "Right Toe z", "Left Upper Leg x", "Left Upper Leg y", "Left Upper Leg z",
        "Left Lower Leg x", "Left Lower Leg y", "Left Lower Leg z", "Left Foot x", "Left Foot y", "Left Foot z",
        "Left Toe x", "Left Toe y", "Left Toe z"
    ],
    "Segment Acceleration": [
        "Pelvis x", "Pelvis y", "Pelvis z", "L5 x", "L5 y", "L5 z", "L3 x", "L3 y", "L3 z",
        "T12 x", "T12 y", "T12 z", "T8 x", "T8 y", "T8 z", "Neck x", "Neck y", "Neck z",
        "Head x", "Head y", "Head z", "Right Shoulder x", "Right Shoulder y", "Right Shoulder z",
        "Right Upper Arm x", "Right Upper Arm y", "Right Upper Arm z", "Right Forearm x", "Right Forearm y", "Right Forearm z",
        "Right Hand x", "Right Hand y", "Right Hand z", "Left Shoulder x", "Left Shoulder y", "Left Shoulder z",
        "Left Upper Arm x", "Left Upper Arm y", "Left Upper Arm z", "Left Forearm x", "Left Forearm y", "Left Forearm z",
        "Left Hand x", "Left Hand y", "Left Hand z", "Right Upper Leg x", "Right Upper Leg y", "Right Upper Leg z",
        "Right Lower Leg x", "Right Lower Leg y", "Right Lower Leg z", "Right Foot x", "Right Foot y", "Right Foot z",
        "Right Toe x", "Right Toe y", "Right Toe z", "Left Upper Leg x", "Left Upper Leg y", "Left Upper Leg z",
        "Left Lower Leg x", "Left Lower Leg y", "Left Lower Leg z", "Left Foot x", "Left Foot y", "Left Foot z",
        "Left Toe x", "Left Toe y", "Left Toe z"
    ],
    "Segment Angular Velocity": [
        "Pelvis x", "Pelvis y", "Pelvis z", "L5 x", "L5 y", "L5 z", "L3 x", "L3 y", "L3 z",
        "T12 x", "T12 y", "T12 z", "T8 x", "T8 y", "T8 z", "Neck x", "Neck y", "Neck z",
        "Head x", "Head y", "Head z", "Right Shoulder x", "Right Shoulder y", "Right Shoulder z",
        "Right Upper Arm x", "Right Upper Arm y", "Right Upper Arm z", "Right Forearm x", "Right Forearm y", "Right Forearm z",
        "Right Hand x", "Right Hand y", "Right Hand z", "Left Shoulder x", "Left Shoulder y", "Left Shoulder z",
        "Left Upper Arm x", "Left Upper Arm y", "Left Upper Arm z", "Left Forearm x", "Left Forearm y", "Left Forearm z",
        "Left Hand x", "Left Hand y", "Left Hand z", "Right Upper Leg x", "Right Upper Leg y", "Right Upper Leg z",
        "Right Lower Leg x", "Right Lower Leg y", "Right Lower Leg z", "Right Foot x", "Right Foot y", "Right Foot z",
        "Right Toe x", "Right Toe y", "Right Toe z", "Left Upper Leg x", "Left Upper Leg y", "Left Upper Leg z",
        "Left Lower Leg x", "Left Lower Leg y", "Left Lower Leg z", "Left Foot x", "Left Foot y", "Left Foot z",
        "Left Toe x", "Left Toe y", "Left Toe z"
    ],
    "Segment Angular Acceleration": [
        "Pelvis x", "Pelvis y", "Pelvis z", "L5 x", "L5 y", "L5 z", "L3 x", "L3 y", "L3 z",
        "T12 x", "T12 y", "T12 z", "T8 x", "T8 y", "T8 z", "Neck x", "Neck y", "Neck z",
        "Head x", "Head y", "Head z", "Right Shoulder x", "Right Shoulder y", "Right Shoulder z",
        "Right Upper Arm x", "Right Upper Arm y", "Right Upper Arm z", "Right Forearm x", "Right Forearm y", "Right Forearm z",
        "Right Hand x", "Right Hand y", "Right Hand z", "Left Shoulder x", "Left Shoulder y", "Left Shoulder z",
        "Left Upper Arm x", "Left Upper Arm y", "Left Upper Arm z", "Left Forearm x", "Left Forearm y", "Left Forearm z",
        "Left Hand x", "Left Hand y", "Left Hand z", "Right Upper Leg x", "Right Upper Leg y", "Right Upper Leg z",
        "Right Lower Leg x", "Right Lower Leg y", "Right Lower Leg z", "Right Foot x", "Right Foot y", "Right Foot z",
        "Right Toe x", "Right Toe y", "Right Toe z", "Left Upper Leg x", "Left Upper Leg y", "Left Upper Leg z",
        "Left Lower Leg x", "Left Lower Leg y", "Left Lower Leg z", "Left Foot x", "Left Foot y", "Left Foot z",
        "Left Toe x", "Left Toe y", "Left Toe z"
    ],
    "Joint Angles ZXY" : [
        "L5S1 Lateral Bending", "L5S1 Axial Bending", "L5S1 Flexion/Extension",
        "L4L3 Lateral Bending", "L4L3 Axial Rotation", "L4L3 Flexion/Extension",
        "L1T12 Lateral Bending", "L1T12 Axial Rotation", "L1T12 Flexion/Extension",
        "T9T8 Lateral Bending", "T9T8 Axial Rotation", "T9T8 Flexion/Extension",
        "T1C7 Lateral Bending", "T1C7 Axial Rotation", "T1C7 Flexion/Extension",
        "C1 Head Lateral Bending", "C1 Head Axial Rotation", "C1 Head Flexion/Extension",
        "Right T4 Shoulder Abduction/Adduction", "Right T4 Shoulder Internal/External Rotation", "Right T4 Shoulder Flexion/Extension",
        "Right Shoulder Abduction/Adduction", "Right Shoulder Internal/External Rotation", "Right Shoulder Flexion/Extension",
        "Right Elbow Ulnar Deviation/Radial Deviation", "Right Elbow Pronation/Supination", "Right Elbow Flexion/Extension",
        "Right Wrist Ulnar Deviation/Radial Deviation", "Right Wrist Pronation/Supination", "Right Wrist Flexion/Extension",
        "Left T4 Shoulder Abduction/Adduction", "Left T4 Shoulder Internal/External Rotation", "Left T4 Shoulder Flexion/Extension",
        "Left Shoulder Abduction/Adduction", "Left Shoulder Internal/External Rotation", "Left Shoulder Flexion/Extension",
        "Left Elbow Ulnar Deviation/Radial Deviation", "Left Elbow Pronation/Supination", "Left Elbow Flexion/Extension",
        "Left Wrist Ulnar Deviation/Radial Deviation", "Left Wrist Pronation/Supination", "Left Wrist Flexion/Extension",
        "Right Hip Abduction/Adduction", "Right Hip Internal/External Rotation", "Right Hip Flexion/Extension",
        "Right Knee Abduction/Adduction", "Right Knee Internal/External Rotation", "Right Knee Flexion/Extension",
        "Right Ankle Abduction/Adduction", "Right Ankle Internal/External Rotation", "Right Ankle Dorsiflexion/Plantarflexion",
        "Right Ball Foot Abduction/Adduction", "Right Ball Foot Internal/External Rotation", "Right Ball Foot Flexion/Extension",
        "Left Hip Abduction/Adduction", "Left Hip Internal/External Rotation", "Left Hip Flexion/Extension",
        "Left Knee Abduction/Adduction", "Left Knee Internal/External Rotation", "Left Knee Flexion/Extension",
        "Left Ankle Abduction/Adduction", "Left Ankle Internal/External Rotation", "Left Ankle Dorsiflexion/Plantarflexion",
        "Left Ball Foot Abduction/Adduction", "Left Ball Foot Internal/External Rotation", "Left Ball Foot Flexion/Extension"
    ],
    "Joint Angles XZY": [
        "L5S1 Lateral Bending", "L5S1 Axial Bending", "L5S1 Flexion/Extension",
        "L4L3 Lateral Bending", "L4L3 Axial Rotation", "L4L3 Flexion/Extension",
        "L1T12 Lateral Bending", "L1T12 Axial Rotation", "L1T12 Flexion/Extension",
        "T9T8 Lateral Bending", "T9T8 Axial Rotation", "T9T8 Flexion/Extension",
        "T1C7 Lateral Bending", "T1C7 Axial Rotation", "T1C7 Flexion/Extension",
        "C1 Head Lateral Bending", "C1 Head Axial Rotation", "C1 Head Flexion/Extension",
        "Right T4 Shoulder Abduction/Adduction", "Right T4 Shoulder Internal/External Rotation", "Right T4 Shoulder Flexion/Extension",
        "Right Shoulder Abduction/Adduction", "Right Shoulder Internal/External Rotation", "Right Shoulder Flexion/Extension",
        "Right Elbow Ulnar Deviation/Radial Deviation", "Right Elbow Pronation/Supination", "Right Elbow Flexion/Extension",
        "Right Wrist Ulnar Deviation/Radial Deviation", "Right Wrist Pronation/Supination", "Right Wrist Flexion/Extension",
        "Left T4 Shoulder Abduction/Adduction", "Left T4 Shoulder Internal/External Rotation", "Left T4 Shoulder Flexion/Extension",
        "Left Shoulder Abduction/Adduction", "Left Shoulder Internal/External Rotation", "Left Shoulder Flexion/Extension",
        "Left Elbow Ulnar Deviation/Radial Deviation", "Left Elbow Pronation/Supination", "Left Elbow Flexion/Extension",
        "Left Wrist Ulnar Deviation/Radial Deviation", "Left Wrist Pronation/Supination", "Left Wrist Flexion/Extension",
        "Right Hip Abduction/Adduction", "Right Hip Internal/External Rotation", "Right Hip Flexion/Extension",
        "Right Knee Abduction/Adduction", "Right Knee Internal/External Rotation", "Right Knee Flexion/Extension",
        "Right Ankle Abduction/Adduction", "Right Ankle Internal/External Rotation", "Right Ankle Dorsiflexion/Plantarflexion",
        "Right Ball Foot Abduction/Adduction", "Right Ball Foot Internal/External Rotation", "Right Ball Foot Flexion/Extension",
        "Left Hip Abduction/Adduction", "Left Hip Internal/External Rotation", "Left Hip Flexion/Extension",
        "Left Knee Abduction/Adduction", "Left Knee Internal/External Rotation", "Left Knee Flexion/Extension",
        "Left Ankle Abduction/Adduction", "Left Ankle Internal/External Rotation", "Left Ankle Dorsiflexion/Plantarflexion",
        "Left Ball Foot Abduction/Adduction", "Left Ball Foot Internal/External Rotation", "Left Ball Foot Flexion/Extension"
    ],
    'Ergonomic Joint Angles ZXY': [
        "T8_Head Lateral Bending", "T8_Head Axial Bending", "T8_Head Flexion/Extension",
        "T8_LeftUpperArm Lateral Bending", "T8_LeftUpperArm Axial Bending", "T8_LeftUpperArm Flexion/Extension",
        "T8_RightUpperArm Lateral Bending", "T8_RightUpperArm Axial Bending", "T8_RightUpperArm Flexion/Extension",
        "Pelvis_T8 Lateral Bending", "Pelvis_T8 Axial Bending", "Pelvis_T8 Flexion/Extension",
        "Vertical_Pelvis Lateral Bending", "Vertical_Pelvis Axial Bending", "Vertical_Pelvis Flexion/Extension",
        "Vertical_T8 Lateral Bending", "Vertical_T8 Axial Bending", "Vertical_T8 Flexion/Extension"
    ],
    'Ergonomic Joint Angles XZY': [
        "T8_Head Lateral Bending", "T8_Head Axial Bending", "T8_Head Flexion/Extension",
        "T8_LeftUpperArm Lateral Bending", "T8_LeftUpperArm Axial Bending", "T8_LeftUpperArm Flexion/Extension",
        "T8_RightUpperArm Lateral Bending", "T8_RightUpperArm Axial Bending", "T8_RightUpperArm Flexion/Extension",
        "Pelvis_T8 Lateral Bending", "Pelvis_T8 Axial Bending", "Pelvis_T8 Flexion/Extension",
        "Vertical_Pelvis Lateral Bending", "Vertical_Pelvis Axial Bending", "Vertical_Pelvis Flexion/Extension",
        "Vertical_T8 Lateral Bending", "Vertical_T8 Axial Bending", "Vertical_T8 Flexion/Extension"
    ],
    "Center of Mass": [
        "CoM pos x", "CoM pos y", "CoM pos z",
        "CoM vel x", "CoM vel y", "CoM vel z",
        "CoM acc x", "CoM acc y", "CoM acc z"
    ]
    
}