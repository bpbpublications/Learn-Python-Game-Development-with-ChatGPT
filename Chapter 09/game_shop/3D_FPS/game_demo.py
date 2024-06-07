# filename: game_demo.py

from panda3d.core import Point3, Vec3, DirectionalLight
from panda3d.core import AmbientLight
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from math import sin, cos
from panda3d.core import CollisionTraverser,CollisionNode
from panda3d.core import CollisionHandlerQueue,CollisionRay
from panda3d.core import Filename,AmbientLight,DirectionalLight
from panda3d.core import PandaNode,NodePath,Camera,TextNode
from panda3d.core import Point3,Vec3,Vec4,BitMask32
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import PointLight
from panda3d.core import Fog
from direct.task.Task import Task
from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from math import sin, cos
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Disable the camera trackball controls.
        self.disableMouse()

        # Load the environment model.
        self.environ = self.loader.loadModel("models/environment")
        self.environ.reparentTo(self.render)

        # Scale and position the model.
        self.environ.setScale(0.25, 0.25, 0.25)
        self.environ.setPos(-8, 42, 0)

        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "spinCameraTask")

        # Add the move task.
        self.taskMgr.add(self.move, "moveTask")

        # Define a key map.
        self.keyMap = {"left":0, "right":0, "forward":0, "backward":0}

        # Bind the keys.
        self.accept("w", self.setKey, ["forward", 1])
        self.accept("w-up", self.setKey, ["forward", 0])
        self.accept("s", self.setKey, ["backward", 1])
        self.accept("s-up", self.setKey, ["backward", 0])
        self.accept("a", self.setKey, ["left", 1])
        self.accept("a-up", self.setKey, ["left", 0])
        self.accept("d", self.setKey, ["right", 1])
        self.accept("d-up", self.setKey, ["right", 0])

    # Records the state of the arrow keys.
    def setKey(self, key, value):
        self.keyMap[key] = value

    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        if self.mouseWatcherNode.hasMouse():
            x = self.mouseWatcherNode.getMouseX()
            y = self.mouseWatcherNode.getMouseY()
            self.camera.setHpr(x * -60, y * 60, 0)
        return Task.cont

    # Define a procedure to move the 'player'.
    def move(self, task):
        elapsed = globalClock.getDt()
        if self.keyMap["left"]:
            self.camera.setX(self.camera, -elapsed*10)
        if self.keyMap["right"]:
            self.camera.setX(self.camera, elapsed*10)
        if self.keyMap["forward"]:
            self.camera.setY(self.camera, elapsed*10)
        if self.keyMap["backward"]:
            self.camera.setY(self.camera, -elapsed*10)
        return Task.cont

app = MyApp()
app.run()