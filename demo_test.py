class Student(object):
    pass


Student.name = 'xm'

print (Student.name)

def set_age(self,age):
    self.age = age

Student.set_age = set_age
s = Student()
s.set_age(20)
print (s.age)  #20



class A:
    def demo(self):
        print(1)

def demo2(self,step):
    print(2)
A.demo2=demo2
A().demo2("haha")




