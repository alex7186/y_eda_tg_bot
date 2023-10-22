from pandas import DataFrame
import sqlite3
import os
from math import pi, sin, cos, atan2
from datetime import datetime

SQLITE3_CONNECTION = None


def calculate_distance(lat: float, lon: float, result_count: int = 10) -> DataFrame:
    global SQLITE3_CONNECTION

    cursor = SQLITE3_CONNECTION.cursor()
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

    global SQLITE3_CONNECTION

    cursor = SQLITE3_CONNECTION.cursor()

    cursor.execute(
        """
        insert into users_log (date, user_tg_id, location_longitude, location_latitude)
        values ("{}", "{}", {}, {})
        """.format(
            date_str, user_tg_id, location_longitude, location_latitude
        )
    )

    SQLITE3_CONNECTION.commit()
    cursor.close()


def _add_calculate_distance_procedure():
    global SQLITE3_CONNECTION

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

    SQLITE3_CONNECTION.create_function("calculate_distance", 4, _calculate_distance)


def read_logs_stat(n_max: int = 10):
    global SQLITE3_CONNECTION

    cursor = SQLITE3_CONNECTION.cursor()
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

    result["date"] = result["date"].apply(
        lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S").strftime("%H:%M %d.%m.%y")
    )

    result["geo"] = result[["latitude", "longitude"]].apply(
        lambda x: f"https://www.google.com/search?channel=fs&q={x[0]}+{x[1]}", axis=1
    )

    return result[["date", "user_tg_id", "geo"]]


def clear_self_logs():
    global SQLITE3_CONNECTION

    cursor = SQLITE3_CONNECTION.cursor()
    cursor.execute(
        """
        delete from users_log
        where user_tg_id = 747558089
        """
    )

    SQLITE3_CONNECTION.commit()
    cursor.close()


if __name__ != "__main__":

    SQLITE3_CONNECTION = sqlite3.connect(
        os.path.join(os.environ.get("BASE_DIR"), "data", "final_door_codes.db")
    )
    _add_calculate_distance_procedure()
