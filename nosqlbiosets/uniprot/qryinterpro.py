#!/usr/bin/env python
""" Query InterPro data indexed with MongoDB """

from nosqlbiosets.qryutils import Query


class QueryInterPro(Query):

    def id2names(self, ids):
        assert self.dbc.db == "MongoDB"
        qc = [
            {"$match":
                {"$or": [
                    {"external_doc_list.db_xref": {
                        '$elemMatch': {"dbkey": {"$in": list(ids)}
                                       }}},
                    {"member_list.db_xref.dbkey": {"$in": list(ids)}
                     }
                ]}},
            {"$facet": {
                "external": [
                    {"$unwind": "$external_doc_list.db_xref"},
                    {"$project": {
                        "_id": "$external_doc_list.db_xref.dbkey",
                        "name": "$name"}}
                ],
                "member": [
                    {"$unwind": "$member_list.db_xref"},
                    {"$project": {
                        "_id": "$member_list.db_xref.dbkey",
                        "name": "$name"}}
                ]
            }}
        ]
        r = list(self.aggregate_query(qc))
        names = dict()
        for facet in [r[0]['external'], r[0]['member']]:
            j = {i['_id']: i['name'] for i in facet}
            names.update(j)
        return names
