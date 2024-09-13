import person_pb2
person =person_pb2.Person()
person.name = "Linda"
person.age = 25

print(person.SerializeToString())