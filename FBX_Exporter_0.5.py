#initialization of all Imports and Variables
'''Imports'''
import maya.cmds as cmds
import maya.mel as mel
import subprocess

'''Variables'''
MeshSelection = cmds.ls(selection=True)
try:
    MeshName = MeshSelection[0]
except:
    cmds.error('FBX Exporter requires an active selection. Please select an object.', noContext=True)
    
NewName = ''
MeshPrefix = 'Temp_'   
 
    
    
       
#Mesh Integrity, Non-Manifold, Lamina
'''Non-manifold edges check'''
nonManifoldEdges = cmds.polyInfo(MeshName, nonManifoldEdges=True)
if nonManifoldEdges is None:
    nonManifoldEdgesCheck = 'Good'
else:
    nonManifoldEdgesCheck = 'Bad'


'''Lamina faces check'''
laminaFaces = cmds.polyInfo (MeshName, laminaFaces=True)
if laminaFaces is None:
    LaminaFacesCheck = 'Good'
else:
    LaminaFacesCheck = 'Bad'
    
'''N-Gons Check'''
try:
    NGons = mel.eval('polyCleanupArgList 4 { "0","2","1","0","1","0","0","0","0","1e-05","0","1e-05","0","1e-05","0","-1","0","0" };')
    if NGons == []:
        NGonsCheck = 'Good'
        cmds.warning('FBX exporter initialized')
    else:
        NGonsCheck = 'Bad'
except:
    pass

'''Current unit'''
BoundingBox = cmds.polyEvaluate (MeshName, boundingBox=True)  
MeshHeight = round((BoundingBox[1][1]-BoundingBox[1][0]), 2)

CurrentUnit = cmds.currentUnit (query=True, linear=True )
if CurrentUnit == 'm':
    CurrentUnitCheck = f'{MeshHeight} m'
elif CurrentUnit == 'cm':
    CurrentUnitCheck = f'{MeshHeight} cm'
else:
    CurrentUnitCheck = 'Bad'    



    
    
#Prefix Setup
def PrefixSetup(*args):
    global MeshPrefix
    try:
        cmds.deleteUI(f'{MeshPrefix}{MeshName}')
    except:
        pass
    Object = cmds.confirmDialog(
            title='Confirm', 
            message='What kind of object is it?', 
            button=['Character','Environment', 'Other'], 
            defaultButton='Yes', 
            cancelButton='No', 
            dismissString='No' )
            
    if Object == 'Character':
        Character = cmds.confirmDialog( 
            title='Confirm', 
            message='What type of object is it?', 
            button=['Player','NPC', 'Weapons', 'Gear'], 
            defaultButton='Yes', cancelButton='No', 
            dismissString='No' )
            
        if Character == 'Player':
            MeshPrefix = f'CH_PL_'
        elif Character == 'NPC':
            MeshPrefix = f'CH_NPC_'
        elif Character == 'Weapons':
            MeshPrefix = f'CH_WP_'
        elif Character == 'Gear':
            MeshPrefix = f'CH_GE_'
        else:
            pass
            
    elif Object == 'Environment':
        Character = cmds.confirmDialog(
        title='Confirm', 
        message='What type of object is it?', 
        button=['Wall','Prop', 'Ground'], 
        defaultButton='Yes', 
        cancelButton='No', 
        dismissString='No' )
        
        if Character == 'Wall':
            MeshPrefix = f'EN_W_'
        elif Character == 'Prop':
            MeshPrefix = f'EN_P_'
        elif Character == 'Ground':
            MeshPrefix = f'EN_G_'
        else:
            pass    
        
    elif Object == 'Other':
        Character = cmds.confirmDialog(
        title='Confirm', 
        message='This option is currently not available.', 
        button=['oh, okay :c'], 
        defaultButton='Yes', 
        cancelButton='No', 
        dismissString='No' ) 
   
    else:
        pass
    
    cmds.text(f'{MeshPrefix}{MeshName}', parent = MeshPrefixSetupRight)
    
    
    
    
 
#Change name
def NameChange(*args):
    global MeshName
    global NewName
    global NameDisplayCurrent
    result = cmds.promptDialog(
    		title='Rename Object',
    		message='Enter Name:',
    		button=['OK', 'Cancel'],
    		defaultButton='OK',
    		cancelButton='Cancel',
    		dismissString='Cancel')
    
    if result == 'OK' and MeshPrefix != 'temp':
    	NewName = cmds.promptDialog(query=True, text=True)
    	try:
    	    cmds.deleteUI(f'{NameDisplayCurrent}')
    	    cmds.deleteUI(f'{MeshPrefix}{MeshName}')
    	    
    	except:
    	    pass
    	
    	
    	
    	
    	cmds.rename(MeshName, NewName) 
    	MeshName = NewName
    	NameDisplayCurrent = cmds.text (f'{MeshName}', parent=MeshInformationRight)
    	cmds.text(f'{MeshPrefix}{MeshName}', parent = MeshPrefixSetupRight)
    	
    else:
        NewName ='TempName'
        
        
        
        

#Destination folder
def OpenDestinationFolder(*args):
    global DirectoryAddress
    subprocess.Popen(f'explorer "{DirectoryAddress}"')
    
 
 
 
 
 
#Select Export Destination
def ExportDestination(*args):
    global DirectoryAddress
    global Destination
    try:
        DirectoryAddressList = cmds.fileDialog2(fileMode=3, okCaption='Choose folder',caption='Choose folder to put the file or something i guess')
        DirectoryAddress = DirectoryAddressList[0].replace('/', '\\')
        cmds.deleteUI(Destination)
        Destination = cmds.text(f'{DirectoryAddress}', parent = ExportDestinationSetupRight)
    except:
        pass   
        
        
        
        
        
#Checkboxes
'''Default values 3D'''
SmoothGroupStatus = True
SmoothGroupStatusString = 'true'

HardEdgeStatus = False
HardEdgeStatusString = 'false'

SmoothMeshStatus = False
SmoothMeshStatusString = 'false'

def SmoothingGroups(value):
    global SmoothGroupStatus
    SmoothGroupStatus=value   
    if SmoothGroupStatus == True:   
        SmoothGroupStatusString='true'
    else:
        SmoothGroupStatusString='false'

def HardEdge(value):
    global HardEdgeStatus
    global HardEdgeStatusString
    HardEdgeStatus=value   
    if HardEdgeStatus == True:   
        HardEdgeStatusString='true'
    else:
        HardEdgeStatusString='false'
    
def SmoothMesh(value):
    global SmoothMeshStatus
    SmoothMeshStatus=value
    if SmoothMeshStatus == True:   
        SmoothMeshStatusString='true'
    else:
        SmoothMeshStatusString='false'
    
'''Default values animation'''
SkeletonDefinitionsStatus = 1
SkeletonDefinitionsStatusString = 'false'

def SkeletonDefinitions(value):
    global SkeletonDefinitionsStatus
    SkeletonDefinitionsStatus=value  
    if SkeletonDefinitionsStatus == True:   
        SkeletonDefinitionsStatusString='true'
    else:
        SkeletonDefinitionsStatusString='false'
    print(SkeletonDefinitionsStatusString)
   
#FBXB Exporter 3D
test = ''
SuccessMessage = ''
def ExportFBX(*args):
    global DirectoryAddress
    global test
    global SuccessMessage
    try:
        cmds.deleteUI(SuccessMessage)
    except:
        pass
    try:
        DirectoryAddressFix = DirectoryAddress.replace('\\', '/')
        mel.eval('FBXExportCameras -v false')
        mel.eval(f'FBXExportHardEdges -v {HardEdgeStatusString}')
        mel.eval(f'FBXExportSmoothingGroups -v {SmoothGroupStatusString}')
        mel.eval(f'FBXExportSmoothMesh -v {SmoothMeshStatusString}') 
        mel.eval('FBXExportConstraints -v false')
        
        
        "FBXExportConvertUnitString [mm|dm|cm|m|km|In|ft|yd|mi];"         "<------------------------This command forces size"
        
        cmds.select(MeshName) 
        mel.eval(f'FBXExport -f "{DirectoryAddressFix}/{MeshPrefix}{MeshName}.fbx" -s')
             
        SuccessMessage = cmds.text(f'{MeshPrefix}{MeshName} exported to {DirectoryAddress}.', font='tinyBoldLabelFont', parent = Head)
    except:
        pass
        
#FBX Exporter Animation
test = ''
SuccessMessage = ''
def ExportFBXAnim(*args):
    global DirectoryAddress
    global test
    global SuccessMessage
    try:
        cmds.deleteUI(SuccessMessage)
    except:
        pass
    try:
        DirectoryAddressFix = DirectoryAddress.replace('\\', '/')
        mel.eval('FBXExportCameras -v false')
        mel.eval('FBXExportHardEdges -v false')
        mel.eval('FBXExportSmoothingGroups -v true')
        mel.eval('FBXExportSmoothMesh -v false') 
        mel.eval('FBXExportConstraints -v false') 
        
        mel.eval('FBXExportAnimationOnly -v true')
        mel.eval(f'FBXExportSkeletonDefinitions -v {SkeletonDefinitionsStatusString}')
        mel.eval(f'FBXExportSplitAnimationIntoTakes -v \"{MeshName}\" 10 25') 
        mel.eval('FBXExportApplyConstantKeyReducer -v true')
        
        
        '''
        mel.evel(FBXExportSkeletonDefinitions -v [true|false]; Use this function to either include or exclude Skeleton definition in your export.
        
        '''
        
        cmds.select(MeshName)    
        mel.eval(f'FBXExport -f "{DirectoryAddressFix}/{MeshPrefix}{MeshName}.fbx" -s')
            
        SuccessMessage = cmds.text(f'{MeshPrefix}{MeshName} exported to {DirectoryAddress}.', font='tinyBoldLabelFont', parent = Head)
    except:
        pass



        
                   
#Window
#Contains all informations of layouts. Requires other scripts to be connected to buttons
MainWindow = cmds.window (title="FBX Exporter v0.5", widthHeight=(450, 440), menuBar=True)

form = cmds.formLayout()
tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5, borderStyle='none')
cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )



'''Menu bar'''
cmds.menu 
MenuBar = cmds.menu(label='Help')
cmds.menuItem(label='This is Simons Glorious FBX Exporter v0.5, SGFBXEv0.5 for short, Hope that helps c:')
cmds.menuItem(label='More features coming soon...')

'''Main layout'''
"MainLayout = cmds.columnLayout (adjustableColumn=True, rowSpacing=10, columnAlign = 'center',columnAttach=('both', 5), columnWidth=250)"
Head = cmds.columnLayout ('General', adjustableColumn=True, rowSpacing=10, columnAlign = 'center', columnAttach=('both', 5), parent=tabs)
Head2 = cmds.columnLayout ('How-to', adjustableColumn=True, rowSpacing=10, columnAlign = 'center', width=350, columnAttach=('both', 5), parent=tabs)

cmds.separator (parent=Head)

'''Mesh information'''
MeshInformation = cmds.flowLayout (columnSpacing=10, parent = Head)
MeshInformationLeft = cmds.rowColumnLayout (numberOfColumns=1, columnOffset=(1,'left',25), width=150, parent=MeshInformation)
MeshInformationRight = cmds.rowColumnLayout (numberOfColumns=1, columnOffset=(1,'left',25), width=150, parent=MeshInformation)
cmds.text(f'Mesh name: ', parent=MeshInformationLeft, font='boldLabelFont')
NameDisplayCurrent = cmds.text (f'{MeshName}', parent=MeshInformationRight)


'''Current unit'''
CurrentUnit = cmds.flowLayout (columnSpacing=10, parent = Head)
CurrentUnitLeft = cmds.rowColumnLayout (numberOfColumns=1, columnOffset=(1,'left',25), width=150, parent=CurrentUnit)
CurrentUnitRight = cmds.rowColumnLayout (numberOfColumns=1, columnOffset=(1,'left',25), width=150, parent=CurrentUnit)
cmds.text(f'Current unit: ', font='boldLabelFont', parent=CurrentUnitLeft)
cmds.text(f'{CurrentUnitCheck}', parent=CurrentUnitRight)

'''Mesh integrity'''
MeshIntegrity = cmds.flowLayout (columnSpacing=10, parent = Head)
MeshIntegrityLeft = cmds.rowColumnLayout (numberOfColumns=1, columnOffset=(1,'left',25), width=150, parent=MeshIntegrity)
MeshIntegrityRight = cmds.rowColumnLayout (numberOfColumns=1, columnOffset=(1,'left',25), width=150, parent=MeshIntegrity)
cmds.text(f'Mesh integrity: ', font='boldLabelFont', parent=MeshIntegrityLeft)

if LaminaFacesCheck == 'Good' and nonManifoldEdgesCheck == 'Good' and NGonsCheck == 'Good':
    GoodStatus = cmds.text('Good', backgroundColor=(0,.8,0), width=125, parent=MeshIntegrityRight)
if nonManifoldEdgesCheck == 'Bad':
    nonManifoldEdgesCheckStatus = cmds.text('non-Manifold Edges', backgroundColor=(.8,0,0), width=125, parent=MeshIntegrityRight)
if LaminaFacesCheck == 'Bad':
    LaminaFacesCheckStatus = cmds.text('Lamina Faces', backgroundColor=(.8,0,0), width=125, parent=MeshIntegrityRight)
if NGonsCheck == 'Bad':
    NGonsCheckStatus = cmds.text('N-Gons', backgroundColor=(.8,0,0), width=125, parent=MeshIntegrityRight)



'''Preview'''
MeshPrefixSetup = cmds.flowLayout( columnSpacing=10, parent = Head)
MeshPrefixSetupLeft = cmds.rowColumnLayout (numberOfColumns=1, columnOffset=(1,'left',25), width=150, parent=MeshPrefixSetup)
MeshPrefixSetupRight = cmds.rowColumnLayout (numberOfColumns=1, columnOffset=(1,'left',25), width=150, parent=MeshPrefixSetup)
cmds.text(f'Prefix Preview: ', font='boldLabelFont', parent=MeshPrefixSetupLeft)
cmds.text(f'{MeshPrefix}{MeshName}', parent = MeshPrefixSetupRight)

ExportDestinationSetup = cmds.flowLayout( columnSpacing=10, parent = Head)
ExportDestinationSetupLeft = cmds.rowColumnLayout (numberOfColumns=1, columnOffset=(1,'left',25), width=150, parent=ExportDestinationSetup)
ExportDestinationSetupRight = cmds.rowColumnLayout (numberOfColumns=1, columnOffset=(1,'left',25), parent=ExportDestinationSetup)
cmds.text(f'Destination Preview: ', font='boldLabelFont', parent=ExportDestinationSetupLeft)
try:
    Destination = cmds.text(f'{DirectoryAddress}', parent = ExportDestinationSetupRight)
except:
    DirectoryAddress = 'Currently not specified'
    
cmds.separator(parent=Head)

'''Object choice'''
ObjectChoice = cmds.flowLayout('test',columnSpacing = 10, parent = Head)

cmds.button( label='Prefix setup', command=PrefixSetup, parent = ObjectChoice)
cmds.button( label='Change name', command=NameChange, parent=ObjectChoice)
cmds.button( label='Export Destination', command=ExportDestination, parent = ObjectChoice)
cmds.button( label='Open destination folder', command=OpenDestinationFolder, parent = ObjectChoice)




'''
historyBox = cmds.checkBox('Export history', parent=Head, changeCommand=test45)
CamerasBox = cmds.checkBox('Export Cameras', parent=Head, changeCommand=test45)
SmoothingGroupsBox = cmds.checkBox('Export SmoothingGroups', parent=Head, changeCommand=test45)
'''

'''HOW TO'''
HowToLayout = cmds.flowLayout (columnSpacing=10, parent = Head2)
cmds.text(f'Mesh name: Current name of selected object.', align='left', parent=Head2)
cmds.text(f'Change name: Changes name of mesh (for scene and export).', align='left', parent=Head2)
cmds.separator(parent=Head2)

cmds.text(f'Current unit: Current measurement unit and numeric size.', align='left', parent=Head2)
cmds.text(f'Mesh inegrity: Turns red if there is non-manifold or laminal geometry.', align='left', parent=Head2)
cmds.separator(parent=Head2)

cmds.text(f'Prefix preview: Shows the current prefix that the object will be \nexported with.', align='left', parent=Head2)
cmds.text(f'Prefix setup: Sets prefix corresponding to user input (temp as default).', align='left', parent=Head2)
cmds.separator(parent=Head2)

cmds.text(f'Destination preview: Shows the current export destination.', align='left', parent=Head2)
cmds.text(f'Open destination folder: Opens destination folder.', align='left', parent=Head2)
cmds.text(f'Export Destination: Sets the export destination (saved in session cache).', align='left', parent=Head2)
cmds.text(f'Export mesh: Exports the mesh to given destination.', align='left', parent=Head2)
cmds.separator(parent=Head2)


tabsExport = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5, borderStyle='none', parent=Head)
Animation = cmds.columnLayout ('Animation', adjustableColumn=True, rowSpacing=10, columnAlign = 'center', width=350, columnAttach=('both', 5), parent=tabsExport)
Graphics = cmds.columnLayout ('3D Graphics', adjustableColumn=True, rowSpacing=10, columnAlign = 'center', columnAttach=('both', 5), parent=tabsExport)


cmds.separator (parent=Graphics)
cmds.separator (parent=Animation)

GraphicsCheckboxGrid = cmds.gridLayout (numberOfColumns=3, cellWidth=130, parent=Graphics)
AnimationCheckboxGrid = cmds.gridLayout (numberOfColumns=3, cellWidth=130, parent=Animation)
AnimationColuumn = cmds.columnLayout(columnAlign='left', parent=Animation)

cmds.checkBox(label='Smoothing groups', v=SmoothGroupStatus, changeCommand=SmoothingGroups, parent=GraphicsCheckboxGrid)
cmds.checkBox(label='Hard edges', v=HardEdgeStatus, changeCommand=HardEdge, parent=GraphicsCheckboxGrid)
cmds.checkBox(label='SmoothMesh', v=SmoothMeshStatus, changeCommand=SmoothMesh, parent=GraphicsCheckboxGrid)
cmds.checkBox(label='Export option', parent=GraphicsCheckboxGrid)
cmds.checkBox(label='Export option', parent=GraphicsCheckboxGrid)
cmds.checkBox(label='Export option', parent=GraphicsCheckboxGrid)


cmds.checkBox(label='Include skeleton',v=SkeletonDefinitionsStatus, changeCommand=SkeletonDefinitions, parent=AnimationCheckboxGrid)
cmds.checkBox(label='Export option', parent=AnimationCheckboxGrid)
cmds.checkBox(label='Export option', parent=AnimationCheckboxGrid)
cmds.checkBox(label='Export option', parent=AnimationCheckboxGrid)

cmds.intSliderGrp( field=True, label='Starting frame', parent=AnimationColuumn)
cmds.intSliderGrp( field=True, label='Ending frame', minValue=-10, maxValue=10, fieldMinValue=-100, fieldMaxValue=100, value=0, parent=AnimationColuumn)

cmds.button( label='Export FBX Mesh', width = 100, command=ExportFBX, parent=Graphics)
cmds.button( label='Export FBX Animation', width = 100, command=ExportFBXAnim, parent=Animation)



'''Show window'''
cmds.showWindow(MainWindow)