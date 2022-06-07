from unittest import mock

import pytest
import requests
from celery.exceptions import Retry

from project.users import tasks
from project.users.factories import UserFactory
from project.users.models import User
from project.users.tasks import task_add_subscribe


def test_post_succeed(db_session, monkeypatch):
    user = UserFactory.create()

    mock_requests_post = mock.MagicMock()
    monkeypatch.setattr(requests, "post", mock_requests_post)

    task_add_subscribe(user.id)

    mock_requests_post.assert_called_with(
        "https://httpbin.org/delay/5",
        data={"email": user.email}
    )


def test_exception(db_session, monkeypatch):
    user = UserFactory.create()

    mock_requests_post = mock.MagicMock()
    monkeypatch.setattr(requests, "post", mock_requests_post)

    mock_task_add_subscribe_retry = mock.MagicMock()
    monkeypatch.setattr(task_add_subscribe, "retry", mock_task_add_subscribe_retry)

    mock_task_add_subscribe_retry.side_effect = Retry()
    mock_requests_post.side_effect = Exception()

    with pytest.raises(Retry):
        task_add_subscribe(user.id)


# from tests/users/test_views.py
def test_user_subscribe_view(client, db_session, settings, monkeypatch, user_factory):
    user = user_factory.build()

    task_add_subscribe = mock.MagicMock(name="task_add_subscribe")
    task_add_subscribe.return_value = mock.MagicMock(task_id="task_id")
    monkeypatch.setattr(tasks.task_add_subscribe, "delay", task_add_subscribe)

    response = client.post(
        "/users/user_subscribe/",
        json={"email": user.email, "username": user.username}
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "send task to Celery successfully",
    }

    # query from the db again
    user = db_session.query(User).filter_by(username=user.username).first()
    task_add_subscribe.assert_called_with(
        user.id
    )


# from tests/users/test_tasks.py
def test_post_succeed(db_session, monkeypatch, user):
    mock_requests_post = mock.MagicMock()
    monkeypatch.setattr(requests, "post", mock_requests_post)

    task_add_subscribe(user.id)

    mock_requests_post.assert_called_with(
        "https://httpbin.org/delay/5",
        data={"email": user.email}
    )


# from tests/users/test_tasks.py
def test_exception(db_session, monkeypatch, user):
    mock_requests_post = mock.MagicMock()
    monkeypatch.setattr(requests, "post", mock_requests_post)

    mock_task_add_subscribe_retry = mock.MagicMock()
    monkeypatch.setattr(task_add_subscribe, "retry", mock_task_add_subscribe_retry)

    mock_task_add_subscribe_retry.side_effect = Retry()
    mock_requests_post.side_effect = Exception()

    with pytest.raises(Retry):
        task_add_subscribe(user.id)
