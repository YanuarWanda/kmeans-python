import math
import copy
import pandas as pd

# Inisialisasi variabel
k = 0
f = 0
t = 0.8
initialData = []
featureNames = []
featureLength = 0

# Baca data dari excel
def readData(filename):
    data = pd.read_excel(filename)
    data.drop(data.columns[0], axis=1, inplace=True)

    for i in range(len(data)):
        initialData.append({
            "features": [],
            "cluster": 1
        })
    for col in data.columns:
        featureNames.append(col)
        for i, val in enumerate(data[col]):
            if (col == "Kelompok"):
                initialData[i]["cluster"] = val
            else:
                initialData[i]["features"].append(val)

readData("original/kmeans.xlsx")
# readData("original/doc1.xlsx")
# readData("original/doc2.xlsx")
# readData("original/doc3.xlsx")
# readData("original/doc4.xlsx")
# readData("original/doc5.xlsx")
# readData("original/doc6.xlsx")
# readData("original/doc7.xlsx")
# readData("original/doc8.xlsx")
# readData("original/doc9.xlsx")

# Hitung jumlah kelompok (cluster)
for d in initialData:
    if d["cluster"] > k:
        k = d["cluster"]

# Hitung jumlah fitur (feature)
if (len(initialData) > 0):
    featureLength = len(initialData[0]["features"])

# Hitung centroid
def calculateCentroid(data):
    # Inisialisasi data kfx (Total data yang ada di setiap kelompok dan jumlah nilai di setiap kelompok)
    kfxs = []
    for i in range(k):
        kfxs.append({
            "total": 0,
            "values": []
        })
        for findex in range(featureLength):
            kfxs[i]["values"].append(0)

    # Menghitung jumlah data di setiap kelompok
    for d in data:
        kfxs[d["cluster"] - 1]["total"] += 1

    # Menghitung jumlah nilai data di setiap kelompok
    for findex in range(featureLength):
        for d in data:
            kfxs[d["cluster"] - 1]["values"][findex] += d["features"][findex]

    # Menghitung centroid
    centroids = []
    for kindex, kfx in enumerate(kfxs):
        centroids.append([])
        for findex in range(featureLength):
            if(kfx["total"] > 0):
                centroids[kindex].append(kfx["values"][findex] / kfx["total"])
            else:
                centroids[kindex].append(0)

    return [kfxs, centroids]

# Measuring distance
def measureDistance(centroids, data):
    distances = []
    for dindex, d in enumerate(data):
        distances.append([])
        for c in centroids:
            distance = 0
            for xindex, x in enumerate(d["features"]):
                distance += pow(abs(x - c[xindex]), 2)
            distance = math.sqrt(distance)
            distances[dindex].append(distance)
    return distances

# Periksa kelompok baru
def clusterCheck(distances, data):
    newData = copy.deepcopy(data)
    isChanged = False
    for dindex, d in enumerate(newData):
        for dii, di in enumerate(distances[dindex]):
            if di < distances[dindex][d["cluster"] - 1]:
                d["cluster"] = dii + 1
                isChanged = True
    return [isChanged, newData]

# Periksa deltaf
def calculateDeltaF(distances, data):
    oldF = f
    newF = 0
    for dindex, d in enumerate(data):
        newF += distances[dindex][d["cluster"] - 1]
    deltaf = abs(newF - oldF)
    return [deltaf, newF]

# Tampilkan hasil
def displayResult(data):
    dash = "---------"
    for x in range(featureLength + 1):
        dash += "----------------"
    print(dash)
    displayHeader = "| Data\t|"
    for x in featureNames:
        displayHeader = displayHeader + " " + x + "\t|"
    print(displayHeader)
    print(dash)
    for index, i in enumerate(data):
        displayData = "| " + str(index + 1) + "\t"
        for x in range(featureLength):
            displayData = displayData + "| " + str(i["features"][x]) + ("\t\t" if len(str(i["features"][x])) <= 5 else "\t")
        displayData += "| " + str(i["cluster"]) + "\t\t|"
        print(displayData)
    print(dash)

print("Data awal")
displayResult(initialData)
print("\n")

stop = False
oldData = initialData
newData = initialData
iterasi = 1
while (not stop):
    centroids = calculateCentroid(oldData)
    distances = measureDistance(centroids[1], oldData)
    newData = clusterCheck(distances, oldData)
    fdelta = calculateDeltaF(distances, oldData)
    oldData = newData[1]

    print("Iterasi " + str(iterasi))
    displayResult(oldData)
    print("Delta F\t: " + str(fdelta[0]))
    print("\n")

    if fdelta[0] < t or not newData[0]:
        stop = True

    f = fdelta[1]
    iterasi += 1

print("Hasil")
displayResult(newData[1])