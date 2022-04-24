x = [{'key': '1956', 'id': '9', 'rotulo': 'bla_bla', 'tipo': 'rose'}, {'key': '1888', 'tipo': 'bbb', 'rotulo': 'bla_bla', 'id': '9'}]

print(sorted(x, key=lambda d: d['key']) )