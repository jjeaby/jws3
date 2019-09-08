import unittest
import jws3.bucket as bc

class TestStringMethods(unittest.TestCase):

    # def test_upper(self):
    #     self.assertEqual('foo'.upper(), 'FOO')
    #
    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())
    #
    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

    def test_delete_item(self):
        ret = bc.delete_file('dailywords', 'util')
        self.assertTrue(ret, msg='삭제 실패')

        ret = bc.get_pages_s3_keys('dailywords', limit=1, search='util2.py')
        self.assertFalse(ret, msg='삭제 실패')



    # ret = bc.create_bucket('dailywords', 'ap-northeast-2')
    # print("create_bucket:", ret)

    # print("-"*100)
    #
    # ret = upload_file('/home/jjeaby/Dev/02.jjeaby.github/jws3/jws3/bucket.py', 'dailywords', 'bucket.py', acl='public')
    # print("upload_file:", ret)
    # print("-"*100)
    #
    # ret = upload_file('/home/jjeaby/Dev/02.jjeaby.github/jws3/jws3/bucket.py', 'dailywords', 'util2.py', acl='public')
    # print("upload_file:", ret)
    # print("-"*100)
    #
    # ret = list_files('dailywords')
    # print('list_files', ret)
    # print("-"*100)
    #
    # ret = get_pages_s3_keys('dailywords', limit=1, search='util')
    # print('get_pages_s3_keys_limit=1', ret)
    # print("-"*100)
    #
    # ret = get_pages_s3_keys('dailywords', limit=2, search='.')
    # print('get_pages_s3_keys', ret)
    #
    # ret = get_pages_s3_keys('dailywords', limit=2, search='.', NextContinuationToken=ret['NextContinuationToken'])
    # print('get_pages_s3_keys', ret)

    # ret = delete_bucket('dailywords')
    # print("delete_bucket:", ret)

if __name__ == '__main__':
    unittest.main()
