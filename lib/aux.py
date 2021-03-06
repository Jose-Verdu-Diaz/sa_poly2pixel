###############################################
##                                           ##
##      Auxiliary classes and functions      ##
##                                           ##
###############################################


##################################
##        Terminal Colors       ##
##################################
def get_color_escape(r, g, b, background=False):
    return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    DARKGREY = '\u001b[38;5;232m'

##################################
##      Check if is number      ##
##################################
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

##################################
##        Progress Bar          ##
##################################
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def printHeader():
    print(f'{bcolors.BOLD}{bcolors.OKBLUE}8888888b.   .d88888b.  888    Y88b   d88P      {bcolors.FAIL} .d8888b.       {bcolors.OKBLUE}8888888b. 8888888 Y88b   d88P 8888888888 888      \n{bcolors.OKBLUE}888   Y88b d88P" "Y88b 888     Y88b d88P       {bcolors.FAIL}d88P  Y88b      {bcolors.OKBLUE}888   Y88b  888    Y88b d88P  888        888      \n{bcolors.OKBLUE}888    888 888     888 888      Y88o88P        {bcolors.FAIL}       888      {bcolors.OKBLUE}888    888  888     Y88o88P   888        888      \n{bcolors.OKBLUE}888   d88P 888     888 888       Y888P         {bcolors.FAIL}     .d88P      {bcolors.OKBLUE}888   d88P  888      Y888P    8888888    888      \n{bcolors.OKBLUE}8888888P"  888     888 888        888          {bcolors.FAIL} .od888P"       {bcolors.OKBLUE}8888888P"   888      d888b    888        888      \n{bcolors.OKBLUE}888        888     888 888        888          {bcolors.FAIL}d88P"           {bcolors.OKBLUE}888         888     d88888b   888        888      \n{bcolors.OKBLUE}888        Y88b. .d88P 888        888          {bcolors.FAIL}888"            {bcolors.OKBLUE}888         888    d88P Y88b  888        888      \n{bcolors.OKBLUE}888         "Y88888P"  88888888   888          {bcolors.FAIL}888888888       {bcolors.OKBLUE}888       8888888 d88P   Y88b 8888888888 88888888 {bcolors.ENDC}\n')

def printLoadedProject(prj):
    print(bcolors.BOLD + bcolors.OKBLUE + 'Loaded project: {project}'.format(project= bcolors.FAIL + 'None' if prj == None else bcolors.OKGREEN + prj.name) + bcolors.ENDC )

def printTable(headers, data, colors = None):
    #######################################
    # Calc the longest row of each column #
    #######################################
    columnsMax = [*(0 for i in headers)]
    for i,col in enumerate(data):
        for row in col:
            if len(str(row)) + 2 > columnsMax[i]: columnsMax[i] = len(str(row)) + 2
    #If header is the longest
    for i,h in enumerate(headers):
        if len(str(h)) + 2 > columnsMax[i]: columnsMax[i] = len(str(h)) + 2

    separatorList = ['┳','┃ ', '╋']
    edgeListL = ['┏','┃ ','┣']
    edgeListR = ['┓','┃','┫']

    #################
    # Print Headers #
    #################
    for i in range(3):

        line = []
        for j,h in enumerate(headers):
            if j == len(headers) - 1:
                separator = ''
            else:
                separator = separatorList[i]
            
            if i == 1:
                line.append(h + "".join([*(" " for k in range(columnsMax[j] - len(h) - 1))]) + separator)
            else:
                line.append("".join([*("━" for k in range(columnsMax[j]))]) + separator)

        print(f'{edgeListL[i]}{"".join([*(line)])}{edgeListR[i]}')

    colLen = len(data)
    rowLen = len(data[0])

    for i in range(rowLen):
        line=[]
        for j in range(colLen):
            if not colors == None and j == len(headers) - 2:
                separator = '┃'
            elif j == len(headers) - 1:
                separator = ''
            else:
                separator = '┃ '

            if not colors == None and j == len(headers) - 1:
                line.append(colors[i] + "".join([*(" " for k in range(columnsMax[j]))]) + bcolors.ENDC + separator)
            else:   
                line.append(data[j][i] + "".join([*(" " for k in range(columnsMax[j] - len(data[j][i]) - 1))]) + separator)
        print(f'{edgeListL[1]}{"".join([*(line)])}{edgeListR[1]}')
    
    line = []
    for i,h in enumerate(headers):
        if i == len(headers) - 1:
            separator = ''
        else:
            separator = '┻'      
        line.append("".join([*("━" for k in range(columnsMax[i]))]) + separator)
    print(f'┗{"".join([*(line)])}┛')
