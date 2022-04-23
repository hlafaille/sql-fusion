import pprint

from objects.SQLColumn import Column
from objects.SchemaAlias import SchemaAlias
from objects.SchemaInterpreter import SchemaInterpreter
from objects.SchemaMap import SchemaMap

if __name__ == "__main__":
    schema = SchemaMap(
        [
            Column("isn", int),
            SchemaMap(columns=[
                SchemaAlias("customer_name", "name", str),
                SchemaAlias("customer_address_line1", "line1", str),
                SchemaAlias("customer_address_line2", "line2", str),
                SchemaAlias("customer_address_zip", "zip", int)],
                group_name="customer"),
            SchemaMap(columns=[
                Column("id", int),
                SchemaAlias("first_name", "firstName", str),
                SchemaAlias("last_name", "lastName", str),
                Column("status", str)
            ],
                group_name="employee")
        ])

    interpreter = SchemaInterpreter(schema)

    pp = pprint.PrettyPrinter(indent=4)
    for x in interpreter.master_json:
        pp.pprint(x)
    # print("----------------")
    print(interpreter.master_json)
