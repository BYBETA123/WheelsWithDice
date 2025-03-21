import pygame
import datetime
from dice import Dice
import os


class multiline:
    def __init__(self, text = "Default text", font = None, color = (255, 255, 255), width = 600):
        self.text = text
        self.font = font
        self.color = color
        self.width = width
        self.lines = [""]
        self.rendered = [""]
        self.breakdown()
        self.render()
    
    def update(self, text):
        self.text = text
        self.lines = [""]
        self.rendered = [""]
        self.breakdown()
        self.render()
        return self

    def breakdown(self):
        for character in self.text:
            if self.font.size(self.lines[-1] + character)[0] > self.width:
                self.lines.append(character)
            else:
                self.lines[-1] += character

    def render(self):
        # render the text
        self.rendered = [self.font.render(line, True, self.color) for line in self.lines]
        return self.rendered

    def getText(self):
        return self.lines
    
    def getRendered(self):
        return self.rendered
    
    def getHeight(self):
        return sum([line.get_height() for line in self.rendered])

def readFile(filePath):
    with open(filePath, "r") as f:
        text_lines = f.readlines()

    t_w, t_i = [], []
    for l in text_lines:
        try: 
            line = l.strip()
            a = line.index(" ")
            t_w.append(int(line[:a]))
            t_i.append(line[a+1:])
        except:
            print(f"Error in parsing the line, check the file for any errors\n The line is: {l} with path: {filePath}\n, The appropriate format: <weight> <text>")
    return t_w, t_i

# actual start of program

wheelpth = "wheels/"

# Get the file path from the user
while True:
    folderpath = input("Enter the folder path (Default = Monopoly): ")
    if folderpath in os.listdir(wheelpth):
        break
    if folderpath == "":
        folderpath = "Monopoly"
        break
    print(f"Folder \"{folderpath}\" not found, please try again")
folderpath += "/"

# find any file within the folder
files = os.listdir(wheelpth + folderpath)
global filePath
filePath = wheelpth + folderpath + files[0]

# read the file
print(f"Reading from file: \"{filePath}\"")

text_weights, text_items = readFile(filePath)
print(text_weights, text_items)

# Initialize Pygame
pygame.init()
# Set screen dimensions and title
screen = pygame.display.set_mode((600, 600))
bg = pygame.image.load("assets/bg.png")
pygame.display.set_caption('Scrollable Loot Box Animation - Text')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# These sizes probably need to be adjusted
mainFont = pygame.font.SysFont("Arial", 72)
secondaryFont = pygame.font.SysFont("Arial", 36)
smallFont = pygame.font.SysFont("Arial", 24)
# Function to render text as a surface
winner_text = secondaryFont.render("Winner", True, WHITE)
# Create a scrolling effect (simulated loot box items rolling through)
frames = 20
fps = 1 / frames  # Frames per second
globalHide = False

lineMapper = multiline("This is a test of the multiline class", secondaryFont, (255, 255, 255), 550)

def animate_loot_box(spinTime = 10):

    oS = spinTime    
    if spinTime %5 != 0: # fixing input
        spinTime = round((spinTime)/5)*5 # nearest 5
    spinTime = max(5, spinTime) # minimum 5 seconds
    if os != spinTime:
        print(f"Time set to {spinTime} seconds")


    def render_text(text, font, multiline = False):
        if multiline:
            return lineMapper.update(text).getRendered()
        oldText = text
        newText = oldText
        # sanity check that it is less than 300 pixels wide
        if font.size(oldText)[0] < 300:
            return font.render(oldText, True, WHITE) # exit early
        tempText = "..." + newText + "..."
        while (font.size(tempText)[0] > 300):
            newText = newText[1:-1]
            tempText = "..." + newText + "..."
        newText = "..." + newText + "..." 
        return font.render(newText, True, WHITE)

    def getText(rendered_texts, index):
        i = (index+len(rendered_texts)) % len(rendered_texts)
        return rendered_texts[i]

    def winner():
        # This should bring up a box which shows the correct answer in full
        # create the box
        t = getText(rendered_texts, index)
        screen.blit(t, (base_x - t.get_width()//2, base_y - t.get_height()//2))

        pygame.draw.rect(screen, GREEN, (base_x - t.get_width()//2, base_y - t.get_height()//2, t.get_width(), t.get_height()), 1)

        # create the box around the text
        # create a new surface for the text
        # draw a box around the text
        # display both
        lineMapper.update(text_items[index])
        temp = lineMapper

        pygame.draw.rect(screen, BLUE, (20, 450, 550, temp.getHeight()), border_top_left_radius= 6, border_top_right_radius= 6) # outer box
        pygame.draw.rect(screen, GREEN, (20, 450 + winner_text.get_height(), 550, temp.getHeight()), border_bottom_left_radius= 6, border_bottom_right_radius= 6)
        screen.blit(winner_text, (25, 450))
        h = winner_text.get_height() + 450
        for l in temp.getRendered():
            screen.blit(l, (25, h))
            h+=l.get_height()

    def scrollFunc(percentage):
        return ((0.013*percentage**(1.5) + 1))

    def drawOptions():
        x = 10
        y = 10
        screen.blit(smallFont.render(files[currentFile], True, WHITE), (x, y))

    def findInList(item, lst):
        print(item, lst)
        for i in range(len(lst)):
            if item in lst[i]:
                return i
        return -1
    
    running = True
    index = 0  # Index of the current
    spinning = datetime.datetime.now() # start the timer
    lTime = spinning
    # Render the text items as surfaces
    selected = False
    base_x = 300
    base_y = 300
    #other variables
    scrollSpeed = 10 # Speed of the scrolling effect
    lFrame = 0 # Frame counter
    currentFile = 0 # file counter
    d = Dice()
    global filePath
    text_weights, text_items = readFile(filePath)
    d.setSidesWithWeights(text_items, text_weights)
    # d.setSidesWithWeights(["One is the loneliest number the world has ever seen", "Two is a pear like the fruit but not red like an apple"], [1, 1])
    text_items = d.getItems(hide = globalHide)
    r = d.roll(time=-1, returnType="side")
    print(text_items)
    searchIndex = findInList(r, text_items)
    rendered_texts = [render_text(text, mainFont) for text in text_items]
    secondary_texts = [render_text(text, secondaryFont) for text in text_items]
    small_texts = [render_text(text, smallFont, multiline=True) for text in text_items]
    rigged = -1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # we want the ability to rig the wheel (Don't tell anyone)
                if event.key == pygame.K_1 or event.key == pygame.K_KP1: # key 1
                    rigged = 0
                    print(f"RIGGED: {text_items[rigged%len(text_items)]}")
                if event.key == pygame.K_2 or event.key == pygame.K_KP2: # key 2
                    rigged += 1
                    print(f"RIGGED: {text_items[rigged%len(text_items)]}")
                if event.key == pygame.K_3 or event.key == pygame.K_KP3: # key 3
                    rigged += 2
                    print(f"RIGGED: {text_items[rigged%len(text_items)]}")
                if event.key == pygame.K_4 or event.key == pygame.K_KP4: # key 4
                    rigged += 3
                    print(f"RIGGED: {text_items[rigged%len(text_items)]}")
                if event.key == pygame.K_5 or event.key == pygame.K_KP5: # key 5
                    rigged += 4
                    print(f"RIGGED: {text_items[rigged%len(text_items)]}")
                if event.key == pygame.K_6 or event.key == pygame.K_KP6: # key 6
                    rigged += 5
                    print(f"RIGGED: {text_items[rigged%len(text_items)]}")
                if event.key == pygame.K_7 or event.key == pygame.K_KP7: # key 7
                    rigged += 6
                    print(f"RIGGED: {text_items[rigged%len(text_items)]}")
                if event.key == pygame.K_8 or event.key == pygame.K_KP8: # key 8
                    rigged += 7
                    print(f"RIGGED: {text_items[rigged%len(text_items)]}")
                if event.key == pygame.K_9 or event.key == pygame.K_KP9: # key 9
                    rigged += 8
                    print(f"RIGGED: {text_items[rigged%len(text_items)]}")
                if event.key == pygame.K_0 or event.key == pygame.K_KP0: # key 0
                    rigged += 9
                    print(f"RIGGED: {text_items[rigged%len(text_items)]}")


                if event.key == pygame.K_SPACE:
                    if selected:

                        percentage = 0
                        spinning = datetime.datetime.now() # Resetting the timer
                        lTime = spinning
                        lFrame = 0
                        r = d.roll(time=-1, returnType="side")
                        print(d.getDetails())
                        searchIndex = findInList(r, text_items)
                        if rigged != -1:
                            searchIndex = rigged
                        selected = False
                        print("Restarted")
                if event.key == pygame.K_i:
                    print(pygame.mouse.get_pos())
                if selected and (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):
                    if event.key == pygame.K_LEFT:
                        currentFile = (currentFile - 1) % len(files)
                        print("Moving left")
                    if event.key == pygame.K_RIGHT:
                        currentFile = (currentFile + 1) % len(files)
                        print("Moving right")
                    
                    print(f"Reading from file: \"{files[currentFile]}\"")
                    filePath = wheelpth + folderpath + files[currentFile]
                    text_weights, text_items = readFile(filePath)
                    d.setSidesWithWeights(text_items, text_weights)
                    # d.setSidesWithWeights(["One is the loneliest number the world has ever seen", "Two is a pear like the fruit but not red like an apple"], [1, 1])
                    text_items = d.getItems(hide = globalHide)
                    r = d.roll(time=-1, returnType="side")
                    print(text_items)
                    index = 0 # reset the index
                    searchIndex = findInList(r, text_items)
                    rendered_texts = [render_text(text, mainFont) for text in text_items]
                    secondary_texts = [render_text(text, secondaryFont) for text in text_items]
                    small_texts = [render_text(text, smallFont, multiline=True) for text in text_items]
                    # because of this, we need to reset the text
                    screen.fill(BLACK)
                    # new drawing code
                    screen.blit(bg, (0,0))
                    pygame.draw.circle(screen, BLACK, (300, 300), 200)
                    pygame.draw.circle(screen, WHITE, (300, 300), 200, 10)

                    # Only show 3 items
                    screen.blit(getText(secondary_texts, index - 1), (base_x - getText(secondary_texts, index - 1).get_width()//2, base_y - getText(secondary_texts, index - 1).get_height()*2.5))
                    screen.blit(getText(rendered_texts, index), (base_x - getText(rendered_texts, index).get_width()//2, base_y - getText(rendered_texts, index).get_height()//2))
                    screen.blit(getText(secondary_texts, index + 1), (base_x - getText(secondary_texts, index + 1).get_width()//2, base_y + getText(secondary_texts, index + 1).get_height()*1.5 ))

        if datetime.datetime.now() - lTime > datetime.timedelta(seconds=fps):
            lTime = datetime.datetime.now() # Resetting the timer
            #frame update
            percentage = (lTime-spinning) / datetime.timedelta(seconds=spinTime) * 100
            scrollSpeed = int(min(scrollFunc(percentage), 40)) # 25 is the minimum speed

            if lFrame > scrollSpeed and not selected:
                lFrame = 0

                selected = (percentage >= 100) and (index == searchIndex)

                if not selected:
                    index = (index + 1) % len(text_items)  # Wrap around to the beginning if we reach the end
                else:
                    print("Switched")

                screen.blit(bg, (0,0))
                pygame.draw.circle(screen, BLACK, (300, 300), 200)
                pygame.draw.circle(screen, WHITE, (300, 300), 200, 10)

                # Only show 3 items
                screen.blit(getText(secondary_texts, index - 1), (base_x - getText(secondary_texts, index - 1).get_width()//2, base_y - getText(secondary_texts, index - 1).get_height()*2.5))
                screen.blit(getText(rendered_texts, index), (base_x - getText(rendered_texts, index).get_width()//2, base_y - getText(rendered_texts, index).get_height()//2))
                screen.blit(getText(secondary_texts, index + 1), (base_x - getText(secondary_texts, index + 1).get_width()//2, base_y + getText(secondary_texts, index + 1).get_height()*1.5 ))

                drawOptions()

            if selected: # in case it didn't actually reach 100%

                winner()
                drawOptions()
    
                pass

            pygame.display.flip()  # Update the screen
            lFrame += 1

    pygame.quit()

# Start the animation
animate_loot_box(5)
