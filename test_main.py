"""Contains tests for the GitHub user viewer."""

import pytest

from main import get_github_user_details, APIError


class TestGetGithubUserDetails:
    """Class containing tests for the get_github_user_details() function."""

    def test_returns_a_dict(self, requests_mock):
        """Checks that the function returns a dict."""

        requests_mock.get("https://api.github.com/users/test",
                          status_code=200,
                          json={})

        response = get_github_user_details("test")

        assert isinstance(response, dict)

    def test_raises_error_on_400(self, requests_mock):
        """Checks that the function raises an appropriate exception if the API
        responds with a 400 code."""

        requests_mock.get("https://api.github.com/users/test",
                          status_code=400)

        with pytest.raises(APIError) as err_info:
            get_github_user_details("test")

        assert isinstance(err_info.value, APIError)
        assert err_info.value.message == "Invalid username."
        assert err_info.value.code == 400

    def test_raises_error_on_500(self, requests_mock):
        """Checks that the function raises an appropriate exception if the API
        responds with a 500 code."""

        requests_mock.get("https://api.github.com/users/test",
                          status_code=500)

        with pytest.raises(APIError) as error_info:
            get_github_user_details("test")

        assert isinstance(error_info.value, APIError)
        assert error_info.value.message == "Server error."
        assert error_info.value.code == 500

    def test_calls_the_api(self, requests_mock):
        """Checks that the function actually attempts to call the API."""

        requests_mock.get("https://api.github.com/users/test",
                          status_code=200,
                          json={})

        get_github_user_details("test")

        assert requests_mock.called
        assert requests_mock.call_count == 1
