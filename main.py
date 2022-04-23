from objects.SchemaMap import SchemaMap

if __name__ == "__main__":
    schema = SchemaMap(
        ["isn",
         SchemaMap(
             group_name="customer",
             columns=["name",
                      SchemaMap(
                          group_name="address",
                          columns=["line1", "line2", "zip", "city", "state", "country"]
                      )
                      ]
         )
         ]
    )
    print("ass pp {0}".format(schema.columns))
