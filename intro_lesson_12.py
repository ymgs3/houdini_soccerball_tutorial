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
rbdbulletsolver.setDisplayFlag(True)


# 全ノードをいい位置に移動
for node in hou.node("/").allSubChildren():
    node.moveToGoodPosition()

# 保存
hou.hipFile.save("soccerball_by_script_12.hip")