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

soccerball_ctrl = hou.node("/obj/soccerball_ctrl")
squash_ctrl = hou.node("/obj/squash_ctrl")
soccerball_anim = hou.node("/obj/soccerball_anim")

# 01 
soccerball_ctrl_ty = soccerball_ctrl.parm("ty")
chop = soccerball_ctrl.findOrCreateMotionEffectsNetwork()
channel = soccerball_ctrl_ty.createClip(chop,"noise_translate_clip",False,False,False,False,False)
channel.parm('range').set(3)
channel.parm('units').set(0)

noise = chop.createNode('noise')
toChannel = noise.relativePathTo(channel)
noise.parm('seed').setExpression('$C')
#noise.parm('period').set(0.89)
#noise.parm('rough').set(0.566)
#noise.parm('amp').set(1.53)
noise.parm('channelname').set('`run("chopls {0}")`'.format(toChannel))
mathNode = chop.createNode('math')
mathNode.parm('chopop').set(1)
mathNode.setInput(0,channel)
mathNode.setInput(1,noise)

# 02
limit = chop.createNode('limit')
limit.parm('type').set(1)
limit.parm('min').set(0)
limit.parm('max').set(5)
limit.setInput(0,mathNode)
limit.setDisplayFlag(True)
limit.setExportFlag(True)

# 03
frameRange = hou.playbar.frameRange()
key = hou.Keyframe()
key.setFrame(frameRange[0])
key.setValue(0)

noise_amp = noise.parm('amp')
noise_amp.setKeyframe(key)
key.setFrame(frameRange[1])
key.setValue(1)
noise_amp.setKeyframe(key)

# 04
scene = toolutils.sceneViewer()
# ビューアの現行Flipbook設定をコピーします。
flipbook_options = scene.flipbookSettings().stash()

# 必要に応じて設定を変更します
# (例えば、フレーム範囲と出力ファイル名を設定します)
flipbook_options.frameRange( (1, 10) )

flipbook_options.output("render/test_$F.pic")

# 修正した設定を使ってFlipbookを生成します。
scene.flipbook(scene.curViewport(), flipbook_options)

# 全ノードをいい位置に移動
for node in hou.node("/").allSubChildren():
    node.moveToGoodPosition()

# 保存
hou.hipFile.save("soccerball_by_script_10.hip")