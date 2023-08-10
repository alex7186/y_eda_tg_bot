import psycopg2
from pandas import DataFrame


POSTGRESQL_CONN = psycopg2.connect(
    host="localhost", dbname="y_eda_db", user="postgres", password="password"
)

# POSTGRESQL_CONN.autocommit = True


def calculate_distance(lat: float, lon: float, result_count: int = 10) -> DataFrame:
    global POSTGRESQL_CONN

    with POSTGRESQL_CONN.cursor() as cursor:

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
                    {}, {}, 'M'
                ) as distance
            
            from y_eda_data

            order by distance

            limit {}
            """.format(
                lat, lon, result_count
            )
        )

        return DataFrame(
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


def _create_table() -> None:
    global POSTGRESQL_CONN

    with POSTGRESQL_CONN.cursor() as cursor:
        cursor.execute(
            """
        CREATE TABLE y_eda_data (
            address_city varchar (100),
            address_street varchar (150),
            address_house varchar (50),
            address_entrance integer,
            location_longitude real,
            location_latitude real,
            codes_list varchar(100)
        )
        """
        )


def _add_calculate_distance_procedure1():
    global POSTGRESQL_CONN

    with POSTGRESQL_CONN.cursor() as cursor:
        cursor.execute(
            """
        CREATE OR REPLACE FUNCTION calculate_distance(
            lat1 float, lon1 float, lat2 float, lon2 float, units varchar)
        RETURNS float AS $dist$
            DECLARE
                dist float = 0;
                radlat1 float;
                radlat2 float;
                theta float;
                radtheta float;
            BEGIN
                -- IF lat1 = lat2 OR lon1 = lon2 THEN
                    -- RETURN dist;
                -- ELSE
                radlat1 = pi() * lat1 / 180;
                radlat2 = pi() * lat2 / 180;
                theta = lon1 - lon2;
                radtheta = pi() * theta / 180;
                dist = sin(radlat1) * sin(radlat2) + cos(radlat1) * cos(radlat2) * cos(radtheta);

                IF dist > 1 THEN dist = 1; END IF;

                dist = acos(dist);
                dist = dist * 180 / pi();
                dist = dist * 60 * 1.1515;

                IF units = 'K' THEN dist = dist * 1.609344; END IF;
                IF units = 'N' THEN dist = dist * 0.8684; END IF;

                RETURN dist;
                -- END IF;
            END;
        $dist$ LANGUAGE plpgsql;
        """
        )


def _add_calculate_distance_procedure2():
    global POSTGRESQL_CONN

    with POSTGRESQL_CONN.cursor() as cursor:
        cursor.execute(
        """
        CREATE OR REPLACE FUNCTION calculate_distance(
            lat1 float, lon1 float, lat2 float, lon2 float, units varchar)
        RETURNS float AS $dist$
            DECLARE
                dist float = 0;
                delta_lat float;
                delta_lon float;
            BEGIN

                delta_lat = (pi()*lat2/180) - (pi()*lat1/180);
                delta_lon = (pi()*lon2/180) - (pi()*lon1/180);

                dist = sin(delta_lat/2)*sin(delta_lat/2) + cos(lat1 * pi()/180) * cos(lat2*pi()/180) * sin(delta_lon/2)*sin(delta_lon/2);

                dist = 2 * atan2(sqrt(dist), sqrt(1-dist)) * 6378.137 * 1000;

                RETURN dist;

            END;
        $dist$ LANGUAGE plpgsql;
        """
        )
