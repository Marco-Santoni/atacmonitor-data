DROP TABLE IF EXISTS paline;
CREATE TABLE paline (
    stop_code varchar(10) PRIMARY KEY,
    stop_name varchar(200),
    stop_desc varchar(200),
    stop_lat float,
    stop_lon float
);
