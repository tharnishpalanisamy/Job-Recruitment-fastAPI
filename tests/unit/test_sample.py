def test_sample_data(sample_data):
    assert sample_data["name"] == "Test User"
    assert sample_data["email"] == "test@example.com"
    