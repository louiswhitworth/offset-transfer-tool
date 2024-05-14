import maya.cmds as cmds # type: ignore
import maya.api.OpenMaya as om # type: ignore

#Set offset parent matrix identity to transform values, then clears transforms to 0
def clearTransforms(*args):
    nodeList = cmds.ls(sl=True)
    for node in nodeList:
        localMatrix = om.MMatrix(cmds.xform(node, q=True, m=True, ws=False))
        offsetParentMatrix = om.MMatrix(cmds.getAttr(f"{node}.offsetParentMatrix"))
        newMatrix = localMatrix * offsetParentMatrix
        cmds.setAttr(f"{node}.offsetParentMatrix", newMatrix, type="matrix")

        #Attributes to clear. Add jointOrient if attr exists (for joints)
        transformList = [".translate", ".rotate", ".scale",]
        transformList.append(".jointOrient") if cmds.attributeQuery('jointOrient', node=node, exists=True) else False

        #Reset transform values
        for attribute in transformList:
            value = 1 if attribute == ".scale" else 0
            for axis in ["X", "Y", "Z"]:
                cmds.setAttr(node + attribute + axis, value)

#Clear offset parent matrix identity and return values to transforms 
def returnTransforms(*args):
    nodeList = cmds.ls(sl=True)
    for node in nodeList:
        localMatrix = om.MMatrix(cmds.xform(node, q=True, m=True, ws=False))
        worldLocation = cmds.xform(node, q=True, m=True, ws=True)
        cmds.setAttr(f"{node}.offsetParentMatrix", localMatrix, type="matrix")
        cmds.xform(f"{node}", m=worldLocation, ws=True)

        
#Create tool UI. Just two buttons, one to send transform values to OPM and one to return them(and one to bring them all, and in the darkness bind them(?))
def offsetParentMatrixToolUI():
    #Check if the window exists, and if it does, delete

    if(cmds.window("offsetParentMatrixToolsUI", ex=1)):
        cmds.deleteUI("offsetParentMatrixToolsUI")

    #Create window
    window = cmds.window("offsetParentMatrixToolsUI", t="Move Transforms to/from Offset Parent Matrix", w=200, h=200, mnb=0,mxb=0)

    #Create the main layout
    mainLayout = cmds.formLayout(nd=100)

    #Buttons
    clearTransformsButton = cmds.button(l="Move transform values to Offset Parent Matrix", c=clearTransforms)
    returnTransformsButton= cmds.button(l="Reset Offset Parent Matrix and Return Transforms", c=returnTransforms)
    

    #Adjust layout
    cmds.formLayout(mainLayout, e=1, attachForm=[(clearTransformsButton, 'top', 5), (clearTransformsButton, 'left', 5), (clearTransformsButton, 'right', 5),
                                                 (returnTransformsButton, 'left', 5), (returnTransformsButton, 'right', 5)], 
                                    attachControl=[(returnTransformsButton, 'top', 5, clearTransformsButton)])

    #Display window
    cmds.showWindow(window)
