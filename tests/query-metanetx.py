#!/usr/bin/env python
""" Sample queries with MetaNetX compounds and reactions """

import os
import unittest

from nosqlbiosets.dbutils import DBconnection


def query(es, index, qc, doc_type=None, size=0):
    print("querying '%s'  %s" % (doc_type, str(qc)))
    r = es.search(index=index, doc_type=doc_type,
                  body={"size": size, "query": qc})
    nhits = r['hits']['total']
    return r['hits']['hits'], nhits


class QueryMetanetx(unittest.TestCase):
    d = os.path.dirname(os.path.abspath(__file__))
    index = "nosqlbiosets"

    def query_sample_keggids(self, dbc, cids):
        if dbc.db == 'Elasticsearch':
            qc = {"match": {"xrefs": ' '.join(cids)}}
            hits, n = query(dbc.es, self.index, qc, "compound", len(cids))
            mids = [xref['_id'] for xref in hits]
        else:  # MongoDB
            qc = {'xrefs': {'$elemMatch': {'$elemMatch': {'$in': cids}}}}
            hits = dbc.mdbi["compound"].find(qc, limit=10)
            mids = [c['_id'] for c in hits]
        print(mids)
        return mids

    def query_sample_metanetxids(self, dbc, mids):
        if dbc.db == 'Elasticsearch':
            qc = {"ids": {"values": mids}}
            hits, n = query(dbc.es, self.index, qc, "compound", len(mids))
            descs = [c['_source']['desc'] for c in hits]
        else:  # MongoDB
            qc = {"_id": {"$in": mids}}
            hits = dbc.mdbi["compound"].find(qc, limit=10)
            descs = [c['desc'] for c in hits]
        print(descs)
        return descs

    def test_es(self):
        dbc = DBconnection("Elasticsearch", self.index, recreateindex=False)
        mids = self.query_sample_keggids(dbc, ['C00116', 'C05433'])
        self.assertEqual(mids, ['MNXM2000', 'MNXM89612'])
        descs = self.query_sample_metanetxids(dbc, mids)
        self.assertEqual(descs, ['glycerol', 'alpha-carotene'])

    def test_mongodb(self):
        dbc = DBconnection("MongoDB", self.index, recreateindex=False)
        mids = self.query_sample_keggids(dbc, ['C00116', 'C05433'])
        self.assertEqual(mids, ['MNXM2000', 'MNXM89612'])
        descs = set(self.query_sample_metanetxids(dbc, mids))
        self.assertSetEqual(descs, {'glycerol', 'alpha-carotene'})


if __name__ == '__main__':
    unittest.main()
