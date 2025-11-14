QUERY_RESPUESTAS = "SELECT * FROM RESPUESTAS;"


QUERY_MEJORES_PUNTAJES = """select
    p.nombre,
    (
        -- Subconsulta para calcular el puntaje total del grupo
        select
            sum(r.correctas)
        from
            RESPUESTAS r
        where
            r.idrespuesta in (
                -- Subconsulta interna para encontrar todas las IdRespuesta del grupo
                select
                    h.idrespuesta
                from
                    HACEN h
                where
                    h.grupoid = p.grupoid
            )
    ) as puntaje_total_grupal
from
    PARTICIPANTES p
order by
    puntaje_total_grupal desc"""

QUERY_PUNTAJE_FECHA = """select
    r_outer.Fecha,
    cast(r_outer.Correctas as unsigned) as puntaje_ganador
from
    PARTICIPANTES p,
    HACEN h_outer,
    RESPUESTAS r_outer
where
    p.GrupoId = h_outer.GrupoId
    and h_outer.IdRespuesta = r_outer.IdRespuesta
    and cast(r_outer.Correctas as unsigned) = (
        -- Subconsulta Correlacionada: Encuentra el Puntaje Máximo para la Fecha actual
        select max(cast(r_inner.Correctas as unsigned))
        from RESPUESTAS r_inner
        where r_inner.Fecha = r_outer.Fecha
    )
group by
    r_outer.Fecha
order by
    r_outer.Fecha;"""

QUERY_MAS_VELOCES = """select
    p.nombre,
    (
        -- subconsulta para calcular el tiempo total del grupo en segundos
        select
            sum(time_to_sec(r.tiempo_total))
        from
            RESPUESTAS r
        where
            r.idrespuesta in (
                -- subconsulta interna: obtiene los idrespuesta que pertenecen al grupo
                select
                    h.idrespuesta
                from
                    HACEN h
                where
                    h.grupoid = p.grupoid
            )
    ) as tiempo_total_segundos
from
    PARTICIPANTES p
order by
    tiempo_total_segundos asc -- ordenamos de menor a mayor (el mejor tiempo es el más bajo)"""