import os # Buat bersihin layar
import math # yang dipake math.sqrt buat ngitung nilai akar
import copy # Buat bikin duplikat data objek
from random import randint # Buat cari nilai random kelompok
import pandas as pd # Buat baca data dari excel

# Clear layar terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Inisialisasi jumlah kelompok, f, dan nilai threshold
k = int(input("Masukkan jumlah kelompok: "))
f = 0
t = float(input("Masukkan nilai threshold: "))

# Clear layar terminal
os.system('cls' if os.name == 'nt' else 'clear')

initialData = [] # Tempat menyimpan data iterasi 0 / data awal
featureNames = [] # Tempat menyimpan daftar nama fitur untuk ditampilkan

# Buat fungsi untuk baca data dari excel
def readData(filename):
    data = pd.read_excel(filename)
    data.drop(data.columns[0], axis=1, inplace=True) # Data kolom pertama tidak dibaca karena isinya data nomor urutan data

    # Inisialisasi isi data awal
    for i in range(len(data)):
        initialData.append({
            "features": [],
            "cluster": randint(1, k) # Memasukkan setiap data ke kelompok secara acak
        })

    # Mengisi data awal dari excel
    for col in data.columns:
        featureNames.append(col)
        for i, val in enumerate(data[col]):
            initialData[i]["features"].append(val)

# readData("random/kmeans.xlsx")
# readData("random/doc1.xlsx")
# readData("random/doc2.xlsx")
# readData("random/doc3.xlsx")
# readData("random/doc4.xlsx")
# readData("random/doc5.xlsx")
# readData("random/doc6.xlsx")
# readData("random/doc7.xlsx")
# readData("random/doc8.xlsx")
readData("random/doc9.xlsx")

# Menghitung centroid setiap kelompok
def calculateCentroid(data):
    # Mencari nilai kfx
    kfxs = []
    for i in range(k):
        # Inisialisasi data kfx
        kfxs.append({
            "total": 0,
            # Tempat menyimpan total data di setiap kelompok
            "values": []
            # Tempat menyimpan jumlah nilai fitur di setiap kelompok
        })

        for _ in range(len(featureNames)):
            kfxs[i]["values"].append(0)

    # Menghitung total data di setiap kelompok
    for d in data:
        kfxs[d["cluster"] - 1]["total"] += 1

    # Menghitung jumlah nilai fitur di setiap kelompok
    for fIndex in range(len(featureNames)):
        for d in data:
            kfxs[d["cluster"] - 1]["values"][fIndex] += d["features"][fIndex]

    # Menghitung centroid
    centroids = []
    for kIndex, kfx in enumerate(kfxs):
        centroids.append([])
        for fIndex in range(len(featureNames)):
            if(kfx["total"] > 0):
                centroids[kIndex].append(kfx["values"][fIndex] / kfx["total"])
            else:
                centroids[kIndex].append(0)

    print("kfxs:\n", kfxs)
    print("centroids:\n", centroids)

    return centroids

# Menghitung jarak data ke centroid
def measureDistance(centroids, data):
    distances = []
    for dIndex, d in enumerate(data):
        distances.append([])
        # Menghitung jarak menggunakan rumus euclidean
        for c in centroids:
            distance = 0
            for xIndex, x in enumerate(d["features"]):
                distance += pow(abs(x - c[xIndex]), 2)
            distance = math.sqrt(distance)
            distances[dIndex].append(distance)
    print("Jarak:\n", distances)
    return distances

# Memindahkan setiap data ke kelompok dengan centroid terdekat
def clusterCheck(distances, data):
    newData = copy.deepcopy(data)
    isChanged = False
    for dataIndex, d in enumerate(newData):
        for distanceIndex, di in enumerate(distances[dataIndex]):
            if di < distances[dataIndex][d["cluster"] - 1]:
                d["cluster"] = distanceIndex + 1
                isChanged = True
    return [isChanged, newData]

# Menghitung fungsi f (objektif)
def calculateDeltaF(distances, data):
    oldF = f
    newF = 0
    for dIndex, d in enumerate(data):
        newF += distances[dIndex][d["cluster"] - 1]
    deltaf = abs(newF - oldF)
    return [deltaf, newF]

# Membuat fungsi untuk menampilkan data
def displayResult(data):
    dash = "---------"
    for x in range(len(featureNames) + 1):
        dash += "----------------"
    print(dash)

    displayHeader = "| Data\t|"
    for x in featureNames:
        displayHeader = displayHeader + " " + x + "\t|"
    displayHeader = displayHeader + " Kelompok\t|"
    print(displayHeader)
    print(dash)

    for index, i in enumerate(data):
        displayData = "| " + str(index + 1) + "\t"
        for x in range(len(featureNames)):
            displayData = displayData + "| " + str(i["features"][x]) + ("\t\t" if len(str(i["features"][x])) <= 5 else "\t")
        displayData += "| " + str(i["cluster"]) + "\t\t|"
        print(displayData)
    print(dash)

print("k = ", k)
print("f = ", f)
print("t = ", t)

print("\nData awal")
displayResult(initialData)
print("\n")

stop = False
oldData = initialData
newData = initialData
iterasi = 1
while (not stop):
    centroids = calculateCentroid(oldData)
    distances = measureDistance(centroids, oldData)
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