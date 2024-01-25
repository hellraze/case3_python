import io, os, itertools, random

def main():
    random.seed(1183)
    print("Reading templates...")
    head = readFile('templates/head.tex')
    qStart = readFile('templates/qStart.tex')
    qStart2 = readFile('templates/qStart2.tex')
    qFinish = readFile('templates/qFinish.tex')
    tail = readFile('templates/tail.tex')

    print("Reading tasks...")
    tasks = readTasks()

    print("Reading students...")
    students = readStudents()

    print("Generating variants...")
    variants = generateVariants(tasks, len(students))
    random.shuffle(variants)


    os.makedirs(os.path.dirname("latex/main.tex"), exist_ok=True)
    
    out = io.open("latex/main.tex", "w", encoding='utf-8')
    print("Making main.tex file...")

    out.write(head)
    for i in range(len(variants)):
        out.write(qStart + str(students[i]) + qStart2)
        for taskNumber, task in enumerate(tasks):
            out.write(task[variants[i][taskNumber]-1])    
        out.write(qFinish)
    out.write(tail)
    out.close()

    out = io.open("latex/dump.tex", "w", encoding='utf-8')
    print("Making dump.tex file...")

    out.write(head)
    for i in range(len(tasks)):
        out.write(qStart + str(i+1) + qStart2)
        for k in range(len(tasks[i])):
            out.write(tasks[i][k])
        out.write(qFinish)
    out.write(tail)
    out.close()

    print("Done!")
    

def readTasks():
    result = []
    totalTasks = len(os.listdir('tasks'))
    print(totalTasks+1)
    for i in range(1,totalTasks):
        result.append([])
        totalVariants = len(os.listdir('tasks/%d' % i))
        for k in range(1,totalVariants):
            result[i-1].append(readFile('tasks/%d/%d.tex' % (i,k)))
    return result

def readStudents():
    file = io.open("students.txt", encoding='utf-8')
    result = file.readlines()
    file.close()
    return result

def generateVariants(tasks, total):
    counts = []
    for i in tasks:
        counts.append(len(i))
    result = set()
    while len(result) < total:
        result.add(generateVariant(counts))
    return list(result)

def generateVariant(counts):
    result = []
    for i in range(len(counts)):
        for j in counts[i]:
            result.append(j)
    return tuple(result)

def readFile(name):
    file = io.open(name, encoding='utf-8')
    text = file.read()
    file.close()
    return text


if __name__ == "__main__":
    main()
