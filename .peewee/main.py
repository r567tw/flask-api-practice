from peewee import *

db = SqliteDatabase("sample.db")


class Base(Model):
    class Meta:
        database = db


class Test(Base):
    id = PrimaryKeyField()
    title = CharField(null=False)
    description = TextField()

    class Meta:
        order_by = ('title',)
        db_table = 'test'


# Test.create_table()
# Test.create(id=1, title='test', description='ttttt')
# Test.create(id=2, title='test', description='ttttt')
# record = Test.get(Test.title == 'test')
# print(record.id)
# print(record.description)

# record.description = 'new update'
# record.save()

# record.delete_instance()

# records = Test.select().get()
# print(records)
