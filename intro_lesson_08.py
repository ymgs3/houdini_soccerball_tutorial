import os
# Houdini 上のpythonならhouはデフォルトインポートされているみたいなのでインポート処理を飛ばす
# 環境変数取れたら Houdini　上と判断
if not 'HFS' in os.environ:
    try:
        import hrpyc
        connection, hou = hrpyc.import_remote_module()
    except:
        # 最後に定義されているhouのautocompleteが効くみたいなので例外側でインポート　
        import hou

obj = hou.node("/obj")
geo = hou.node("/obj/soccerball_geo")

# 01
geo_anim = geo.copyTo(obj)
geo_anim.setName("socccerball_anim")

geo.setDisplayFlag(False)
geo_anim.setDisplayFlag(True)

# 02
soccerball_ctrl = obj.createNode("null","soccerball_ctrl")
soccerball_ctrl.setParms({
    "controltype":1,
    "orientation":2,
    "geoscale":4,
})

geo_anim.setInput(0,soccerball_ctrl)
geo_anim.setSelectableInViewport(False)

# 03
matchsize = None
for child in geo_anim.children():
    if child.type().nameComponents()[2] == "matchsize":
        matchsize = child

subdivide = matchsize.inputs()[0]

xform = geo_anim.createNode("xform")

xform.setInput(0,subdivide)
matchsize.setInput(0,xform)

xform_to_ctrl_path = xform.relativePathTo(soccerball_ctrl)

xform.setParmExpressions(
    {
        'rz':'ch("{0}")'.format(xform_to_ctrl_path),
    }
)


# 04
xform.setParmExpressions(
    {
        'rz':'-ch("{0}/tx")*360/(2*$PI*1.1)'.format(xform_to_ctrl_path),
    }
)

# 05
squash_ctrl = obj.createNode("null","squash_ctrl")
squash_ctrl.setParms({
    "controltype":2,
    "geoscale":0.2,
    "ty":2.5,
})

squash_ctrl.parm("pre_xform").set(squash_ctrl.parm("pre_xform").menuItems()[1])
squash_ctrl.parm("pre_xform").pressButton()

# 06
squash_ctrl.setInput(0,soccerball_ctrl)

# 07
null_geo_out = hou.node("/obj/socccerball_anim/GEOMETRY_OUT")

bend = geo_anim.createNode("bend")
bend.setInput(0, matchsize)
null_geo_out.setInput(0, bend)

bend.setParms({
    "limit_deformation":False,
})
# bend.parm("setcaptureregion").pressButton()

bend.setParms({
    "upvectorcontrol":3,
    "upx":0,
    "upy":0,
    "upz":1,
    "dirx":0,
    "diry":1,
    "dirz":0,
    "length":2.2,
    "enablelengthscale":True,
})

bend_to_ctrl_path = bend.relativePathTo(squash_ctrl)
bend.setParmExpressions(
    {
        'lengthscale':'ch("{0}/ty")+1'.format(bend_to_ctrl_path),
    }
)

# 08
soccerball_ctrl.parm("tz").lock(True)
soccerball_ctrl.parm("rx").lock(True)
soccerball_ctrl.parm("ry").lock(True)
soccerball_ctrl.parm("rz").lock(True)
soccerball_ctrl.parm("sx").lock(True)
soccerball_ctrl.parm("sy").lock(True)
soccerball_ctrl.parm("sz").lock(True)

# 09
squash_ctrl.parm("tx").lock(True)
squash_ctrl.parm("tz").lock(True)
squash_ctrl.parm("rx").lock(True)
squash_ctrl.parm("ry").lock(True)
squash_ctrl.parm("rz").lock(True)
squash_ctrl.parm("sx").lock(True)
squash_ctrl.parm("sy").lock(True)
squash_ctrl.parm("sz").lock(True)

# 全ノードをいい位置に移動
for node in hou.node("/").allSubChildren():
    node.moveToGoodPosition()

# 保存
hou.hipFile.save("soccerball_by_script_08.hip")