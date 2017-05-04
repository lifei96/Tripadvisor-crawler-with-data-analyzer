# -*- coding: utf-8 -*-

import googlemaps


def dist_duration(origins, destinations, mode, key):
    gmaps = googlemaps.Client(key=key)
    distance_matrix_result = gmaps.distance_matrix(origins=origins, destinations=destinations,
                                                   mode=mode, language='en-US', units='metric')
    if distance_matrix_result['status'] != 'OK':
        return distance_matrix_result['status'], '', 0, 0
    element = distance_matrix_result['rows'][0]['elements'][0]
    if element['status'] != 'OK':
        return 'OK', element['status'], 0, 0
    return 'OK', 'OK', element['distance']['value'], element['duration']['value']


if __name__ == '__main__':
    print dist_duration('columbia, maryland', 'New York', 'driving', 'AIzaSyCDGB2qXJN654aXykZ9LyT83Lp4bXVJ_7k')
