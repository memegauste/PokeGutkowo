"""Regression tests for the public API, admin editor, and site settings."""
import pytest
from django.core.exceptions import ValidationError
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.urls import reverse

from pokegutkowo.models import Player, Post, Settings

pytestmark = pytest.mark.django_db


@pytest.fixture
def player():
    return Player.objects.create(
        nickname='Trener', level=40, team=Player.MYSTIC, trainer_code='123456789012',
    )


@pytest.mark.parametrize('endpoint', ['players_view', 'posts_view'])
def test_empty_lists(client, endpoint):
    response = client.get(reverse(endpoint))
    assert response.status_code == 200
    assert response.json() == []


def test_players_api(client, player):
    response = client.get(reverse('players_view'))
    assert response.status_code == 200
    assert response.json() == [{
        'id': player.pk, 'nickname': 'Trener', 'level': 40,
        'team': 'mystic', 'trainer_code': '123456789012',
    }]


def test_posts_api_serializes_author_and_orders_newest_first(client, player):
    old = Post.objects.create(title='Pierwszy', context='<p>Cześć!</p>', author=player)
    new = Post.objects.create(title='Najnowszy', context='<strong>Nowy</strong>', author=player)
    response = client.get(reverse('posts_view'))
    assert response.status_code == 200
    assert response.json() == [
        {'id': new.pk, 'title': 'Najnowszy', 'context': '<strong>Nowy</strong>', 'author': 'Trener'},
        {'id': old.pk, 'title': 'Pierwszy', 'context': '<p>Cześć!</p>', 'author': 'Trener'},
    ]


def test_empty_settings_is_an_object(client):
    response = client.get(reverse('settings_view'))
    assert response.status_code == 200
    assert response.json() == {}


def test_settings_api_includes_absolute_media_url(client, player):
    settings = Settings.objects.create(
        title='Gutkowo', owner_acc=player, owner_about='Cześć!',
        owner_screenshot='trainer.png', discord='https://discord.gg/example',
    )
    response = client.get(reverse('settings_view'))
    assert response.status_code == 200
    assert response.json() == {
        'id': settings.pk, 'title': 'Gutkowo', 'owner_acc': player.pk,
        'owner_about': 'Cześć!', 'owner_screenshot': 'http://testserver/media/trainer.png',
        'discord': 'https://discord.gg/example',
    }


def test_settings_allows_editing_the_single_instance():
    settings = Settings.objects.create(title='Gutkowo')
    settings.title = 'Nowa nazwa'
    settings.full_clean()
    settings.save()
    assert Settings.objects.get().title == 'Nowa nazwa'


def test_settings_rejects_another_instance():
    Settings.objects.create(title='Gutkowo')
    with pytest.raises(ValidationError, match='Można utworzyć tylko 1'):
        Settings(title='Druga strona').full_clean()


def test_settings_validation_recovers_when_duplicate_rows_already_exist():
    Settings.objects.bulk_create([Settings(title='Pierwsza'), Settings(title='Druga')])
    with pytest.raises(ValidationError, match='Można utworzyć tylko 1'):
        Settings.objects.first().full_clean()


@pytest.mark.parametrize('endpoint', ['players_view', 'posts_view', 'settings_view'])
def test_public_api_is_read_only(client, endpoint):
    assert client.post(reverse(endpoint), {}, content_type='application/json').status_code == 405


def test_admin_login_page(client):
    assert client.get(reverse('admin:login')).status_code == 200


def test_admin_post_form_uses_ckeditor5(admin_client):
    response = admin_client.get(reverse('admin:pokegutkowo_post_add'))
    assert response.status_code == 200
    assert b'django_ckeditor_5/dist/bundle.js' in response.content
    assert b'ckeditor/ckeditor/ckeditor.js' not in response.content


def test_editor_upload_requires_staff(client):
    response = client.post(reverse('ck_editor_5_upload_file'))
    assert response.status_code in (302, 403)


def test_cors_allows_local_frontend(client):
    response = client.get(reverse('players_view'), HTTP_ORIGIN='http://localhost:3000')
    assert response['Access-Control-Allow-Origin'] == 'http://localhost:3000'


def test_cors_rejects_unknown_origin(client):
    response = client.get(reverse('players_view'), HTTP_ORIGIN='https://untrusted.example')
    assert 'Access-Control-Allow-Origin' not in response


def test_editor_migration_preserves_existing_html(transactional_db):
    previous = [('pokegutkowo', '0002_auto_20201228_1452')]
    current = [('pokegutkowo', '0003_alter_post_context')]
    executor = MigrationExecutor(connection)
    executor.migrate(previous)
    try:
        apps = executor.loader.project_state(previous).apps
        author = apps.get_model('pokegutkowo', 'Player').objects.create(
            nickname='Trener', level=40, team='mystic',
        )
        html = '<h2>Stary post</h2><p><strong>Oryginalna treść</strong></p>'
        post = apps.get_model('pokegutkowo', 'Post').objects.create(
            title='Stary post', context=html, author=author,
        )
    finally:
        MigrationExecutor(connection).migrate(current)
    assert Post.objects.get(pk=post.pk).context == html
