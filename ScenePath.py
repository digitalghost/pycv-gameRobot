# -*- coding: utf-8 -*
class ScenePath:
	"""Auto execute path in scene"""
	#单个路径名称
	name = ""
	#特征点图片文件名
	features = []	
	#点击特征点图片文件名
	touches = []
	#自定义逻辑方法名
	method = ""
	#自定义逻辑方法执行次数
	methodRepeatTime = 0
	#下一个路径的id,默认-1为没有下一个场景路径
	nextPathId = -1
	#当前路径执行前的等待时间
	waitTime = 2
	#当未找到特征点时是否需要继续查找
	needRepeatWhenNotFound = True
	#是否需要重新截图
	needReSnapshots = True

	def __init__(self, pathId):
		self.pathId = pathId


		