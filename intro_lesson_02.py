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
platonic = geo.createNode('platonic')
platonic.parm('type').set(5)

box = None
polyextrude = None
subdivide = None
for child in geo.children():
    if child.type().nameComponents()[2] == "polyextrude":
        polyextrude = child
    elif child.type().nameComponents()[2] == "subdivide":
        subdivide = child
    elif child.type().nameComponents()[2] == "box":
        box = child

polyextrude.setInput(0,platonic)

if box:
    box.destroy()

# 02
polyextrude.parm('dist').set(0.06)


# 03
# https://www.sidefx.com/ja/docs/houdini/hom/hou/GeometryViewportDisplaySet.html
# https://www.sidefx.com/ja/docs/houdini/hom/hou/glShadingType.html
# ジオメトリビューアの参照を取得します。
pane = hou.ui.curDesktop().paneTabOfType(hou.paneTabType.SceneViewer)
# 表示設定を取得します。
settings = pane.curViewport().settings()
# オブジェクト用のGeometryViewportDisplaySetを取得します。
tmplset = settings.displaySet(hou.displaySetType.SelectedObject)
# このサブセットのシェーディングモードをワイヤーフレーム表示にするようにHoudiniに伝えます。
tmplset.setShadedMode(hou.glShadingType.SmoothWire)



# 全ノードをいい位置に移動
for node in hou.node("/").allSubChildren():
    node.moveToGoodPosition()

# 保存
hou.hipFile.save("soccerball_by_script_02.hip")