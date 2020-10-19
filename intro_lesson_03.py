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


geo = hou.node("/obj/box_object")

# 01
platonic = None
polyextrude = None
subdivide = None
for child in geo.children():
    if child.type().nameComponents()[2] == "polyextrude":
        polyextrude = child
    elif child.type().nameComponents()[2] == "subdivide":
        subdivide = child
    elif child.type().nameComponents()[2] == "platonic":
        platonic = child

subdivide.setInput(0,None)

# 02
subdivide.setInput(0,platonic)
polyextrude.setInput(0,subdivide)


# 03
sphere = geo.createNode('sphere')
ray = geo.createNode('ray')

ray.setInput(0,subdivide)
ray.setInput(1,sphere)

polyextrude.setInput(0,ray)

# 04
polyextrude.setDisplayFlag(True)
polyextrude.parm('splittype').set(1)

# 05
attribcreate = geo.createNode('attribcreate')
attribcreate.parm('name1').set("patches")
attribcreate.parm('class1').set(1)
attribcreate.setParmExpressions(
    {
        'value1v1':'@primnum',
    }
)
attribcreate.setInput(0,platonic)
subdivide.setInput(0,attribcreate)

# 06
visualizer = hou.viewportVisualizers.createVisualizer(
    hou.viewportVisualizers.type('vis_marker'),
    hou.viewportVisualizerCategory.Scene)
visualizer.setName("Patch_Numbers")
visualizer.setLabel("Patch_Numbers")
visualizer.setParm("class",2)
visualizer.setParm("attrib", "patches")
pane = hou.ui.curDesktop().paneTabOfType(hou.paneTabType.SceneViewer)
visualizer.setIsActive(True,pane.curViewport())


# 07
visualizer.setIsActive(False,pane.curViewport())

# 全ノードをいい位置に移動
for node in hou.node("/").allSubChildren():
    node.moveToGoodPosition()
    
# 保存
hou.hipFile.save("soccerball_by_script_03.hip")