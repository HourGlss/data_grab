import pickle

data = pickle.load(open('./../data/000000Z.pickle', 'rb'))
types = set()
for k, v in data.items():
    if k == "aircraft":
        for e in v:
            before = len(types)
            types.add(e['type'])
            after = len(types)
            if before != after:
                print(e['type'])
                print(f"\t{[e.keys()]}")
                try:
                    print(e['hex'],e['lat'],e['lon'])
                except:
                    pass
