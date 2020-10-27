import os
# Houdini 上のpythonならhouはデフォルトインポートされているみたいなのでインポート処理を飛ばす
# 環境変数取れたら Houdini　上と判断
if not 'HFS' in os.environ:
    try:
        import hrpyc
        connection, hou = hrpyc.import_remote_module()
        toolutils = connection.modules["toolutils"]
        soputils = connection.modules["soputils"]
    except:
        # 最後に定義されているhouのautocompleteが効くみたいなので例外側でインポート　
        import hou
        import toolutils
        import soputils

soccerball_anim = hou.node("/obj/soccerball_anim")
geo_out = hou.node("/obj/soccerball_anim/GEOMETRY_OUT")
stage = hou.node("/stage")
backdrop = hou.node("/stage/backdrop")

materiallibrary = None
for child in stage.children():
    if child.type().nameComponents()[2] == "materiallibrary":
        materiallibrary = child

# 01
geo = hou.node("/obj").createNode('geo',"extract_object1")
object_merge = geo.createNode("object_merge")
object_merge.parm("objpath1").set(geo_out.path())
object_merge.parm("xformtype").set(1)

usdexport = geo.createNode("usdexport")
usdexport.parm("trange").set(1)
usdexport.parm("lopoutput").set("$HIP/geo/soccerball_anim.usd")
usdexport.setInput(0,object_merge)
usdexport.parm("execute").pressButton()

# 02
reference = stage.createNode("reference","soccerball_anim")
reference.parm("filepath1").set("$HIP/geo/soccerball_anim.usd")
reference.setInput(0,backdrop)
reference.setDisplayFlag(True)

# 03
materiallibrary2 = materiallibrary.copyTo(stage)
materiallibrary2.parm("geopath1").set("/soccerball_anim/mesh_0")
materiallibrary2.setInput(0,reference)

# 04
xform = stage.createNode("xform")
xform.parm("tx").set(35)
xform.parm("tx").set(-1.7)
xform.parm("ry").set(170)
xform.parm("primpattern").set("/soccerball_anim/mesh_0")
xform.setInput(0,materiallibrary2)

# 05
camera = stage.createNode("camera")
camera.setParms(
    {
        "ty":11,
        "tz":81,
        "rx":-3,
        "ry":-3.7,
        "aperture":camera.parm("aperture").menuItems()[1],
        "horizontalAperture":19,
        "verticalAperture":9,
    }
)
camera.setInput(0,xform)

# 06
domelight = hou.node("/stage/domelight1")
domelight.setSelected(True,True)
node = domelight.outputs()
while(len(node) > 0):
    node = node[0]
    node.setSelected(True)
    node = node.outputs()
    
copyNodes = hou.copyNodesTo(hou.selectedNodes(), stage)

copyNodes[0].setInput(0,camera)
copyNodes[-1].setDisplayFlag(True)

# 07 
rendergeometrysettings = stage.createNode("rendergeometrysettings")

for parm in rendergeometrysettings.allParms():
    print(parm.name())

rendergeometrysettings.parm("xn__primvarskarmaobjectmblur_control_8sbfg").set(rendergeometrysettings.parm("xn__primvarskarmaobjectmblur_control_8sbfg").menuItems()[0])
rendergeometrysettings.parm("xn__primvarskarmaobjectmblur_7fbfg").set(True)
rendergeometrysettings.parm("xn__primvarskarmaobjectgeosamples_control_e1bfg").set(rendergeometrysettings.parm("xn__primvarskarmaobjectgeosamples_control_e1bfg").menuItems()[0])
rendergeometrysettings.parm("xn__primvarskarmaobjectgeosamples_dobfg").set(2)
rendergeometrysettings.setInput(0,reference)
materiallibrary2.setInput(0,rendergeometrysettings)

# 08
karma = copyNodes[-1]
karma.parm("camera").set(camera.parm("primpath").eval())
karma.parm("trange").set(karma.parm("trange").menuItems()[1])
karma.parm("picture").set("$HIP/render/soccerbal_anim_$F.exr")
karma.parm("execute").pressButton()


# 全ノードをいい位置に移動
for node in hou.node("/").allSubChildren():
    node.moveToGoodPosition()

# 保存
hou.hipFile.save("soccerball_by_script_11.hip")