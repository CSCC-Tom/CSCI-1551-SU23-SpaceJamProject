from pandac.PandaModules import Vec3
from direct.showbase.DirectObject import DirectObject
from Classes.GameObjects.ModelWithCollider import ModelWithSphereCollider
from direct.interval.LerpInterval import LerpPosInterval
from typing import Callable
from Classes.Gameplay.SpaceJamPandaBase import SpaceJamBase


class ProjectileObject(DirectObject):
    """ModelWithSphereCollider projectile that will use an Interval to move and will detect collision / flight-lifecycle events in a basic way"""

    flightMovementInterval: LerpPosInterval = {}
    prepared = False
    commenced = False

    def __init__(
        self,
        base: SpaceJamBase,
        model_path: str,
        node_name: str,
        flight_concluded_callback: Callable[[], None],
    ):
        DirectObject.__init__(self)
        self.modelColliderNode = ModelWithSphereCollider(
            base, model_path, base.render, node_name
        )
        self.flightConcludedCallback = flight_concluded_callback

    def prepareFlight(
        self, flightStartPos: Vec3, flightDir: Vec3, flightDistance: float
    ):
        self.modelColliderNode.modelNode.setPos(flightStartPos)
        projectileTargetPos = flightStartPos + (flightDir * flightDistance)
        self.flightMovementInterval = LerpPosInterval(
            self.modelColliderNode.modelNode,
            2,
            projectileTargetPos,
            flightStartPos,
            None,
            "noBlend",
            1,
            1,
            "projectileFireInterval",
        )

        self.prepared = True

    def commenceFlight(self):
        if not self.prepared:
            raise AssertionError(
                "ProjectileObject.commenceFlight called, but did not call prepareFlight first! Nothing happened."
            )
        self.acceptOnce("Flight Concluded", self.concludeFlight, [False])
        self.flightMovementInterval.setDoneEvent("Flight Concluded")
        self.flightMovementInterval.start()
        self.commenced = True

    def concludeFlight(self, interrupted: bool):
        if not self.commenced:
            raise AssertionError(
                "ProjectileObject.concludeFlight called, but did not call commenceFlight first! Nothing happened."
            )
        self.flightMovementInterval.pause()
        # Stick the "concluded" projectile somewhere far away so we don't see it.
        self.modelColliderNode.modelNode.setPos((9000, 9000, 9000))
        # Call back up to whatever needs to know about the flight being over
        if interrupted == False:
            self.flightConcludedCallback()
