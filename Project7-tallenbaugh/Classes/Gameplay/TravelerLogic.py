import math
from enum import Enum
from panda3d.core import NodePath, Vec3, Quat, look_at
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
    intervals: list[Interval]
    startPoints: list[Vec3]  # "Start Point" of each interval step
    endPoints: list[Vec3]  # "End Point" of each interval step

    def __init__(
        self,
        base: SpaceJamBase,
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
        self.base = base
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
        if stepIndex >= (len(self.startPoints) - 1):
            return 0
        return stepIndex + 1

    def _getPrevStepIndex(self, stepIndex: int):
        if stepIndex == 0:
            return len(self.startPoints) - 1
        return stepIndex - 1

    def intervalIsDone(self, stepIndex: int):
        self.currentStepIndex = self._getNextStepIndex(stepIndex)
        if self.rotType == TravelerRotationStyle.AlwaysLookAtCurrentPoint:
            self.traveler.lookAt(self.endPoints[self.currentStepIndex], Vec3.up())
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

    def _hprIntervalBetweenPoints(
        self,
        stepIndex: int,
        a_0: Vec3,
        a: Vec3,
        b: Vec3,
        duration: float,
        unique_name: str,
    ):
        self.accept(
            unique_name + "_Step_" + str(stepIndex), self.intervalIsDone, [stepIndex]
        )
        quat_a = Quat()
        look_at(quat_a, a_0 - a, Vec3.up())
        quat_b = Quat()
        look_at(quat_b, a - b, Vec3.up())
        interval = LerpHprInterval(
            self.traveler,
            duration,
            quat_b.getHpr(),
            quat_a.getHpr(),
            None,
            None,
            "noBlend",
            1,
            1,
            unique_name,
        )
        interval.setDoneEvent(unique_name + "_Step_" + str(stepIndex))
        return interval

    def _prepareTravelSequence(self, unique_name: str):
        # Prepare sequence of intervals
        self.tripSequence = Sequence(name=unique_name + "Seq")

        if len(self.points) < 2:
            # Nowhere to go!
            return
        self.currentStepIndex = 0
        self.intervals = []
        self.startPoints = []
        self.endPoints = []

        step_duration = (
            self.tripDuration / len(self.points)
            if self.closedLoop
            else self.tripDuration / ((len(self.points) * 2) - 1)
        )
        if self.rotType == TravelerRotationStyle.StopAndRotateAtEachPoint:
            step_duration = step_duration * 0.5

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

        # RotateAtEachPoint style needs rotation intervals in between each position interval.
        if self.rotType == TravelerRotationStyle.StopAndRotateAtEachPoint:
            rot_index = 0
            final_interval_count = len(self.intervals) * 2
            pos_intervals = self.intervals
            self.intervals = []
            while len(self.intervals) < final_interval_count:
                step_number = step_number + 1
                print(
                    "HPR Interval at index "
                    + str(rot_index)
                    + ", prevStep "
                    + str(self._getPrevStepIndex(rot_index))
                )
                self.intervals.append(pos_intervals[rot_index])
                self.intervals.append(
                    self._hprIntervalBetweenPoints(
                        step_number,
                        self.startPoints[self._getPrevStepIndex(rot_index)],
                        self.startPoints[rot_index],
                        self.endPoints[rot_index],
                        step_duration,
                        unique_name,
                    )
                )
                rot_index = rot_index + 1

        # Finally populate the sequence with all the intervals.
        for i in self.intervals:
            self.tripSequence.append(i)

        # Some rotation types are task-based.
        if self.rotType == TravelerRotationStyle.AlwaysLookAtNextPoint:
            self.base.taskMgr.add(
                self.alwaysLookAtNextPointTask, unique_name + "_AlwaysLookAtNextPoint"
            )

    # Define a procedure to move the camera.
    def alwaysLookAtNextPointTask(self, task: Task):
        self.traveler.lookAt(
            self.endPoints[self._getNextStepIndex(self.currentStepIndex)], Vec3.up()
        )
        return task.cont
