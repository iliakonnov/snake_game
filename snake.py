# coding:utf8
import random
from TorWorld import *


class Snake:
    def __init__(self, W, idHead, idBody, idBrick, idFood, world_h, world_w):
        self.bricksmany = 0
        self.foodmany = 0
        self.bricksmany_old = 0
        self.foodmany_old = 0
        self.FaBFirstTime = True
        self.score = 0

        self.world = W
        self.idHead = idHead
        self.idBody = idBody
        self.idBrick = idBrick
        self.idFood = idFood
        self.world_h = world_h
        self.world_w = world_w

    def Init(self, positions, tar):
        self.dir = tar
        self.positions = positions

        head = self.positions[0]
        self.world.PutCell(head[0], head[1], self.idHead)
        for tail in self.positions[1:]:
            self.world.PutCell(tail[0], tail[1], self.idBody)

    def FoodAndBricks(self, FoodMany, BricksMany):
        self.w_world_max = self.world_w - 2
        self.h_world_max = self.world_h - 2
        self.w_world_min = 1
        self.h_world_min = 1
        while self.bricksmany < BricksMany:
            brick_x = random.randint(self.w_world_min, self.w_world_max)
            brick_y = random.randint(self.h_world_min, self.h_world_max)
            brick_e = self.world.IsEmpty(brick_x, brick_y)
            if brick_e:
                self.world.PutCell(brick_x, brick_y, self.idBrick)
                self.bricksmany = self.bricksmany + 1

        while self.foodmany < FoodMany:
            food_x = random.randint(self.w_world_min, self.w_world_max)
            food_y = random.randint(self.h_world_min, self.h_world_max)
            food_e = self.world.IsEmpty(food_x, food_y)
            if food_e:
                self.world.PutCell(food_x, food_y, self.idFood)
                self.foodmany = self.foodmany + 1

        if self.FaBFirstTime:
            self.bricksmany_old, self.foodmany_old = self.bricksmany, self.foodmany
            self.FaBFirstTime = False

    def Move(self):
        head = self.positions[0]
        newHead = [head[0] + self.dir[0], head[1] + self.dir[1]]
        eated = False

        if not self.world.IsEmpty(newHead[0], newHead[1]):
            place = self.world.GetCell(newHead[0], newHead[1])
            if place in [self.idHead, self.idBody, self.idBrick]:
                return False
            elif place in [self.idFood]:
                eated = True

        self.world.PutCell(head[0], head[1], self.idBody)
        self.positions.insert(0, newHead)
        self.world.PutCell(newHead[0], newHead[1], self.idHead)
        if not eated:
            self._RemoveTail()
        else:
            self.foodmany = self.foodmany - 1
            if self.foodmany == 0:
                self.bricksmany = 0
                self.FoodAndBricks(self.foodmany_old, self.bricksmany_old)
            self.score += 1
        return True

    def TurnUp(self):
        self.dir = (0, -1)

    def TurnDown(self):
        self.dir = (0, 1)

    def TurnLeft(self):
        self.dir = (-1, 0)

    def TurnRight(self):
        self.dir = (1, 0)

    def _RemoveTail(self):
        tail = self.positions.pop()
        self.world.Clear(tail[0], tail[1])

if __name__ == "__main__":
    W = TorWorld(7, 9)
    idHead = 2
    idBody = 1
    idBrick = 3
    idFood = 4
    S = Snake(W, idHead, idBody, idBrick, idFood, 7, 9)

    startSnake = [[1, 3], [1, 2], [1, 1]]
    S.Init(startSnake, (0, 1))

    assert W.GetCell(1, 3) == idHead, "ERROR HEAD"
    assert W.GetCell(1, 1) == idBody, "ERROR TAIL"

    assert S.Move(), "ERROR NO BRICK"
    assert S.world.GetCell(1, 4) == idHead, "ERROR HEAD"
    assert S.world.GetCell(1, 3) == idBody, "ERROR BODY"
    assert S.world.IsEmpty(1, 1), "ERROR TAIL"

    W.PutCell(4, 5, idBrick)
    startSnake = [[4, 4]]
    S.Init(startSnake, (0, 1))
    assert not S.Move(), "ERROR BRICK"

    W.Clear(4, 5)
    S.Init(startSnake, (0, 1))
    for i in range(1000):
        assert S.Move(), "ERROR 5"
    print("SUCCESS!")
