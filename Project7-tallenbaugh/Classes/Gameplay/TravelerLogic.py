import math
from enum import Enum
from panda3d.core import NodePath, Vec3
from direct.task import Task

from Classes.Gameplay.SpaceJamPandaBase import SpaceJamBase
from direct.showbase.DirectObject import DirectObject
from direct.interval.Interval import Interval
from direct.interval.LerpInterval import LerpPosInterval, LerpHprInterval
from direct.interval.IntervalGlobal import Sequence


class TravelerRotationStyle(Enum):
    AlwaysLookAtCurrentPoint = 0
    AlwaysLookAtNextPoint = 1
    StopAndRotateAtEachPoint = 2


class SimplePointBasedTravelTask(DirectObject):
    points: list[Vec3]  # Raw input points
    intervals: list[LerpPosInterval]
    startPoints: list[Vec3]  # "Start Point" of each interval step
    endPoints: list[Vec3]  # "End Point" of each interval step

    def __init__(
        self,
        unique_name: str,
        travelling_node: NodePath,
        # If points_of_travel first and last point are the same, we will loop.
        # If they are different, we will ping-pong
        points_of_travel: list[Vec3],
        duration_of_trip: float,  # seconds
        start_immediately: bool = True,
        # If negative, infinite.
        number_of_cycles: int = -1,
        rotation_type: TravelerRotationStyle = TravelerRotationStyle.AlwaysLookAtCurrentPoint,
    ):
        DirectObject.__init__(self)
        self.points = points_of_travel
        self.cycles = number_of_cycles
        self.traveler = travelling_node
        self.tripDuration = duration_of_trip
        self.rotType = rotation_type
        if len(points_of_travel) < 2:
            self.closedLoop = False
        else:
            firstPoint = self.points[0]
            lastPoint = self.points[len(self.points) - 1]
            self.closedLoop = firstPoint == lastPoint

        self._prepareTravelSequence(unique_name)

        self.accept(unique_name + "_SequenceDone", self.sequenceIsDone)
        self.tripSequence.setDoneEvent(unique_name + "_SequenceDone")
        if start_immediately:
            self.tripSequence.loop()

    def _getNextStepIndex(self, stepIndex: int):
        if stepIndex >= (len(self.intervals) - 1):
            return 0

        return stepIndex + 1

    def intervalIsDone(self, stepIndex: int):
        if self.rotType == TravelerRotationStyle.AlwaysLookAtCurrentPoint:
            nextIndex = self._getNextStepIndex(stepIndex)
            self.traveler.lookAt(self.endPoints[nextIndex], Vec3.up())
        print("Step " + str(stepIndex) + " finished!")

    def sequenceIsDone(self):
        print("Sequence finished!")

    def _posIntervalBetweenPoints(
        self, stepIndex: int, a: Vec3, b: Vec3, duration: float, unique_name: str
    ):
        self.accept(
            unique_name + "_Step_" + str(stepIndex), self.intervalIsDone, [stepIndex]
        )
        interval = LerpPosInterval(
            self.traveler, duration, b, a, None, "noBlend", 1, 1, unique_name
        )
        interval.setDoneEvent(unique_name + "_Step_" + str(stepIndex))
        return interval

    def _prepareTravelSequence(self, unique_name: str):
        # Prepare sequence of intervals
        self.tripSequence = Sequence(name=unique_name + "Seq")

        if len(self.points) < 2:
            # Nowhere to go!
            return

        self.intervals = []
        self.startPoints = []
        self.endPoints = []
        step_duration = (
            self.tripDuration / len(self.points)
            if self.closedLoop
            else self.tripDuration / ((len(self.points) * 2) - 1)
        )
        step_number = -1
        for i in range(len(self.points) - 2):
            step_number = step_number + 1
            a = self.points[i]
            b = self.points[i + 1]
            self.intervals.append(
                self._posIntervalBetweenPoints(
                    step_number, a, b, step_duration, unique_name
                )
            )
            self.startPoints.append(a)
            self.endPoints.append(b)
        # Intervals above get us to the final point.
        # If we are a closed loop, this is all we need.
        if self.closedLoop:
            step_number = step_number + 1
            self.intervals.append(
                self._posIntervalBetweenPoints(
                    step_number,
                    self.points[len(self.points) - 2],
                    self.points[0],
                    step_duration,
                    unique_name,
                )
            )
            self.startPoints.append(self.points[len(self.points) - 2])
            self.endPoints.append(self.points[0])
        else:
            for i in reversed(range(len(self.points) - 1)):
                if i == 0:
                    break
                step_number = step_number + 1
                a = self.points[i]
                b = self.points[i - 1]
                self.intervals.append(
                    self._posIntervalBetweenPoints(
                        step_number, a, b, step_duration, unique_name
                    )
                )
                self.startPoints.append(a)
                self.endPoints.append(b)

        for i in self.intervals:
            self.tripSequence.append(i)

    # Define a procedure to move the camera.
    def alwaysLookAtTask(self, task):
        # self.tripSequence.interval
        return Task.cont
