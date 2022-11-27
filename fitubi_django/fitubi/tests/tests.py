import pytest

from .testutils import *


@pytest.mark.django_db
def test_user_connection():
    users_count = count_users()
    fitubiusers_count = count_fitubiusers()
    user = create_user()
    assert count_users() == users_count + 1
    assert count_fitubiusers() == fitubiusers_count + 1
    assert check_fitubiuser(user) == True


# @pytest.mark.django_db
# def test_get_movie_list(client, set_up):
#     response = client.get("/movies/", {}, format='json')
#
#     assert response.status_code == 200
#     assert Movie.objects.count() == len(response.data)
#
#
# @pytest.mark.django_db
# def test_get_movie_detail(client, set_up):
#     movie = Movie.objects.first()
#     response = client.get(f"/movies/{movie.id}/", {}, format='json')
#
#     assert response.status_code == 200
#     for field in ("title", "year", "description", "director", "actors"):
#         assert field in response.data
#
#
# @pytest.mark.django_db
# def test_delete_movie(client, set_up):
#     movie = Movie.objects.first()
#     response = client.delete(f"/movies/{movie.id}/", {}, format='json')
#     assert response.status_code == 204
#     movie_ids = [movie.id for movie in Movie.objects.all()]
#     assert movie.id not in movie_ids
#
#
# @pytest.mark.django_db
# def test_update_movie(client, set_up):
#     movie = Movie.objects.first()
#     response = client.get(f"/movies/{movie.id}/", {}, format='json')
#     movie_data = response.data
#     new_year = 3
#     movie_data["year"] = new_year
#     new_actors = [random_person().name]
#     movie_data["actors"] = new_actors
#     response = client.patch(f"/movies/{movie.id}/", movie_data, format='json')
#     assert response.status_code == 200
#     movie_obj = Movie.objects.get(id=movie.id)
#     assert movie_obj.year == new_year
#     db_actor_names = [actor.name for actor in movie_obj.actors.all()]
#     assert len(db_actor_names) == len(new_actors)