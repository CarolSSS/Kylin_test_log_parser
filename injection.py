import os

ctestFile = "../kylin/core-common/src/main/resources/ctest.properties"


def inject(name, value):
    with open(ctestFile, 'w') as fp:
        print("ctest file at : " + ctestFile)
        print("inject parameter: " + name + " =" + value)
        fp.write(name + " =" + value)


def delete():
    print("clear ctest File at " + ctestFile)
    os.remove(ctestFile)
    f = open(ctestFile, "w")
    f.close()


inject("kylin.env.zookeeper-base-sleep-time", "5555")
# delete()
