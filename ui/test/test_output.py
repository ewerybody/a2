import a2output


def test_get_set_vars():
    bucket = []
    def test(msg, bucket=bucket):
        bucket.append(msg)
    a2output.connect(test)
    assert bucket == []
    print('something')
    assert bucket != []
