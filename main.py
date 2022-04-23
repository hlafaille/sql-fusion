from factories.DataclassFactory import DataclassFactory
from objects.SQLColumn import Column
from objects.SchemaAlias import SchemaAlias
from objects.SchemaMap import SchemaMap, RootSchemaMap

if __name__ == "__main__":
    schema = RootSchemaMap(columns=[
        SchemaAlias(database_name="incremental",
                    pretty_name="id",
                    datatype=int),
        Column("date", str),
        SchemaMap(columns=[
            SchemaAlias(database_name="shipping_line1", pretty_name="line1", datatype=str),
            SchemaAlias(database_name="shipping_line2", pretty_name="line2", datatype=str),
            SchemaAlias(database_name="shipping_zip", pretty_name="shipping", datatype=str),
            SchemaAlias(database_name="shipping_city", pretty_name="city", datatype=str),
            SchemaAlias(database_name="shipping_state", pretty_name="state", datatype=str),
            SchemaAlias(database_name="shipping_country", pretty_name="country", datatype=str),
        ], group_name="ShippingAddress"),
        SchemaAlias(database_name="credit_card_details", pretty_name="credit_card", datatype=str),
        SchemaMap(columns=[
            Column("id", int),
            SchemaAlias(database_name="firstName", pretty_name="first_name", datatype=str),
            SchemaAlias(database_name="lastName", pretty_name="last_name", datatype=str),
        ], group_name="Employee"),
        SchemaMap(columns=[
            Column("id", int),
            SchemaAlias(database_name="company_name", pretty_name="name", datatype=str),
            SchemaMap(columns=[
                SchemaAlias(database_name="billing_line1", pretty_name="line1", datatype=str),
                SchemaAlias(database_name="billing_line2", pretty_name="line2", datatype=str),
                SchemaAlias(database_name="billing_zip", pretty_name="zip", datatype=int),
                SchemaAlias(database_name="billing_city", pretty_name="city", datatype=str),
                SchemaAlias(database_name="billing_state", pretty_name="state", datatype=str),
            ], group_name="CustomerAddress")
        ], group_name="Customer"),
        Column("customer_po", int),
        Column("items", dict),
        Column("notes", dict),
        Column("previous_document", int),
        SchemaMap(columns=[
            Column("shipping_account", str),
            Column("shipping_cost", float),
            Column("shipping_method", str)
        ], group_name="ShippingInformation")

    ],
        root_name="SalesInvoice")

    dataclass_factory = DataclassFactory(schema)
