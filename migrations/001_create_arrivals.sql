DROP TABLE IF EXISTS arrivals;
CREATE TABLE arrivals (
    id SERIAL PRIMARY KEY,
    tempo_attesa INTEGER,
    tempo_attesa_secondi INTEGER,
    distanza_fermate INTEGER,
    linea varchar(10),
    id_palina varchar(10),
    nome_palina varchar(40),
    collocazione varchar(60),
    capolinea varchar(40),
    in_arrivo boolean,
    a_capolinea boolean,
    created_at timestamp with time zone
);
