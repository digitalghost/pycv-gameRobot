# -*- coding: utf-8 -*
import Settings
from Scene import Scene
from ScenePath import ScenePath
from ToolUtils import ToolUtils

class YYSGame(object):
	"""阴阳师游戏自动化脚本"""
	def __init__(self):
		super(YYSGame, self).__init__()

	def yuhun(self, level=1):
		scene = Scene("御魂副本")

		path1 = ScenePath(0)
		path1.name = "点击御魂入口"
		path1.features = ["tpl1_1.png","tpl1_2.png"]
		path1.touches = ["tch1.png"]
		path1.nextPathId = 1
		scene.paths.append(path1)

		path2 = ScenePath(1)
		path2.name = "点击今日御魂(八岐大蛇)"
		path2.features = ["tpl2.png"]
		path2.touches = ["tch2.png"]
		path2.nextPathId = 2
		scene.paths.append(path2)

		path3 = ScenePath(2)
		path3.name = "点击御魂第一层, 并点击挑战"
		path3.features = ["tpl3_%s.png" %str(level)]
		path3.touches = ["tpl3_%s.png" %str(level), "tch4.png"]
		path3.nextPathId = 4
		scene.paths.append(path3)

		path5 = ScenePath(4)
		path5.name = "点击准备"
		path5.features = ["tpl5.png"]
		path5.touches = ["tch5.png"]
		path5.waitTime = 15
		path5.nextPathId = 5
		scene.paths.append(path5)

		path6 = ScenePath(5)
		path6.name = "点击自动攻击"
		path6.features = ["tpl6.png"]
		path6.touches = ["tch6.png"]
		path6.nextPathId = 6
		path6.needRepeatWhenNotFound = False
		scene.paths.append(path6)

		path7 = ScenePath(6)
		path7.name = "点击完成(胜利页面)"
		path7.features = ["tpl7.png"]
		path7.touches = ["tch7.png"]
		path7.waitTime = 120
		path7.nextPathId = 7
		scene.paths.append(path7)

		path8 = ScenePath(7)
		path8.name = "点击完成(打开奖品)"
		path8.features = ["tpl7.png"]
		path8.touches = ["tch7.png"]
		path8.nextPathId = 8
		scene.paths.append(path8)

		path9 = ScenePath(8)
		path9.name = "点击完成(奖品列表)"
		path9.features = ["tpl7.png"]
		path9.touches = ["tch7.png"]
		path9.waitTime = 10
		path9.nextPathId = 2
		scene.paths.append(path9)

		return scene

	def yaoguai(self, chapter=1):
		scene = Scene("发现妖怪")

		path1 = ScenePath(0)
		path1.name = "点击第%s章节" %str(chapter)
		path1.features = ["tpl1_%s.png" %str(chapter)]
		path1.touches = ["tch1_%s.png" %str(chapter)]
		path1.nextPathId = 1
		scene.paths.append(path1)

		path2 = ScenePath(1)
		path2.name = "点击探索"
		path2.features = ["tpl2.png"]
		path2.touches = ["tch2.png"]
		path2.nextPathId = 2
		scene.paths.append(path2)

		path3 = ScenePath(2)
		path3.name = "锁定出战式神"
		path3.features = ["tpl5.png"]
		path3.touches = ["tpl5.png"]
		path3.waitTime = 8
		path3.nextPathId = 3
		path3.needRepeatWhenNotFound = False
		scene.paths.append(path3)

		path4 = ScenePath(3)
		path4.name = "点击攻击某一个妖怪"
		path4.features = ["tpl3.png"]
		path4.touches = ["tch3.png"]
		path4.nextPathId = 5
		scene.paths.append(path4)

		path6 = ScenePath(5)
		path6.name = "点击自动攻击"
		path6.features = ["tpl9.png"]
		path6.touches = ["tch9.png"]
		path6.nextPathId = 6
		path6.needRepeatWhenNotFound = False
		scene.paths.append(path6)

		path7 = ScenePath(6)
		path7.name = "点击完成(胜利页面)"
		path7.features = ["tpl8.png"]
		path7.touches = ["tch8.png"]
		path7.waitTime = 60
		path7.nextPathId = 7
		scene.paths.append(path7)

		path8 = ScenePath(7)
		path8.name = "点击完成(打开奖品)"
		path8.features = ["tpl11.png"]
		path8.touches = ["tch11.png"]
		path8.nextPathId = 8
		scene.paths.append(path8)

		path9 = ScenePath(8)
		path9.name = "点击完成(奖品列表)"
		path9.features = ["tpl12.png"]
		path9.touches = ["tch12.png"]
		path9.nextPathId = 3
		scene.paths.append(path9)

		path9 = ScenePath(9)
		path9.name = "继续寻找妖怪"
		path9.features = ["tpl4.png"]
		path9.waitTime = 15
		path9.method = "findYG2Fight"
		scene.paths.append(path9)

		return scene

	def findYG2Fight(self, scenePath):
		moveLeftTpl = "tpl4.png"
		moveRightTpl = "tpl6.png"
		rightMoveCount = 0
		movingRight = True
		featuresFounded = False
		print "===BEGIN FIND BOSS OR YAOGUAI==="
		while !featuresFounded:
			tplPath = "tpl10.png"
			print "***FEATURE BOSS MATCHING***........Template Path is %s" %tplPath
			exists,region = ToolUtils.checkTemplateExists(tplPath,Settings.LATEST_SCREENSHOT_PATH)
			if exists:
				print "***BOSS MATCHING SUCCEED***" 
				featuresFounded = True
				touchPath = "tch10.png"
				print "***TOUCH BOSS MATCHING***........Touch Path is %s" %touchPath
				centerX,centerY = ToolUtils.getTouchPoint(region)
				device.touch(centerX,centerY,MonkeyDevice.DOWN_AND_UP)
			else:
				tplPath = "tpl3.png"
				print "***FEATURE YAOGUAI MATCHING***........Template Path is %s" %tplPath
				exists,region = ToolUtils.checkTemplateExists(tplPath,Settings.LATEST_SCREENSHOT_PATH)
				if exists:
					print "***YAOGUAI MATCHING SUCCEED***"
					featuresFounded = True
					touchPath = "tch3.png"
					print "***TOUCH YAOGUAI MATCHING***........Touch Path is %s" %touchPath
					centerX,centerY = ToolUtils.getTouchPoint(region)
					device.touch(centerX,centerY,MonkeyDevice.DOWN_AND_UP)
			if featuresFounded:
				scenePath.nextPathId = 6
				break
			else:
				if (rightMoveCount < 6 and movingRight):
					rightMoveCount += 1
					exists,region = ToolUtils.checkTemplateExists(moveRightTpl,Settings.LATEST_SCREENSHOT_PATH)
				else:
					movingRight = False
					rightMoveCount -= 1
					if(rightMoveCount <= 0):
						print "!!!FIND YAOGUAI FAILED"
						break
					exists,region = ToolUtils.checkTemplateExists(moveLeftTpl,Settings.LATEST_SCREENSHOT_PATH)
					if exists:
						print "***TOUCH MOVE***........Touch Path is %s" %moveRightTpl
						centerX,centerY = ToolUtils.getTouchPoint(region)
						device.touch(centerX,centerY,MonkeyDevice.DOWN_AND_UP)
						MonkeyRunner.sleep(5)
						ToolUtils.takeSnapshot(device)
