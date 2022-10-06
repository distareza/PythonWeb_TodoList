from Data import Data

data = Data()
data.drop_db()
data.create_db()
data.addMasterData("Master1", "Data")
data.addDetailData("Master1", "Detail 1")
data.addDetailData("Master1", "Detail 2")
data.addDetailData("Master1", "Detail 3")

data.addMasterData("Master2", "Data")
data.addDetailData("Master2", "Detail 1")
data.addDetailData("Master2", "Detail 2")
data.addDetailData("Master2", "Detail 3")

for item in data.getAllData():
    print(item)


print(data.getData("Master2"))