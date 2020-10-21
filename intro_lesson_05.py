import os
# Houdini 上のpythonならhouはデフォルトインポートされているみたいなのでインポート処理を飛ばす
# 環境変数取れたら Houdini　上と判断
if not 'HFS' in os.environ:
    try:
        import hrpyc
        connection, hou = hrpyc.import_remote_module()
        toolutils = connection.modules["toolutils"]
        print(toolutils.sceneViewer())
    except:
        # 最後に定義されているhouのautocompleteが効くみたいなので例外側でインポート　
        import hou
        import toolutils

geo = hou.node("/obj/soccerball_geo")

# 01
pane = hou.ui.curDesktop().paneTabOfType(hou.paneTabType.SceneViewer)
pane.setViewportLayout(hou.geometryViewportLayout.DoubleSide)
viewports = pane.viewports()
# 右
viewports[3].changeType(hou.geometryViewportType.Perspective)
# 左
viewports[2].changeType(hou.geometryViewportType.UV)


# 02
block_end = None
for child in geo.children():
    if child.type().nameComponents()[2] == "block_end":
        block_end = child

block_end_output = block_end.outputs()
uvquicshade = geo.createNode('uvquickshade')
uvquicshade.setInput(0,block_end)

for node in block_end_output:
    node.setInput(0,uvquicshade)

# 03
uvflatten = geo.createNode('uvflatten::3.0')
uvflatten.setInput(0,uvquicshade)

for node in block_end_output:
    node.setInput(0,uvflatten)

# 04 
uvquicshade.parm("texture").set("$JOB/tex/soccerball_color.rat")

# 05
# 背景画像の設定こんな感じだと思うがうまく動かない。。。
settings = viewports[2].settings()
settings.backgroundImage(hou.viewportBGImageView.UV).setImageSource(hou.getenv("JOB") + "/tex/soccerball_color.rat")
settings.setDisplayBackgroundImage(True)

# 06
# 同じパッチので中央に近いやつを使う
bbox = None
for prim in uvflatten.geometry().prims():
    if 0 == prim.attribValue("patches"):
        if bbox == None:
            bbox = prim.boundingBox()
        else:
            bbox.enlargeToContain(prim.boundingBox())
nearestPoint = uvflatten.geometry().nearestPoint(bbox.center())
print(nearestPoint)

uvMin = [1,1]
uvMax = [0,0]
nearestPrim = uvflatten.geometry().nearestPrim(bbox.center())

for vertex in nearestPrim[0].vertices():
    uv = vertex.attribValue("uv")
    for i in range(0,2):
        if uvMin[i] > uv[i]:
            uvMin[i] = uv[i]
        if uvMax[i] < uv[i]:
            uvMax[i] = uv[i]

print(nearestPrim[0].vertices())

for prim in nearestPoint.prims():
    print(prim.number())
for vertex in nearestPoint.vertices():
    print(vertex.number())

prim = nearestPoint.prims()[0]
vertex = nearestPoint.vertices()[0]
vertex2 = nearestPoint.vertices()[1]

uv = vertex.attribValue("uv")
uv2 = vertex2.attribValue("uv")

# uvの値をどう求めているかわかないので仮
u = (uvMax[0] - uvMin[0]) / 1.5
v = (uvMax[1] - uvMin[1]) / 1.5
print(uv)
print(uv2)
print(uvMax)
print(uvMin)
uvflatten.parm("pins").set(1)
uvflatten.parm("primvert0x").set(prim.number())
uvflatten.parm("primvert0y").set(vertex.number())

# 07
uvflatten.parm("pinuv0x").set(0.5)
uvflatten.parm("pinuv0y").set(0.5)
uvflatten.parm("pinrefuv0x").set(0.5 + u)
uvflatten.parm("pinrefuv0y").set(0.5 + v)
#uvflatten.parm("pinrefuv0x").set(uv[0])
#uvflatten.parm("pinrefuv0y").set(uv[1])

# 08
uvflatten.parm("lpins").set(1)
uvflatten.parm("lpinuv0x").set(0.5)
uvflatten.parm("lpinuv0y").set(0.5)
uvflatten.parm("lpinrefuv0x").set(0.5 + u)
uvflatten.parm("lpinrefuv0y").set(0.5 + v)

# uv flatten のツールを選ぶ まではできるが Repackの呼び方がわからない・・・
uvflatten.setCurrent(True)
toolutils.sceneViewer().enterCurrentNodeState()

# 全ノードをいい位置に移動
for node in hou.node("/").allSubChildren():
    node.moveToGoodPosition()
    

# 保存
hou.hipFile.save("soccerball_by_script_05.hip")