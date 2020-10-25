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
hou.playbar.setFrameRange(1,120)
hou.setFrame(1)
toolutils.sceneViewer().setCurrentState("select")
toolutils.sceneViewer().setCurrentState("pose")

soccerball_ctrl_tx = soccerball_ctrl.parm("tx")
soccerball_ctrl_ty = soccerball_ctrl.parm("ty")

key = hou.Keyframe()
key.setFrame(1)
key.setValue(-15)
soccerball_ctrl_tx.setKeyframe(key)

key.setFrame(120)
key.setValue(15)
soccerball_ctrl_tx.setKeyframe(key)
key.setValue(0)
soccerball_ctrl_ty.setKeyframe(key)


# 02
frame_list = [12, 36, 60]
accel = 1.0
for frame in frame_list:
    hou.setFrame(frame)
    key.setFrame(frame)
    key.setValue(0)
    key.setInSlope(-1e+08)
    key.setInAccel(accel)
    key.setSlope(1e+08)
    accel /= 2.0
    key.setAccel(accel)
    if frame == 60:
        key.setSlope(0)
    soccerball_ctrl_ty.setKeyframe(key)

hou.setFrame(1)
frame_list = [1,24, 48]
height = 5.0
for frame in frame_list:
    key.setFrame(frame)
    key.setValue(height)
    key.setInSlope(0)
    key.setInAccel(0.2)
    key.setSlope(0)
    key.setAccel(0.2)
    soccerball_ctrl_ty.setKeyframe(key)
    height /= 2.0

# 04
soccerball_anim.parm("vport_onionskin").set(2)
settings = toolutils.sceneViewer().curViewport().settings()
settings.setOnionSkinning(True)
blue = hou.Color((0, 0, 1.0))
settings.setOnionSkinFramesBeforeCount(3)
settings.setOnionSkinFramesBeforeTint(blue)
red = hou.Color((1.0, 0, 0))
settings.setOnionSkinFramesAfterCount(3)
settings.setOnionSkinFramesAfterTint(red)
print(settings.onionSkinFramesAfterTint())


# 08
key.setInSlope(0)
key.setInAccel(0.2)
key.setSlope(0)
key.setAccel(0.2)
squash_ctrl_ty = squash_ctrl.parm("ty")
frame_list = [1, 24, 48]
value = 0.5
for frame in frame_list:
    key.setFrame(frame)
    key.setValue(value)
    value /= 2.0
    squash_ctrl_ty.setKeyframe(key)


frame_list = [12, 36, 60]
value = -0.5
for frame in frame_list:
    key.setFrame(frame-1)
    key.setValue(0)
    squash_ctrl_ty.setKeyframe(key)
    key.setFrame(frame)
    key.setValue(value)
    value /= 2.0
    squash_ctrl_ty.setKeyframe(key)

key.setFrame(65)
key.setValue(0)
squash_ctrl_ty.setKeyframe(key)

# 全ノードをいい位置に移動
for node in hou.node("/").allSubChildren():
    node.moveToGoodPosition()

# 保存
hou.hipFile.save("soccerball_by_script_09.hip")