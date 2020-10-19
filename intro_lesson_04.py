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
polyextrude = None
ray = None
for child in geo.children():
    if child.type().nameComponents()[2] == "polyextrude":
        polyextrude = child
    elif child.type().nameComponents()[2] == "ray":
        ray = child

block_begin = geo.createNode('block_begin')
block_end = geo.createNode('block_end')
rel_begin_path = block_end.relativePathTo(block_begin)
rel_end_path = block_begin.relativePathTo(block_end)
block_begin.parm("method").set(1)
block_begin.parm("blockpath").set(rel_end_path)
block_end.parm('itermethod').set(1)
block_end.parm('method').set(1)
block_end.parm('class').set(0)
block_end.parm('attrib').set("patches")
block_end.parm('blockpath').set(rel_begin_path)
block_end.parm('templatepath').set(rel_begin_path)

block_begin.setInput(0,ray)
polyextrude.setInput(0,block_begin)
block_end.setInput(0,polyextrude)

# 03
fuse = geo.createNode('fuse')
fuse.setInput(0,block_end)

subdivide = geo.createNode('subdivide')
subdivide.parm('iterations').set(2)
subdivide.setInput(0,fuse)

subdivide.setDisplayFlag(True)

# 04
polyextrude.parm('dist').set(0.1)
polyextrude.parm('inset').set(-0.02)

ifd = hou.node("/out").createNode('ifd')
ifd.parm('vm_usemaxthreads').set(2)

# TODO Render Region 

# 全ノードをいい位置に移動
for node in hou.node("/").allSubChildren():
    node.moveToGoodPosition()
    
# 保存
hou.hipFile.save("soccerball_by_script_04.hip")
