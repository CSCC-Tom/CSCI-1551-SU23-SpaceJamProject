from enum import Enum
from direct.showbase.DirectObject import DirectObject
from direct.interval.Interval import Interval
from direct.interval.LerpInterval import LerpPosInterval, LerpHprInterval
from direct.interval.IntervalGlobal import Sequence
from direct.task import Task
from typing import Callable

from panda3d.core import NodePath, Vec3, Quat, look_at
from Classes.Gameplay.SpaceJamPandaBase import SpaceJamBase


class TravelerRotationStyle(Enum):
    Cycle = -1  # Special value used by the TravelTask
    AlwaysLookAtCurrentPoint = 0
    AlwaysLookAtNextPoint = 1
    StopAndRotateAtEachPoint = 2


class TravelPointSequence:
    intervals: list[Interval]
    startPoints: list[Vec3]  # "Start Point" of each interval step
    endPoints: list[Vec3]  # "End Point" of each interval step

    def __init__(
        self,
        unique_name: str,
        points: list[Vec3],
        duration: float,
        event_accept: Callable[[str, Callable, []], None],
        traveler: NodePath,
        rotation_type: TravelerRotationStyle,
        interval_done_callback: Callable[[int], None],
    ):
        self.uName = unique_name
        self.accept = event_accept
        self.intervalDoneCB = interval_done_callback
        self.traveler = traveler
        self.rotType = rotation_type
        # Prepare sequence of intervals
        self.seq = Sequence(name=unique_name + "Seq")
        if len(points) < 2:
            self.closedLoop = False
        else:
            firstPoint = points[0]
            lastPoint = points[len(points) - 1]
            self.closedLoop = firstPoint == lastPoint

        self.currentStepIndex = 0
        self.intervals = []
        self.startPoints = []
        self.endPoints = []

        self.stepDuration = (
            duration / len(points)
            if self.closedLoop
            else duration / ((len(points) * 2) - 1)
        )
        if self.rotType == TravelerRotationStyle.StopAndRotateAtEachPoint:
            self.stepDuration = self.stepDuration * 0.5

        step_number = -1
        for i in range(len(points) - 2):
            step_number = step_number + 1
            a = points[i]
            b = points[i + 1]
            self.intervals.append(
                self.createPosInterval(step_number, a, b, self.stepDuration)
            )
            self.startPoints.append(a)
            self.endPoints.append(b)

        # Intervals above get us to the final point.
        # If we are a closed loop, this is all we need.
        if self.closedLoop:
            step_number = step_number + 1
            self.intervals.append(
                self.createPosInterval(
                    step_number,
                    points[len(points) - 2],
                    points[0],
                    self.stepDuration,
                )
            )
            self.startPoints.append(points[len(points) - 2])
            self.endPoints.append(points[0])
        else:
            for i in reversed(range(len(points) - 1)):
                if i == 0:
                    break
                step_number = step_number + 1
                a = points[i]
                b = points[i - 1]
                self.intervals.append(
                    self.createPosInterval(step_number, a, b, self.stepDuration)
                )
                self.startPoints.append(a)
                self.endPoints.append(b)

        # RotateAtEachPoint style needs rotation intervals in between each position interval.
        if self.rotType == TravelerRotationStyle.StopAndRotateAtEachPoint:
            self.intervals = self.createHprIntervalsBetweenPosIntervals(
                self.intervals, step_number
            )

        # Finally populate the sequence with all the intervals.
        for i in self.intervals:
            self.seq.append(i)

    def startSequence(self):
        self.seq.loop()

    def stopSequence(self):
        self.seq.pause()

    def intervalIsDone(self, stepIndex: int):
        self.currentStepIndex = self.getNextStepIndex(stepIndex)
        # print("Step " + str(stepIndex) + " finished!")
        self.intervalDoneCB(stepIndex)

    def getNextStepIndex(self, stepIndex: int):
        if stepIndex >= (len(self.startPoints) - 1):
            return 0
        return stepIndex + 1

    def getPrevStepIndex(self, stepIndex: int):
        if stepIndex == 0:
            return len(self.startPoints) - 1
        return stepIndex - 1

    def createPosInterval(self, stepIndex: int, a: Vec3, b: Vec3, duration: float):
        self.accept(
            self.uName + "_Step_" + str(stepIndex), self.intervalIsDone, [stepIndex]
        )
        interval = LerpPosInterval(
            self.traveler, duration, b, a, None, "noBlend", 1, 1, self.uName
        )
        interval.setDoneEvent(self.uName + "_Step_" + str(stepIndex))
        return interval

    def createHprInterval(
        self,
        stepIndex: int,
        a_0: Vec3,
        a: Vec3,
        b: Vec3,
        duration: float,
    ):
        self.accept(
            self.uName + "_Step_" + str(stepIndex), self.intervalIsDone, [stepIndex]
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
            self.uName,
        )
        interval.setDoneEvent(self.uName + "_Step_" + str(stepIndex))
        return interval

    def createHprIntervalsBetweenPosIntervals(
        self, pos_intervals: list[Interval], step_number: int
    ):
        rot_index = 0
        final_interval_count = len(pos_intervals) * 2
        intervals = []
        while len(intervals) < final_interval_count:
            step_number = step_number + 1
            # print("HPR Interval at index "+ str(rot_index)+ ", prevStep "+ str(self.getPrevStepIndex(rot_index)))
            intervals.append(pos_intervals[rot_index])
            intervals.append(
                self.createHprInterval(
                    step_number,
                    self.startPoints[self.getPrevStepIndex(rot_index)],
                    self.startPoints[rot_index],
                    self.endPoints[rot_index],
                    self.stepDuration,
                )
            )
            rot_index = rot_index + 1
        return intervals


class PointPositionTravelTask(DirectObject):
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
        self.uName = unique_name
        self.points = points_of_travel
        self.numOfCycles = number_of_cycles
        self.cyclesElapsed = 0
        self.traveler = travelling_node
        self.tripDuration = duration_of_trip
        self.cyclesThroughTypes = rotation_type == TravelerRotationStyle.Cycle
        self.rotType = (
            TravelerRotationStyle.AlwaysLookAtCurrentPoint
            if self.cyclesThroughTypes
            else rotation_type
        )
        # Some rotation types are more task-based than others.
        if self.rotType == TravelerRotationStyle.AlwaysLookAtNextPoint:
            self.base.taskMgr.add(
                self.alwaysLookAtNextPointTask, unique_name + "_AlwaysLookAtNextPoint"
            )

        self.accept(unique_name + "_SequenceDone", self.sequenceIsDone)

        self.createFreshSequence()

        if start_immediately:
            self.tps.startSequence()
            print(
                "PointPositionTravelTask will cycle "
                + (
                    (str(self.numOfCycles) + " times!")
                    if self.numOfCycles > 0
                    else "forever!"
                )
            )

    def intervalIsDone(self, step_index_finished: int):
        if self.rotType == TravelerRotationStyle.AlwaysLookAtCurrentPoint:
            self.traveler.lookAt(self.tps.endPoints[step_index_finished], Vec3.up())

    def createFreshSequence(self):
        self.tps = TravelPointSequence(
            self.uName,
            self.points,
            self.tripDuration,
            self.accept,
            self.traveler,
            self.rotType,
            self.intervalIsDone,
        )
        self.tps.seq.setDoneEvent(self.uName + "_SequenceDone")

    def cycleToNextSequence(self):
        # This only gets called when the traveler is cycling types
        self.tps.stopSequence()
        if self.rotType == TravelerRotationStyle.AlwaysLookAtCurrentPoint:
            self.rotType = TravelerRotationStyle.AlwaysLookAtNextPoint
            self.base.taskMgr.add(
                self.alwaysLookAtNextPointTask, self.uName + "_AlwaysLookAtNextPoint"
            )
        elif self.rotType == TravelerRotationStyle.AlwaysLookAtNextPoint:
            self.base.taskMgr.remove(self.uName + "_AlwaysLookAtNextPoint")
            self.rotType = TravelerRotationStyle.StopAndRotateAtEachPoint
        else:
            # Only when returning back to the first type is this a whole "cycle"
            if self.numOfCycles > 0:
                self.cyclesElapsed = self.cyclesElapsed + 1
                print("Sequence finished cycle " + str(self.cyclesElapsed) + "!")
            self.rotType = TravelerRotationStyle.AlwaysLookAtCurrentPoint
        # Recreate sequence with new type.
        self.createFreshSequence()
        self.tps.startSequence()
        print("Traveler switched to rotation type " + str(self.rotType) + "!")

    def checkForSequenceFinishedCycles(self):
        if self.numOfCycles > 0:
            if self.cyclesElapsed >= self.numOfCycles:
                self.tps.stopSequence()
                print("Traveler has finished all cycles!")
            elif not self.cyclesThroughTypes:
                print("Sequence finished cycle " + str(self.cyclesElapsed) + "!")

    def sequenceIsDone(self):
        if self.cyclesThroughTypes:
            self.cycleToNextSequence()
        else:  # If we are staying on the same type, than a single lap counts as a "cycle"
            self.cyclesElapsed = self.cyclesElapsed + 1
        self.checkForSequenceFinishedCycles()

    # Define a procedure to move the camera.
    def alwaysLookAtNextPointTask(self, task: Task):
        self.traveler.lookAt(
            self.tps.endPoints[self.tps.getNextStepIndex(self.tps.currentStepIndex)],
            Vec3.up(),
        )
        return task.cont
