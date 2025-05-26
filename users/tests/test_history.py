import pytest


@pytest.mark.django_db
class TestAuditHistory:
    def test_customerprofile_history_create_update(self, profile):
        # initial creation record
        history = profile.history.all()
        assert history.count() == 1
        assert history.first().history_type == "+"

        # update creates a new record
        profile.phone_number = "0000000000"
        profile.save()
        history = profile.history.all()
        assert history.count() == 2
        latest = history.first()
        assert latest.history_type == "~"
        assert latest.phone_number == "0000000000"

    def test_address_history_create_update(self, address):
        # creation record exists
        history = address.history.all()
        assert history.count() == 1

        # update creates a new record
        address.city = "Rotterdam"
        address.save()
        history = address.history.all()
        assert history.count() == 2
        latest = history.first()
        assert latest.history_type == "~"
        assert latest.city == "Rotterdam"

    def test_address_history_delete(self, address):
        # delete adds a deletion record
        addr_id = address.id
        address.delete()
        HistoryModel = address.history.model
        deleted = HistoryModel.objects.filter(id=addr_id, history_type="-")
        assert deleted.exists()
