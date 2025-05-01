import json
import pytest

from main import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()


def test_get_flight_success(client):
    response = client.get('/flights/get-flight/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['departure'] == 'Belem'
    assert data['destination'] == 'Maldivas'
    assert data['price'] == 2000


def test_get_flight_not_found(client):
    response = client.get('/flights/get-flight/999')
    assert response.status_code == 404
    assert response.get_json() == {'error': 'Not found'}


def test_search_flights_success(client):
    response = client.get('/flights/search-flights/Belem/Maldivas')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 1
    for flight in data:
        assert 'departure' in flight
        assert 'destination' in flight
        assert 'price' in flight


def test_search_flights_case_insensitive(client):
    response = client.get('/flights/search-flights/belem/maldivas')
    assert response.status_code == 200


def test_search_flights_not_found(client):
    response = client.get('/flights/search-flights/Algum/Lugar')
    assert response.status_code == 404
    assert response.get_json() == {'error': 'No flights available for this trip.'}


def test_book_flight_success(client):
    payload = {'username': 'John Doe', 'email': 'email@exemplo.com'}
    response = client.post('/flights/book-flight/1/10A',
                           data=json.dumps(payload),
                           content_type='application/json')
    assert response.status_code == 201
    assert response.get_json() == {'message': 'Flight booked successfully'}


def test_book_flight_missing_data(client):
    response = client.post('/flights/book-flight/1/10A',
                           data=json.dumps({}),
                           content_type='application/json')
    assert response.status_code == 400
    assert response.get_json() == {'error': 'username and email required'}


def test_book_flight_seat_not_available(client):
    payload = {'username': 'John Doe', 'email': 'email@exemplo.com'}
    response = client.post('/flights/book-flight/1/99Z',
                           data=json.dumps(payload),
                           content_type='application/json')
    assert response.status_code == 400
    assert response.get_json() == {'error': 'Seat not available'}


def test_book_flight_no_seats(client):
    payload = {'username': 'John Doe', 'email': 'email@exemplo.com'}
    response = client.post('/flights/book-flight/2/1A',
                           data=json.dumps(payload),
                           content_type='application/json')
    assert response.status_code == 400
    assert response.get_json() == {'error': 'No seats available'}


def test_book_flight_not_found(client):
    payload = {'username': 'John Doe', 'email': 'email@exemplo.com'}
    response = client.post('/flights/book-flight/999/10A',
                           data=json.dumps(payload),
                           content_type='application/json')
    assert response.status_code == 404
    assert response.get_json() == {'error': 'Flight not found'}
