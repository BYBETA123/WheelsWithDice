import random
import matplotlib.pyplot as plt
from datetime import datetime

class Dice():
    def __init__(self, sides = None):
        if sides is None:
            sides = 1
        self.sides = [(i+1) for i in range(sides)]
        self.rollCount = [0 for _ in range(sides)]
        self.totalCount = sides
        self.lastRoll = None
        self.lastTime = [1 for _ in range(sides)]
        self.total = 0
        self.weighted = False

    def roll(self, time = 10, returnType = "number"):
        sTime = datetime.now()
        #calculate the upper limit of the random numebr
        total = 0
        for i in range(len(self.lastTime)):
            total += self.lastTime[i]

        num = random.randint(1, total)
        #find the side that corresponds to the number
        s = 0 # sum
        for i in range(len(self.lastTime)):
            if num <= self.lastTime[i] + s:
                num = i + 1
                
                break
            s += self.lastTime[i]

        #Once we have picked a number, we need to update the lastTime array
        for i in range(len(self.lastTime)):
            if i != num - 1:
                self.lastTime[i] += 1 #increment the last time for the current number
            else:
                self.lastTime[i] = 1 #reset the last time for the current number
        self.total += 1
        self.rollCount[num - 1] += 1

        # add a delay to simulate a real dice roll
        if time != -1:
            print("") # making sure it is a new line
        while((datetime.now() - sTime).seconds < time):
            # progress bar
            s = '|'
            for i in range(20):
                if i < ((datetime.now() - sTime).seconds / time) * 20:
                    s += '\u2588'
                else:
                    s += ' '
            s+= '|'
            s+= f" {((datetime.now() - sTime).seconds / time) * 100:.2f}%"
            print(s, end='\r')

        if time != -1:
            s = '|'
            for i in range(20):
                if i < ((datetime.now() - sTime).seconds / time) * 20:
                    s += '\u2588'
                else:
                    s += ' '
            s+= '|'
            s+= f" 100.00%"
            print(s, end='\n')

        if returnType == "number":
            return num
        elif returnType == "side":
            return self.sides[num - 1]
        else:
            raise ValueError("The return type must be either 'number' or 'side'")

    def getPercentages(self):
        percentages = []
        for i in range(len(self.sides)):
            percentages.append(f"{(self.rollCount[i] / self.total * 100):.2f}")
        return percentages
    
    def getDistribution(self):
        return self.rollCount
    
    def getLast(self):
        return self.lastTime

    def setCustomSides(self, sides):
        self.sides = sides
        self.rollCount = [0 for _ in range(len(sides))]
        self.totalCount = sides
        self.lastRoll = None
        self.lastTime = [1 for _ in range(len(sides))]
        self.total = 0

    def setSidesWithWeights(self, sides, weights):
        self.sides = []
        if len(sides) != len(weights):
            raise ValueError("The sides and weights must be the same length")
        for i in range(len(weights)):
            for _ in range(weights[i]):
                self.sides.append(sides[i]) # This is better
        self.rollCount = [0 for _ in range(len(self.sides))]
        self.totalCount = len(self.sides)
        self.lastRoll = None
        self.lastTime = [1 for _ in range(len(self.sides))]
        self.total = 0
        self.weighted = True
        
    def getItems(self):

        tempDictionary = {}
        dupes = []
        c = []
        for i in range(len(self.sides)):
            if tempDictionary.get(self.sides[i]) is not None:
                tempDictionary[self.sides[i]] += self.rollCount[i]
                c[dupes.index(self.sides[i])] += 1
            else:
                tempDictionary[self.sides[i]] = self.rollCount[i]
                dupes.append(self.sides[i])
                c.append(1)

        # The dictinoary should be updated such that the copies are updated
        for i in range(len(dupes)):
            tempDictionary[f'{dupes[i]}({c[i]})'] = tempDictionary.pop(dupes[i])

        return list(tempDictionary.keys())

    def showGraph(self):
        # Create the plot
        plt.figure()

        # Plot the first array
        print(self.sides)


        if self.weighted:

            # self.sides is the labels for each side
            print("===========")
            print(self.sides)
            print(self.rollCount)
            # make this a dictionary
            tempDictionary = {}
            dupes = []
            c = []
            for i in range(len(self.sides)):
                if tempDictionary.get(self.sides[i]) is not None:
                    tempDictionary[self.sides[i]] += self.rollCount[i]
                    c[dupes.index(self.sides[i])] += 1
                else:
                    tempDictionary[self.sides[i]] = self.rollCount[i]
                    dupes.append(self.sides[i])
                    c.append(1)

            # The dictinoary should be updated such that the copies are updated
            for i in range(len(dupes)):
                tempDictionary[f'{dupes[i]}({c[i]})'] = tempDictionary.pop(dupes[i])


            print(tempDictionary)

            x = list(tempDictionary.keys())
            y = list(tempDictionary.values())

            plt.plot(x, y, label='Balanced* Dice (Weighted)', color='blue', linestyle='-', marker='o')
            plt.ylim(0, max(y)*1.25)
            # Add titles and labels
            plt.title('Balanced* Graph Distribution', fontsize=14)
            plt.xlabel('Value', fontsize=12)
            plt.ylabel('Probability', fontsize=12)

        else:
            plt.plot(self.sides, self.rollCount, label='Balanced* Dice', color='blue', linestyle='-', marker='o')
            plt.ylim(0, max(self.rollCount)*1.25)
            # Add titles and labels
            plt.title('Balanced* Graph Distribution', fontsize=14)
            plt.xlabel('Value', fontsize=12)
            plt.ylabel('Probability', fontsize=12)

        # Add a legend to differentiate the lines
        plt.legend()

        # Show the plot
        plt.grid(True)
        plt.show()

    def getSides(self):
        return self.sides, len(self.sides)

def findAll(d = None, sides = 6):
    count = 0
    rolls = [0 for _ in range(sides)] # the amount of roles for each side
    
    def countUnique(lst):
        total = 0
        for i in range(len(lst)):
            if lst[i] != 0:
                total += 1
        return total == len(lst)

    while not countUnique(rolls):
        if d is None:
            r = random.randint(1, sides)
        else:
            r = d.roll(time=-1, returnType="number")
        rolls[r - 1] += 1
        count += 1

    return count


def main():

    sides = 6

    def Convergence(dice1, dice2 = None, sides = 6, n = 1000000, output = True):
        t1 = 0
        t2 = 0
        # try 10,000 rolls to find the average
        for i in range(n):
            t1 += findAll(dice1, sides)
            t2 += findAll(dice2, sides)
            if i % 1000 == 0 and output:
                print(f"The total {i} / {n}")

        print(f"Average rolls for all options balanced dice: {t1/n} || Average for all options random dice: {t2/n}")

    def Probability(dice1, dice2 = None, sides = 6, n = 100000, output = True):
        d1_rolls = [0 for _ in range(sides)]
        d2_rolls = [0 for _ in range(sides)]
        for i in range(n):
            r1 = dice1.roll(time=-1, returnType="number")
            if dice2 is not None:
                r2 = dice2.roll(time=-1, returnType="number")
            else:
                r2 = random.randint(1, sides)
            d1_rolls[r1 - 1] += 1
            d2_rolls[r2 - 1] += 1
            if i % (n/1000) == 0 and output:
                print(f"The total {i} / {n}")
        # now that this is done, we can calculate the probability
        for i in range(sides):
            d1_rolls[i] /= n
            d2_rolls[i] /= n
        
        print(f"Balanced Dice: {d1_rolls} || Random Dice: {d2_rolls}")

    def ExpectedValue(dice1, dice2 = None, sides = 6, n = 100000, output = True):
        # calculate the expected value after n runs
        e1 = 0
        e2 = 0
        for i in range(n):
            e1 += dice1.roll(time=-1, returnType="number")
            if dice2 is not None:
                e2 += dice2.roll(time=-1, returnType="number")
            else:
                e2 += random.randint(1, sides)
            if i % (n/1000) == 0 and output:
                print(f"The total {i} / {n}")

        print(f"Balanced Dice: {e1/n} || Random Dice: {e2/n}")

    sides = 50
    d = Dice(sides=sides)

    Convergence(d, None, sides, 10000, output = True)
    exit()
    Probability(d, None, sides, 1000000, output = False)
    ExpectedValue(d, None, sides, 1000000, output = False)

if __name__ == "__main__":
    main()