class DescriptorClass(object):
    def __get__(self, instance, owner):
        print("called get magic method")
        return 23


class SampleClass(object):
    class_attribute = DescriptorClass()


sample_instance = SampleClass()
print(sample_instance.class_attribute)
