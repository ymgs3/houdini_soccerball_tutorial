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

stage = hou.node("/stage")

# 01
materiallibrary = stage.createNode("materiallibrary")

backdrop = hou.node("/stage/backdrop")
sceneimport = None
camera = None
lightmixer = None
for child in stage.children():
    if child.type().nameComponents()[2] == "sceneimport":
        sceneimport = child
    elif child.type().nameComponents()[2] == "lightmixer":
        lightmixer = child
camera = sceneimport.outputs()[0]

camera.setInput(0,materiallibrary)
materiallibrary.setInput(0,sceneimport)

principledshader = materiallibrary.createNode("principledshader::2.0","soccerball_mat")
principledshader.setParms({
    "basecolorr":1.0,
    "basecolorg":1.0,
    "basecolorb":1.0,
})

principledshader2 = principledshader.copyTo(materiallibrary)
principledshader2.setName("backdrop_mat")
principledshader2.setParms({
    "basecolorr":0.0,
    "basecolorg":0.2,
    "basecolorb":0.0,
})

# 02
materiallibrary.parm("materials").set(0)
materiallibrary.parm("fillmaterials").pressButton()

# このパスの取得方法がわからない
materiallibrary.parm("geopath1").set("/soccerball_geo/mesh_0")
materiallibrary.parm("geopath2").set("/backdrop/mesh_0")

# 03
principledshader.setParms({
    "basecolor_useTexture":True,
    "basecolor_texture":"$JOB/tex/soccerball_color.rat",
})

# 04
principledshader.setParms({
    "rough_useTexture":True,
    "rough_texture":"$JOB/tex/soccerball_rough.rat",
    "reflect_useTexture":True,
    "reflect_texture":"$JOB/tex/soccerball_reflect.rat",
    "baseBumpAndNormal_enable":True,
    "baseNormal_texture":"$JOB/tex/soccerball_normal.rat",
    "baseNormal_scale":0.5,
})

# 05
edit = stage.createNode("edit")

edit.setInput(0,sceneimport)
materiallibrary.setInput(0,edit)
# このパスの取得方法がわからない
edit.parm("primpattern").set("/soccerball_geo/mesh_0")
edit.parm("rx").set(0.5)
edit.parm("apply").pressButton()

# 06
principledshader2.setParms({
    "basecolorr":1.0,
    "basecolorg":1.0,
    "basecolorb":1.0,
    "basecolor_useTexture":True,
    "basecolor_texture":"$JOB/tex/backdrop_color.rat",
    "reflect_useTexture":True,
    "reflect_texture":"$JOB/tex/backdrop_reflect.rat",
})

# 07
sopnet_create = hou.node(backdrop.path() + "/sopnet/create")
grid = None
bend = None
for child in sopnet_create.children():
    if child.type().nameComponents()[2] == "grid":
        grid = child
    elif child.type().nameComponents()[2] == "bend":
        bend = child
uvquickshade = sopnet_create.createNode("uvquickshade")
uvquickshade.setInput(0,grid)

uvproject = sopnet_create.createNode("uvproject")
uvproject.setInput(0,uvquickshade)
bend.setInput(0,uvproject)

uvproject.parm("initbbox").pressButton()
uvproject.setParms({
    "vrange1":0,
    "vrange2":-1,
})

# 08
null = stage.createNode("null","SHOT_01")
null.setInput(0,lightmixer)

karma = stage.createNode("karma")
karma.setInput(0,null)
karma.setDisplayFlag(True)
karma.parm("picture").set("$HIP/render/soccerball_test.exr")
karma.parm("execute").pressButton()


# 全ノードをいい位置に移動
for node in hou.node("/").allSubChildren():
    node.moveToGoodPosition()

# 保存
hou.hipFile.save("soccerball_by_script_07.hip")