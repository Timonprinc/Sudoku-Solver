
import pygame, sys
from pygame.locals import *
FPS = 10 #updejta 10x na sekundo

WINDOWMULTIPLIER = 10 #spremen to cifro če hočeš spremeniti velikost polja
WINDOWSIZE = 90
WINDOWWIDTH =  WINDOWSIZE * WINDOWMULTIPLIER
WINDOWHEIGHT =  WINDOWSIZE * WINDOWMULTIPLIER

SQUARESIZE = int((WINDOWSIZE * WINDOWMULTIPLIER) / 3) # veliki kvadrati
CELLSIZE =int(SQUARESIZE / 3)  #pravokotniki (3 na kvadrat- levo-desno)
NUMBERSIZE =int(CELLSIZE / 3) # Size of a cell
WINDOWSIZE = 81 #večkratnik 3,9,27

BLACK     = (0  ,0  ,0  )
WHITE     = (255,255,255)
LIGHTGRAY = (200,200,200)
BLUE      = (0  ,0  ,255) #barva
GREEN     = (0  ,255,0  )

def drawGrid():
    ### Draw Minor Lines
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, LIGHTGRAY, (x,0),(x,WINDOWHEIGHT)) #to barvo uporabi v koordinati (x,0), vse do...
    for y in range (0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, LIGHTGRAY, (0,y), (WINDOWWIDTH, y))
    
    ### Draw Major Lines
    for x in range(0, WINDOWWIDTH, SQUARESIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, BLACK, (x,0),(x,WINDOWHEIGHT))
    for y in range (0, WINDOWHEIGHT, SQUARESIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, BLACK, (0,y), (WINDOWWIDTH, y))

    return None #?

def initiateCells(): #vsaka celica ima cifre od 1-9, najlažje s slovarjem
    currentGrid = {}
    fullCell = [1,2,3,4,5,6,7,8,9]
    for xCoord in range(0,9):
        for yCoord in range(0,9): #81 koordinat-->vsak ključ,ki jih je 81, dobi vrednosti od 1-9
            currentGrid[xCoord,yCoord] = list(fullCell) # Copies List, list
                        #ključ  #vrednost
    return currentGrid    

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    
    FPSCLOCK = pygame.time.Clock() #posodobitev sudokuja

    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    #DISPLAYSURF = pygame.display.set_mode((400,300))







    pygame.display.set_caption('Sudoku Pomagač')

    global BASICFONT, BASICFONTSIZE, LARGEFONT, LARGEFONTSIZE #pisava, oznaka, ''global''-->bo uporabno tudi izven funkcije
    BASICFONTSIZE=15
    LARGEFONTSIZE=55
    BASICFONT=pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    LARGEFONT = pygame.font.Font('freesansbold.ttf', LARGEFONTSIZE)
    currentGrid = initiateCells() #nam vrže ven ta doug slovar, sets all cells to have numbers 1-9


    DISPLAYSURF.fill(WHITE)
    
    
    
    

    
    def displayCells(currentGrid):
        
        
                    # Create offset factors to display numbers in right location in cells #-koordinati.
        xFactor = 0 #da se ne bodo cifre spawnale druga na drugi
        yFactor = 0
        for item in currentGrid: # Iterata čez ključe(0,0) item is x,y co-ordinate from 0 - 8
            cellData = currentGrid[item] # isolates the numbers still available for that cell
            for number in cellData: #iterata čez vsako cifro posebi(0)iterates through each number
                if number != ' ': # ignores those already dismissed, da ne bo težil pri reševanju
                    xFactor = ((number-1)%3) #v 3 vrstice smo prej tist razdelil, to so koordinati x 0,1,2 1/4/7 = 0 2/5/8 = 1 3/6/9 =2
                    if number <= 3:
                        
                        #določanje še y koordinat
                        yFactor = 0 
                    elif number <=6:
                        yFactor = 1
                    else:
                        yFactor = 2
                #(item[0] * CELLSIZE) Positions in the right Cell
                #(xFactor*NUMBERSIZE) Offsets (kompenzacije) to position number    
                if cellData.count(' ') < 8:   # zna bit sumljivo 
                    populateCells(number,(item[0]*CELLSIZE)+(xFactor*NUMBERSIZE),(item[1]*CELLSIZE)+(yFactor*NUMBERSIZE),'small')
                else:
                    populateCells(number,(item[0]*CELLSIZE),(item[1]*CELLSIZE),'large')
                #tole nam da x,y vsake cifre, also pošlje spodnji funkciji info
        
    def populateCells(cellData, x, y,size):
        
        if size == 'small':
            
            cellSurf = BASICFONT.render('%s' %(cellData), True, LIGHTGRAY)
        elif size == 'large':
            
            
           cellSurf = LARGEFONT.render('%s' %(cellData), True, GREEN)
        
            
         
        
        cellRect = cellSurf.get_rect()
        cellRect.topleft = (x, y)
        DISPLAYSURF.blit(cellSurf, cellRect)#funkcije ''obarva'' vrednosti pridobljene
        #iz zgornje funkcije
    def displaySelectedNumber(mousex, mousey, currentGrid): #dela
        
        
        
        xNumber =int( (mousex*27) / WINDOWWIDTH) # xNumber in range 0 - 26
        yNumber =int((mousey*27) / WINDOWWIDTH) # yNumber in range 0 - 26
        #Determine a 0,1 or 2 for x and y
        modXNumber =int( xNumber % 3)
        modYNumber = int(yNumber % 3)
        if modXNumber == 0:
            
            
            xChoices = [1,4,7]
            number = xChoices[modYNumber]        
        elif modXNumber == 1:
            
            
            xChoices = [2,5,8]
            number = xChoices[modYNumber]
        else:
            xChoices = [3,6,9]
            number = xChoices[modYNumber]
        # need to determine the cell we are in
        xCellNumber = int(xNumber / 3)
        yCellNumber = int(yNumber / 3)
        
        # gets a list of current numbers
        currentState = currentGrid[xCellNumber,yCellNumber]
        incNum = 0
    
        while incNum < 9:
            
            
            # if NOT number selected
            if incNum+1 != number:
                
                
                currentState[incNum] = ' ' # make ' '
            else:
                
                
                currentState[incNum] = number # make = number
            #update currentGrid
            currentGrid[xCellNumber,yCellNumber] = currentState
            incNum += 1
        incNum += 1
        #currentGrid = refreshGrid(currentGrid)    
        return currentGrid  
        # If a number is selected, and then changed the grid needs to be refreshed. 

    







    
    
    
    
    
        
    def drawBox(mousex,mousey):
        
        boxx =((mousex*27) / WINDOWWIDTH) * (NUMBERSIZE ) # 27 number of squares
        boxy =((mousey*27) / WINDOWHEIGHT) * (NUMBERSIZE ) # 27 number of squares
        pygame.draw.rect(DISPLAYSURF, BLUE, (boxx,boxy,NUMBERSIZE,NUMBERSIZE), 1) #nariše pravokotnik
        #displaysurf-kje rišemo,barva, x,y, numbersize=velikost škatle, 1=širina črte


        
    displayCells(currentGrid) #
    drawGrid()#pokliče funkcijo, ki riše črte vertikalne pa horizontalne črke po poljih.
    def removeX(currentGrid, item, number):
        #item-kvadratek ki ga gledamo, GLEDA VRSTICE
        
        
        for x in range(0,9):  #x os-9 možnosti
            
            if x != item[0]:
                
                currentState = currentGrid[(x,item[1])] #naredi list za vsak kvadratek in njegove cifre
                currentState[number-1] = ' ' #zbrišemo ponavljajočo cifro
                currentGrid[(x,item[1])] = currentState 
                #ker opazujemo samo x-e bo y konstanten
                #updejtamo slovar
        return currentGrid


    def removeY(currentGrid, item, number):
        #GLEDA STOLPCE, x konstanta
        

        for y in range(0,9):
            
           if y != item[1]:
               
               
               currentState = currentGrid[(item[0],y)] #x konstanten
               currentState[number-1] = ' '
               currentGrid[(item[0],y)] = currentState
        return currentGrid
    def removeGrid(currentGrid, item, number):
        

        if item[0] < 3:
            
            xGrid = [0,1,2] #prvi trije veliki kvadrati (navpično)
        elif item[0] > 5:
            xGrid = [6,7,8]
        else:
            xGrid = [3,4,5]

        if item[1] < 3:
            
            
            yGrid = [0,1,2] #prvi trije veliki kvadrati horizontalno
        elif item[1] > 5:
            
            yGrid = [6,7,8]
        else:
            
            yGrid = [3,4,5]
        for x in xGrid: #gremo čez vsak kvadratek posebi
            
            
            for y in yGrid:
                if (x,y) != item:
                    
                    currentState = currentGrid[(x,y)] # isolates the numbers still available for that cell
                    currentState[number-1] = ' ' # make them blank.
                    currentGrid[(x,y)] = currentState# updejt for all squares except the one containing the number  
        return currentGrid        
    
    #iterates through each of the nine numbers in the grid
    



    def solveSudoku(currentGrid):
            
            for item in currentGrid: #gre čez ključe v diktionariju
                
                
                # item is x,y co-ordinate from 0-8
                cellData = currentGrid[item] # isolates the numbers still available for that cell
                if cellData.count(' ') == 8: #odebeljene cifre( ki vplivajo)
                    # only look at those with one number remaining
                    for number in cellData:
                        # Determine the number there

                        if number != ' ':
                                          #imamo same lufte pa eno cifro
                            
                            updateNumber = number # zabeležimo si to cifro
                    currentGrid = removeX(currentGrid, item, updateNumber) #1. pomagač
                    currentGrid = removeY(currentGrid, item, updateNumber)
                    currentGrid = removeGrid(currentGrid, item, updateNumber)
                    
            # determine if any cells contain a number only used once in X/Y/Grid
            currentGrid = onlyNinX(currentGrid) #2. pomagač
            currentGrid = onlyNinY(currentGrid)
            currentGrid = onlyNinGrid(currentGrid)
            
    def onlyNinX(currentGrid):
        
        
        
         
        # check all items in currentGrid list
        for item in currentGrid:
            
            
            # create two empty lists
            allNumbers = [] #lista za cifre v vrsticah in kvadratkih
            currentNumbers = []


        
            # determine all numbers remaining in the row - store in allNumbers
            for xRange in range(0,9):
                
                
                for rowNumbers in currentGrid[(xRange,item[1])]: #gledamo x os
                    
                    if rowNumbers != ' ': #shranimo cifre v vrstici, ignoriramo luft
                        
                        allNumbers.append(rowNumbers)
                    
                # determine numbers remaining in individual cell being looked at - store in currentNumbers
            for cellNumbers in currentGrid[item]: #pogledamo še cifre v kvadratkih
                    
                    
                if cellNumbers != ' ':
                    
                    
                        
                    currentNumbers.append(cellNumbers)
              
                 # look at numbers remaining in a cell. Check if they only appear in the row once.        
                if len(currentNumbers) > 1:
                    
                        
                        
                             #nevem če je v tej vrstici
                    for checkNumber in currentNumbers:
                        
                            
                            
                        if allNumbers.count(checkNumber) == 1:
                                
                                
                                     # at this stage we know checkNumber appears only once, so we now update grid
                            currentState = currentGrid[item] 
                            for individualNumber in currentState:
                                    
                                    
                                if individualNumber != checkNumber and individualNumber != ' ':
                                        
                                    currentState[individualNumber-1] = ' ' 
                                    currentGrid[item] = currentState         
        return currentGrid     
    def onlyNinY(currentGrid):
        
        # check all items in currentGrid list
        for item in currentGrid:
            
            # create two empty lists
            allNumbers = []
            currentNumbers = []
        
            # determine all numbers remaining in the column - store in allNumbers
            for yRange in range(0,9):
                for columnNumbers in currentGrid[(item[0],yRange)]:
                    
                    if columnNumbers != ' ':
                        
                        allNumbers.append(columnNumbers)
                    
            # determine numbers remaining in individual cell being looked at - store in currentNumbers
            for cellNumbers in currentGrid[item]:
                
                if cellNumbers != ' ':
                    
                    
                    currentNumbers.append(cellNumbers)
        
            # look at numbers remaining in a cell. Check if they only appear in the column once.        
            if len(currentNumbers) > 1:
                
                
                for checkNumber in currentNumbers:
                    
                    
                    if allNumbers.count(checkNumber) == 1:
                        
                        # at this stage we know checkNumber appears only once, so we now update grid
                        currentState = currentGrid[item] 
                        for individualNumber in currentState:
                            
                            if individualNumber != checkNumber and individualNumber != ' ':
                                
                                currentState[individualNumber-1] = ' ' 
                                currentGrid[item] = currentState 
        return currentGrid                    
    
    def onlyNinGrid(currentGrid):
        

        # check all items in currentGrid list
        for item in currentGrid:
            

            # determine the co-ordinates for the grid we are dealing with
    
            if item[0] < 3:
                
                xGrid = [0,1,2]
            elif item[0] > 5:
                
                xGrid = [6,7,8]
            else:
                xGrid = [3,4,5]

            if item[1] < 3:
                yGrid = [0,1,2]
            elif item[1] > 5:
                yGrid = [6,7,8]
            else:
                yGrid = [3,4,5]

            # create two empty lists
            allNumbers = []
            currentNumbers = []

            #iterates through each of the nine numbers in the grid
            for x in xGrid:
                
                for y in yGrid:
                    
                    
            
                    # determine all numbers remaining in the grid - store in allNumbers
                    for gridNumbers in currentGrid[(x,y)]:
                        if gridNumbers != ' ':
                            allNumbers.append(gridNumbers)
                        
            # determine numbers remaining in individual cell being looked at - store in currentNumbers
            for cellNumbers in currentGrid[item]:
                
                if cellNumbers != ' ':
                    
                     currentNumbers.append(cellNumbers)
        
            # look at numbers remaining in a cell. Check if they only appear in the grid once.        
            if len(currentNumbers) > 1:
                
                
                for checkNumber in currentNumbers: 
                    if allNumbers.count(checkNumber) == 1: 
                    
                        # at this stage we know checkNumber appears only once, so we now update grid
                        currentState = currentGrid[item] 
                        for individualNumber in currentState:
                            
                            
                            if individualNumber != checkNumber and individualNumber != ' ': 
                                currentState[individualNumber-1] = ' ' 
                                currentGrid[item] = currentState 
                            
        return currentGrid



            













    mouseClicked=False
    mousex=0
    mousey=0
    


    while True: #main game loop
        mouseClicked=False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type== MOUSEBUTTONUP: #Če kliknemo miš
                mousex, mousey=event.pos #shran kje smo kliknl
                mouseClicked=True
                
        if mouseClicked==True:
            currentGrid = displaySelectedNumber(mousex, mousey, currentGrid)
            
        solveSudoku(currentGrid)  
        
        DISPLAYSURF.fill(WHITE) #na novo farbamo
        displayCells(currentGrid)
        drawGrid()    

        drawBox(mousex, mousey)

        pygame.display.update()
        FPSCLOCK.tick(FPS) #da redno posodablja
        
        

main()

