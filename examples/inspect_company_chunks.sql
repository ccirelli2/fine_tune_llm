SET @cik = '0001373715';
USE edgar;

SELECT fi.id, fi.file_name, fi.file_type, fc.chunk
FROM filing_index as fi
JOIN filing_chunks as fc ON fi.file_name = fc.foreign_id
WHERE
	fi.cik = @cik AND
	fi.file_type = '8-K' AND
    fc.chunk LIKE '%Net Income%'
LIMIT 10;
