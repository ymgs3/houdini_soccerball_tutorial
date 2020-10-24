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