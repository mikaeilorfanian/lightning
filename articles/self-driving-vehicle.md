# Types versus Classes
- Programming to interfaces or types is better than programming to implementation or classes.
- Some programming languages use “duck-typing” not “duck-classing”.
- One of the major additions to Python in recent years is called “Type Hinting” not “Class Hinting”.

What do these three statements have in common? They imply that the type of an object and its class are not the same thing. Do you know the difference? Knowing it is key if you want to write good object oriented code and benefit from interfaces and duck-typing.   
In this article, we’ll go through what types and classes are and put our newfound knowledge to use by exploring duck-typing and programming to interfaces. Let’s get started!   
## Type
> The type of an object is just a name for its interface!   

The *interface* of an object tells you what operations you can run on it. It does this by specifying the methods you can call and what these methods expect and return. Here’s an example:   

    :::python   
    class SelfDrivingVehicle:
        def start(self):
            pass

        def drive(self, destrination: str):
            pass

This interface tells you that objects of type `SelfDrivingVehicle` must have two methods (`start` and `drive`) with the specified signatures. For example, when you ask an object of type `SelfDrivingVehicle` to `drive` you should give it the `destination` as a string (`destination`: str).   
The type of an object is just a name for its interface. The following snippet shows a `Car` class whose instances have the `SelfDrivingVehicle` type because you can ask them to `start` and `drive`:   

    :::python
    class Car:
        def start(self): 
            pass
    
        def drive(self, destination: str):
            pass

An object can have multiple interfaces. For example, in the following snippet we add type `Iterable` (a built-in type in Python) to our `Car`:   

    :::python
    class Car:
        def start(self):  # required for Vehicle type
            pass
    
        def drive(self, destination: str):  # required for Vehicle type
            pass
    
        def __iter__(self):  # required for Iterator type
            pass
    
        def __next__(self):   # required for Iterator type
            pass
    
    car = Car()
    for part in car:
        print(part)

## Class
> The class of an object is about its implementation details!   

An object’s class defines its data, representation, and the operations it can perform. An object’s class is about its implementation.   
Let’s implement how `Car`‘s `start` and `drive` methods actually work:   

    :::python
    class Car:
        def start(self):
            self.engine = 'on'
    
        def drive(self, destination: str):
            if self.engine == 'on':
                self.drive_to(destination)

`self.engine` and the string "`on`" are implementation details of `Car`. They have nothing to do with its type and `SelfDrivingVehicle` doesn’t mention any of them either.   
An important difference between class and type is that an object can have multiple types but only one class. Most languages have built-in methods for getting the class of an object. For example, in Python you can use `type(object)` to get `object`‘s class (which is an oxymoron, of course). But, getting the type of an object is not that easy to do in Python because of duck-typing.   

## Duck-typing
> It quacks like a duck until it doesn't!   

In Python duck-typing means that at *run-time* the interpreter looks up methods and attributes *only* when they are *accessed*.   
To illustrate this, let’s step through the below block of code using the python debugger:   

    :::python
    class A:
        def just_do_it(self):
            pass
    
    def call_some_methods(obj: A):
        import pdb; pdb.set_trace()  # this is like a breakpoint
        obj.just_do_it()
        obj.cant_do_it()  # we're calling a non-existing method here
    
    a = A()
    call_some_methods(a)

Since we set a trace (`pdb.set_trace()`), when we run the code we’ll see something like this:   

    :::bash
    $ python3 tvsclsdbg.py
    > tvsclsdbg.py(7)call_some_methods()
    -> obj.just_do_it()
    (Pdb)

As you can see Python has created an instance of `A` and now we’re in the `call_come_methods` function. The fact that we’re going to call a non-existing method on a doesn’t bother Python because that line of code hasn’t been executed yet.   
Let’s execute the next line of code:   

    :::bash
    (Pdb) next
    > tvsclsdbg.py(8)call_some_methods()
    -> obj.cant_do_it()
    (Pdb)

Python ran `obj.just_do_it()` and still no errors were thrown. Finally, we try to call the non-existing `cant_do_it()` method:   

    :::bash
    (Pdb) next
    AttributeError: 'A' object has no attribute 'cant_do_it'
    > tvsclsdbg.py(8)call_some_methods()
    -> obj.cant_do_it()
    (Pdb)

And we crashed as we tried to invoke the non-existing method. This is what duck-typing means. The methods and attributes you call are not resolved until you execute the line that makes those calls. You might be wondering why this is a big deal? Read on.   

## Duck-typing Makes Code User-friendly
It is a well-known principle of object oriented programming that relying on interfaces is better than relying on implementation (more on this later). Duck-typing allows you to take this idea to an extreme because the compiler and interpreter don’t care about the class of objects you pass around in your program! As a result you can write code that’s powerful yet user friendly.   
For example, Python’s decorators allow you to apply the decorator pattern to any object with just one line of code. Or, with `mock.patch` you can easily change the behavior of any object during run-time.   
So, we can make simple yet powerful structures in our programs because of duck-typing’s reliance on types rather than classes. If this is such a good idea, then how can we use it to our advantage in our programs? By programming to interfaces instead of implementation…    

## Programming to Interfaces
Although the Python language always relies on interfaces that doesn’t stop us from writing code that depends on concrete implementations:   

    :::python
    class Car:
        def start(self) -> bool:
            self.engine = 'on'
    
        def drive(self, destination: str) -> None:
            if self.engine == 'on':
                self._drive_to(destination)
            else:
                raise CarNotOnError
    
    car = Car()
    if car.engine == 'on':  # relies on implementation
        car._drive_to(destination)  # relies on implementation
    else:
        car.engine = 'on'  # relies on implementation
        car._drive_to(destination)   # relies on implementation

The code that uses an instance of the car object has knowledge of the following implementation details about it:   
- car has an engine attribute.   
- car cannot be driven if the engine is not on   
- engine can be turned on by a simple assignment    


Let’s imagine that `car` is used in similar way throughout the code-base. If any of the implementation details of `car` changes (e.g. before the `engine` can be `on` there must be a minimum level of electric charge in the car’s `battery` attribute) then you’d have to modify code in multiple places throughout the code-base and make sure you haven’t missed anything!   
Now, imagine that programming to implementation details (or classes) is habit among the developers programming in this code-base. You’d probably end up with a lot of fragile, hard-to-test, hard-to-read, and hard-to-fix code.   
But, by programming to interfaces you end up with code such as   

    :::bash
    car = Car()
    car.drive(destination)

Now, we’ve reduced our dependency on `car` to just one method. Instead of manipulating the car directly, we simply ask it to `drive`. Our code has no knowledge of how `car` is implemented. We depend only on the interface defined by the `SelfDrivgingVehicle` type.   
