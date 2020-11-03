import os
# Houdini 上のpythonならhouはデフォルトインポートされているみたいなのでインポート処理を飛ばす
# 環境変数取れたら Houdini　上と判断
if not 'HFS' in os.environ:
    try:
        import hrpyc
        connection, hou = hrpyc.import_remote_module()
        toolutils = connection.modules["toolutils"]
    except:
        # 最後に定義されているhouのautocompleteが効くみたいなので例外側でインポート　
        import hou
        import toolutils

        
geo_out = hou.node("/obj/soccerball_geo/GEOMETRY_OUT")
stage = hou.node("/stage")
backdrop = hou.node("/stage/backdrop")

materiallibrary = None
for child in stage.children():
    if child.type().nameComponents()[2] == "materiallibrary":
        materiallibrary = child

# 01
geo = hou.node("/obj").createNode('geo',"soccerball_sim")
object_merge = geo.createNode("object_merge")
object_merge.parm("objpath1").set(geo_out.path())
object_merge.parm("xformtype").set(1)
matchsize = geo.createNode("matchsize")
matchsize.setInput(0,object_merge)
matchsize.setDisplayFlag(True)

# 02
box = geo.createNode("box")
box.parmTuple("t").set((0,8,-8))
box.parmTuple("r").set((45,45,45))
box.setParms({
    "type":1,
    "scale":6,
    })
box.parmTuple("divrate").set((3,3,3))

# 03
copytopoints = geo.createNode("copytopoints::2.0")
copytopoints.parm("pack").set(True)

mountain = geo.createNode("mountain::2.0")
mountain.setInput(0,box)
mountain.parm("height").set(8)

copytopoints.setInput(0,matchsize)
copytopoints.setInput(1,mountain)
copytopoints.setDisplayFlag(True)

# 04
rbdbulletsolver = geo.createNode("rbdbulletsolver")
rbdbulletsolver.setParms({
    "useground":1,
    "density":10,
    "bounce":1.1,
    "collision_bounce":0.8,
    })
rbdbulletsolver.parm("resetsim").pressButton()

rbdbulletsolver.setInput(0,copytopoints)

# 05
usdexport = geo.createNode("usdexport")
usdexport.parm("trange").set(1)
usdexport.parm("lopoutput").set("$HIP/geo/soccerball_sim.usd")
usdexport.setInput(0,rbdbulletsolver)
usdexport.setDisplayFlag(True)
usdexport.parm("execute").pressButton()

# 06
reference = stage.createNode("reference","soccerball_sim")
reference.parm("filepath1").set("$HIP/geo/soccerball_sim.usd")
reference.setInput(0,backdrop)
reference.setDisplayFlag(True)

# 07
rendergeometrysettings = stage.createNode("rendergeometrysettings")
rendergeometrysettings.parm("primpattern").set("/soccerball_sim/piece*")
rendergeometrysettings.parm("xn__primvarskarmaobjectmblur_control_8sbfg").set(rendergeometrysettings.parm("xn__primvarskarmaobjectmblur_control_8sbfg").menuItems()[0])
rendergeometrysettings.parm("xn__primvarskarmaobjectmblur_7fbfg").set(True)
rendergeometrysettings.parm("xn__primvarskarmaobjectgeosamples_control_e1bfg").set(rendergeometrysettings.parm("xn__primvarskarmaobjectgeosamples_control_e1bfg").menuItems()[0])
rendergeometrysettings.parm("xn__primvarskarmaobjectgeosamples_dobfg").set(2)
rendergeometrysettings.setDisplayFlag(True)

# 08
configureprimitive = stage.createNode("configureprimitive")
configureprimitive.parm("primpattern").set("/soccerball_sim/piece*")
configureprimitive.parm("setinstanceable").set(True)
configureprimitive.parm("instanceable").set(configureprimitive.parm("instanceable").menuItems()[0])
configureprimitive.setInput(0,reference)
rendergeometrysettings.setInput(0,configureprimitive)

# 09
materiallibrary2 = materiallibrary.copyTo(stage)
materiallibrary2.parm("geopath1").set("/soccerball_sim/piece*")
materiallibrary2.setInput(0,rendergeometrysettings)

# 10
domelight = hou.node("/stage/camera2")
domelight.setSelected(True,True)
node = domelight.outputs()
while(len(node) > 0):
    node = node[0]
    node.setSelected(True)
    node = node.outputs()
    
copyNodes = hou.copyNodesTo(hou.selectedNodes(), stage)

# 11
camera = copyNodes[0]
camera.setInput(0,materiallibrary2)
karma = copyNodes[-1]
karma.parm("camera").set(camera.parm("primpath").eval())
karma.parm("picture").set("$HIP/render/soccerbal_sim_$F.exr")
karma.setDisplayFlag(True)
karma.parm("execute").pressButton()


# 全ノードをいい位置に移動
for node in hou.node("/").allSubChildren():
    node.moveToGoodPosition()

# 保存
hou.hipFile.save("soccerball_by_script_12.hip")