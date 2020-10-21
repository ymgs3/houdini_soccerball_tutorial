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

geo = hou.node("/obj/soccerball_geo")

# 01
subdivide = None
for child in geo.children():
    if child.isDisplayFlagSet():
        subdivide = child
        
matchsize = geo.createNode("matchsize")
matchsize.parm("justify_y").set(1)
matchsize.setInput(0,subdivide)

null = geo.createNode("null","GEOMETRY_OUT")
null.setInput(0,matchsize)
null.setDisplayFlag(True)

# 02
stage = hou.node("/stage")
sceneimport = stage.createNode("sceneimport")
sceneimport.parm("objects").set("/obj/soccerball_geo")

# 03
sopcreate = stage.createNode("sopcreate","backdrop")

sopnet_create = hou.node(sopcreate.path() + "/sopnet/create")
grid = sopnet_create.createNode("grid")
grid.setParms(
    {
        'sizex':60,
        'sizey':60,
        'tz':-20,
    }
)

bend = sopnet_create.createNode("bend")
bend.setParms(
    {
        'bend':75,
        'originz':-30,
        'dirz':-1,
    }
)
bend.setInput(0,grid)

subdivide = sopnet_create.createNode("subdivide")
subdivide.parm('iterations').set(2)
subdivide.setInput(0,bend)

subdivide.setDisplayFlag(True)

# 04
sopcreate.setInput(0,sceneimport)
sopcreate.setDisplayFlag(True)

camera = stage.createNode("camera")
camera.setParms(
    {
        "ty":2.5,
        "tz":30,
    }
)

camera.setInput(0,sopcreate)
camera.setDisplayFlag(True)

# 05
camera.setParms(
    {
        "aperture":camera.parm("aperture").menuItems()[1],
        "horizontalAperture":19,
        "verticalAperture":9,
    }
)

# 06
domelight = stage.createNode("domelight")
domelight.parm('intensity').set(0.5)
domelight.setInput(0,camera)
domelight.setDisplayFlag(True)
domelight.setCurrent(True)

# ビューポートにカメラを設定する方法がわからない
#pane = hou.ui.curDesktop().paneTabOfType(hou.paneTabType.SceneViewer)
#viewports = pane.viewports()
#settings = viewports[2].settings()
#settings.setCamera(camera)


# 07
light = stage.createNode("light")
light.setParms(
    {
        "tx":5,
        "ty":5,
        "tz":5,
    }
)
light.setInput(0,domelight)


# 08
light2 = stage.createNode("light")
light2.setParms(
    {
        "tx":-5,
        "ty":5,
        "tz":5,
    }
)
light2.setInput(0,light)

# 08
lightmixer = stage.createNode("lightmixer")
lightmixer.setInput(0,light2)
# 編集できる状態にする方法がわからない
#lightmixer.parm("setting_layout").set(
#    '[{"controls": ["buttons"], "rgb": [55, 55, 55], "prim_path": "{0}", "path": "{0}", "type": "LightItem", "contents": []}, {"controls": ["buttons"], "rgb": [55, 55, 55], "prim_path": "{1}", "path": "{1}", "type": "LightItem", "contents": []}, {"controls": ["buttons"], "rgb": [55, 55, 55], "prim_path": "{2}", "path": "{2}", "type": "LightItem", "contents": []}]'.format(domelight.parm("primpath").eval(),light.parm("primpath").eval(),light2.parm("primpath").eval())
#)
lightmixer.setDisplayFlag(True)


# 全ノードをいい位置に移動
for node in hou.node("/").allSubChildren():
    node.moveToGoodPosition()

# 保存
hou.hipFile.save("soccerball_by_script_06.hip")