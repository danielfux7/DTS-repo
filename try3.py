class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

people = [Person("Alice", 20), Person("Bob", 30), Person("Charlie", 40)]

if __name__ == '__main__':

    for person in people:
        print(f"{person.name} is {person.age} years old.")

    print(people[0].name)
    print(people[1].age)