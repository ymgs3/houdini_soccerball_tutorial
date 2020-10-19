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

hou.hipFile.clear(True)

# 01
geo = hou.node("/obj").createNode('geo',"box_object")
box = geo.createNode('box')
box.parm('sizez').set(2)

# 04
polyextrude = geo.createNode('polyextrude')
polyextrude.parm('dist').set(0.4)
polyextrude.parm('splittype').set(0)
polyextrude.setInput(0,box)

# 05
subdivide = geo.createNode('subdivide')
subdivide.parm('iterations').set(2)
subdivide.setInput(0,polyextrude)

# 06
currentNode = subdivide
currentNode.setDisplayFlag(True)

# 全ノードをいい位置に移動
for node in hou.node("/").allSubChildren():
    print("{0}:{1}".format(node.path(), node.type().nameComponents()))
    node.moveToGoodPosition()

    
# 07
print(hou.hipFile.path())
hou.hipFile.save("soccerball_by_script_01.hip")