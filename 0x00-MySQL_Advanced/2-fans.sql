--  ranks country origins of bands, ordered by the number of (non-unique) fans
-- curl https://intranet.alxswe.com/rltoken/uPn947gnZLaa0FJrrAFTGQ
SELECT origin, SUM(fans) AS nb_fans FROM metal_bands GROUP BY origin ORDER BY nb_fans DESC;