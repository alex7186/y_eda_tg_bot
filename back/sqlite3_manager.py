from pandas import DataFrame
import sqlite3
import os
from math import pi, sin, cos, atan2

SQLITE3_CONECTION = None


def sqlite3_manager_init(BASE_DIR=None, full_file_path=None):
    global SQLITE3_CONECTION

    if BASE_DIR:
        SQLITE3_CONECTION = sqlite3.connect(
            os.path.join(BASE_DIR, "data", "final_doorcodes.db")
        )
    else:
        SQLITE3_CONECTION = sqlite3.connect(full_file_path)

    _add_calculate_distance_procedure()

    return SQLITE3_CONECTION


def calculate_distance(lat: float, lon: float, result_count: int = 10) -> DataFrame:
    global SQLITE3_CONECTION

    cursor = SQLITE3_CONECTION.cursor()
    cursor.execute(
        """
        select 
            address_city, 
            address_street, 
            address_house, 
            address_entrance, 
            codes_list,
            calculate_distance(
                location_latitude, 
                location_longitude, 
                {}, {}
            ) as distance
        
        from y_eda_data

        order by distance

        limit {}
        """.format(
            lat, lon, result_count
        )
    )

    result = DataFrame(
        cursor.fetchall(),
        columns=(
            "address_city",
            "address_street",
            "address_house",
            "address_entrance",
            "codes_list",
            "distance",
        ),
    )
    cursor.close()
    return result


def add_log(
    date_str: str, user_tg_id: str, location_longitude: float, location_latitude: float
):

    global SQLITE3_CONECTION

    cursor = SQLITE3_CONECTION.cursor()

    cursor.execute(
        """
        insert into users_log (date, user_tg_id, location_longitude, location_latitude)
        values ("{}", "{}", {}, {})
        """.format(
            date_str, user_tg_id, location_longitude, location_latitude
        )
    )

    SQLITE3_CONECTION.commit()
    cursor.close()


def _add_calculate_distance_procedure():
    global SQLITE3_CONECTION

    def _calculate_distance(
        lat1: float, lon1: float, lat2: float, lon2: float
    ) -> float:

        delta_lat = (pi * lat2 / 180) - (pi * lat1 / 180)
        delta_lon = (pi * lon2 / 180) - (pi * lon1 / 180)

        dist = sin(delta_lat / 2) * sin(delta_lat / 2) + cos(lat1 * pi / 180) * cos(
            lat2 * pi / 180
        ) * sin(delta_lon / 2) * sin(delta_lon / 2)
        dist = 2 * atan2(dist ** (0.5), (1 - dist) ** (0.5)) * 6378.137 * 1000

        return dist

    SQLITE3_CONECTION.create_function("calculate_distance", 4, _calculate_distance)


def read_logs_stat(n_max: int = 10):
    global SQLITE3_CONECTION

    cursor = SQLITE3_CONECTION.cursor()
    cursor.execute(
        """
        select * from users_log
        order by date DESC
        limit {}
        """.format(
            n_max
        )
    )

    result = DataFrame(
        cursor.fetchall(),
        columns=(
            "date",
            "user_tg_id",
            "longitude",
            "latitude",
        ),
    )
    cursor.close()

    return result

def clear_self_logs():
    global SQLITE3_CONECTION

    cursor = SQLITE3_CONECTION.cursor()
    cursor.execute(
        """
        delete from users_log
        where user_tg_id = 747558089
        """
    )

    SQLITE3_CONECTION.commit()
    cursor.close()

