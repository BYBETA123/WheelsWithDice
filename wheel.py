import pygame
import datetime
from dice import Dice


# Initialize Pygame
pygame.init()

# Set screen dimensions and title
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Scrollable Loot Box Animation - Text')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
# List of text items (these could be loot box rewards or items)

# Load font (you can change this to any font you like)
font = pygame.font.SysFont("Arial", 36)

# Function to render text as a surface


# Create a scrolling effect (simulated loot box items rolling through)
frames = 20
fps = 1 / frames  # Frames per second

def animate_loot_box(spinTime = 10):

    def render_text(text):
        return font.render(text, True, WHITE)

    def getText(rendered_texts, index):
        i = (index+len(rendered_texts)) % len(rendered_texts)
        return rendered_texts[i]

    def winner():
        c = GREEN
        screen.fill(c)  # Clear the screen
        screen.blit(getText(rendered_texts, index), (base_x - getText(rendered_texts, index).get_width()//2, base_y - getText(rendered_texts, index).get_height()//2))

    def scrollFunc(percentage):
        return ((0.013*percentage**(1.5) + 1))

    def drawOptions():
        x = 10
        y = 10
        for i in range(len(text_items)):
            screen.blit(rendered_texts[i], (x, y))
            y += rendered_texts[i].get_height()

    running = True
    index = 0  # Index of the current
    spinning = datetime.datetime.now() # start the timer
    lTime = spinning
    # Render the text items as surfaces
    selected = False
    base_x = 400
    base_y = 300
    c = BLACK
    #other variables
    scrollSpeed = 10 # Speed of the scrolling effect
    lFrame = 0 # Frame counter


    d = Dice()
    d.setSidesWithWeights(["One", "Two", "Three", "Four", "Five", "Six"], [1, 1, 1, 3, 1, 2])
    text_items = d.getItems()
    r = d.roll(time=-1, returnType="side")
    print(text_items)

    def findInList(item, lst):
        print(item, lst)
        for i in range(len(lst)):
            if item in lst[i]:
                return i
        return -1
        
    searchIndex = findInList(r, text_items)
    rendered_texts = [render_text(text) for text in text_items]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    if selected:
                        percentage = 0
                        spinning = datetime.datetime.now() # Resetting the timer
                        lTime = spinning
                        lFrame = 0
                        r = d.roll(time=-1, returnType="side")
                        searchIndex = findInList(r, text_items)
                        selected = False
                        print("Restarted")

        # we are drawwing at 1 fps
        if datetime.datetime.now() - lTime > datetime.timedelta(seconds=fps):
            lTime = datetime.datetime.now() # Resetting the timer
            #frame update
            percentage = (lTime-spinning) / datetime.timedelta(seconds=spinTime) * 100

            scrollSpeed = scrollFunc(percentage) # needs to return an integer


            if lFrame > scrollSpeed and not selected:
                lFrame = 0
                screen.fill(c)  # Clear the screen

                # Only show 3 items
                screen.blit(getText(rendered_texts, index - 1), (base_x - getText(rendered_texts, index - 1).get_width()//2, base_y - getText(rendered_texts, index - 1).get_height()*1.5))
                screen.blit(getText(rendered_texts, index), (base_x - getText(rendered_texts, index).get_width()//2, base_y - getText(rendered_texts, index).get_height()//2))
                screen.blit(getText(rendered_texts, index + 1), (base_x - getText(rendered_texts, index + 1).get_width()//2, base_y + getText(rendered_texts, index + 1).get_height()*0.5 ))

                selected = (percentage >= 100) and (index == searchIndex)
                if not selected:
                    index = (index + 1) % len(text_items)  # Wrap around to the beginning if we reach the end
                else:
                    print("Switched")

            if selected: # in case it didn't actually reach 100%

                winner()

            # draw the list of options
            drawOptions()

            # draw centering lines
            pygame.draw.line(screen, WHITE, (400, 0), (400, 600), 1)
            pygame.draw.line(screen, WHITE, (0, 300), (800, 300), 1)

            pygame.display.flip()  # Update the screen
            lFrame += 1

    pygame.quit()

# Start the animation
animate_loot_box()
