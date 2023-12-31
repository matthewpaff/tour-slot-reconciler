import unittest

from slots_tool.conflicts import detect


class ConflictTests(unittest.TestCase):
    def test_latest_versions_overlap_and_stale_versions_do_not(self):
        slot = lambda ident,start,end,version: {'id':ident,'start':start,'end':end,'expires_at':300,'version':version}
        data={'now':50,'slots':[slot('a',100,180,1),slot('a',100,130,2),
                                slot('b',120,150,1),slot('c',160,200,1)]}
        result=detect(data)
        self.assertEqual(result['total'],1)
        self.assertEqual(result['overlaps'],[{'first':'a','second':'b','start':120,'end':130}])

    def test_result_is_bounded_but_total_remains_exact(self):
        data={'now':0,'slots':[{'id':str(i),'start':10,'end':20,'expires_at':30,'version':1} for i in range(5)]}
        result=detect(data,limit=2)
        self.assertEqual(result['total'],10)
        self.assertEqual(len(result['overlaps']),2)
        self.assertTrue(result['truncated'])
