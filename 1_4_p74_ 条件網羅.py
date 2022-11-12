#test対象の関数
def find_auth_user(username=None, password=None, team_name=None):
    try:
        users = User.objects.select_related('team').filter(
            (Q(username=username) | Q(email_iexact=username)),
        )
        if team_name:
            users = users.filter(team__name=team_name)
        else:
            users = users.filter(team_id=Team.PERSONAL_USERS_ID)
        return users.get()
    except User.DoesNotExist:
        return None

#test.py
class TestFindAuthUser:
    def test_team(self):
    def test_email(self):
    def test_email_case_insentisitive(self):
